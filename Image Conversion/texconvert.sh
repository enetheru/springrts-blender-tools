#!/bin/bash
#
VERSION=0.1

function print_help
{
echo "Version: $0 $VERSION
Generates Final images for SpringRTS features.

Usage: $0 imagefile [options ...] outprefix

Options:
  -h, --help               display this help
  -v, --verbose            detailed output
      --nocompress         dont compress with nvidia-texture-tools
  -d, --diffuse <file>     RGB[A] image, will use alpha if present
                            unless --alpha is specified
  -a, --ambient <file>     greyscale image for ambient light values
  -s, --specular <file>    greyscale image for specularity values
  -t, --teamcolour <file>  greyscale image for team colour values
      --alpha <file>       greyscale image for alpha values
  -o, --outfile <string>   output file name
";
}


# NOTE: This requires GNU getopt.  On Mac OS X, you get BSD getopt by default,
# which doesn't work; see below.
TEMP=`getopt -o hvcd:a:s:t:o:b: \
    --long help,verbose,diffuse:,ambient:,specular:,teamcolour:,alpha:,blue:,outfile: \
    -n "$0" -- "$@"`

if [ $? != 0 ] ; then echo -n -e "Terminating..." >&2 ; exit 1 ; fi

# Note the quotes around `$TEMP': they are essential!
eval set -- "$TEMP"

HELP=false;VERBOSE=true;COMPRESS=true;DIFFUSE=;AMBIENT=;SPECULAR=;TEAMCOLOUR=;ALPHA=;OUTFILE=;BLUE=;

while true; do
  case "$1" in
    -h | --help ) print_help ; exit 0 ;;
    -q | --quiet ) VERBOSE=false; shift ;;
         --nocompress ) COMPRESS=false; shift ;;
    -d | --diffuse ) DIFFUSE="$2"; shift 2 ;;
    -a | --ambient ) AMBIENT="$2"; shift 2 ;;
    -s | --specular ) SPECULAR="$2"; shift 2 ;;
    -t | --teamcolour ) TEAMCOLOUR="$2"; shift 2 ;;
    -b | --blue ) BLUE="$2"; shift 2 ;;
         --alpha ) ALPHA="$2"; shift 2 ;;
    -o | --outfile ) OUTFILE="$2"; shift 2 ;;
    -- ) shift; break ;;
    * ) break ;;
  esac
done

# Checking for requirements
command -v convert >/dev/null 2>&1 || { echo -n -e >&2 "Imagemagick is required please install"; exit 1; }
command -v nvcompress >/dev/null 2>&1 || { echo -n -e >&2 "nvidia-texture-tools not found cannot compress images to dds format"; COMPRESS=false; }

# Check to see if our diffuse texture has been specified.
if [ -z "$DIFFUSE" ];
    then
        if [ -z $1 ];
            then
                print_help;
                echo -n -e "ERROR: No Diffuse File Specified\n";
                exit 1;
            else
                DIFFUSE=$1
        fi
fi

echo "LOG: Checking diffuse file format"
if ! identify $DIFFUSE; then echo "ERROR: $DIFFUSE not found or invalid format"; exit 1; fi

# Check to see if output is specified.
if [ -z "$OUTFILE" ];
    then
        if [ -z $2 ];
            then
                OUTFILE=${DIFFUSE%.*};
            else
                OUTFILE=$2
        fi
fi

if [ $VERBOSE = true ]; then echo -e \
"== Options: ==
Verbose: $VERBOSE
Compress: $COMPRESS
Diffuse: $DIFFUSE
Alpha: $ALPHA
Ambient: $AMBIENT
Specular: $SPECULAR
Team Colour: $TEAMCOLOUR
OutPrefix: $OUTFILE\n";
fi

# Create Black greyscale image for use when image doesnt exist.
if [ $VERBOSE = true ]; then echo -n "* Creating Temporary black and white images..."; fi
convert $DIFFUSE -alpha deactivate -black-threshold 200% black_TEMP.tga
convert black_TEMP.tga -negate white_TEMP.tga
if [ $VERBOSE = true ]; then echo "Done"; fi


if [ "$AMBIENT" = "" ]; then AMBIENT=black_TEMP.tga; fi
if [ "$SPECULAR" = "" ]; then SPECULAR=black_TEMP.tga; fi
if [ "$TEAMCOLOUR" = "" ]; then TEAMCOLOUR=black_TEMP.tga; fi
if [ "$BLUE" = "" ]; then BLUE=black_TEMP.tga; fi


# Separate RGB from diffuse
if [ $VERBOSE = true ]; then echo -n "* Separating RGB from diffuse..."; fi
convert $DIFFUSE -alpha deactivate rgb_TEMP.tga
if [ $VERBOSE = true ]; then echo "Done"; fi


# Separate alpha from diffuse
if [ "$ALPHA" = "" ];
    then
        if [ $VERBOSE = true ]; then echo -n "* Extracting alpha from diffuse..."; fi
        convert $DIFFUSE -channel a -alpha extract -separate alpha_TEMP.tga;
        ALPHA="alpha_TEMP.tga"
        if [ $VERBOSE = true ]; then echo "Done"; fi
fi


# Build tex1
if [ $VERBOSE = true ]; then echo -n "* Building tex1..."; fi
convert \( $DIFFUSE -channel r -separate \) \( $DIFFUSE -channel g -separate \) \
\( $DIFFUSE -channel b -separate \) $TEAMCOLOUR -channel rgba -alpha copy \
-combine  "$OUTFILE""_tex1.tga"
if [ $VERBOSE = true ]; then echo "Done"; fi


# Build tex2
if [ $VERBOSE = true ]; then echo -n "* Building tex2..."; fi
convert $AMBIENT $SPECULAR $BLUE $ALPHA -channel rgba -combine "$OUTFILE""_tex2.tga"
if [ $VERBOSE = true ]; then echo "Done"; fi


# remove temp files
if [ $VERBOSE = true ]; then echo -n "* Removing Temporary Files..."; fi
rm black_TEMP.tga rgb_TEMP.tga alpha_TEMP.tga white_TEMP.tga
if [ $VERBOSE = true ]; then echo "Done"; fi


# compress using nvtt
if [ $COMPRESS = true ];
    then
    if [ $VERBOSE = true ]; then echo "* Compressing Textures with nvidia-texture-tools..."; fi
    nvcompress -bc2 "$OUTFILE""_tex1.tga";
    nvcompress -bc2 "$OUTFILE""_tex2.tga";
    rm "$OUTFILE""_tex1.tga";
    rm "$OUTFILE""_tex2.tga";
fi
if [ $VERBOSE = true ]; then echo "Done"; fi
