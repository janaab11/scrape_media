#! /bin/bash
# download.sh [--file|-f <csv-file>] [--audio|-a <audio-dir>]

# Default values of arguments
NAME=lesson
CSV=raw/media_lesson.csv
DATA_DIR=data

# Loop through arguments and process them
for arg in "$@"
do
    case $arg in
        -n|--name)
        NAME="$2"
        shift # Remove argument name from processing
        shift # Remove argument value from processing
        ;;
        -f|--file)
        CSV="$2"
        shift # Remove argument name from processing
        shift # Remove argument value from processing
        ;;
        -d|--data)
        DATA_DIR="$2"
        shift # Remove argument name from processing
        shift # Remove argument value from processing
        ;;
        OTHERS+="$1")
        shift # Remove generic argument from processing
        ;;
    esac
done

set -x

download() {
    mkdir -p ${1}/${2}/${3}
    wget ${4} -O ${1}/${2}/${3}/${5}.mp3 
#    curl "$(echo $2 | xargs)" | ffmpeg -i - $3/$1.wav #as we are processing it by librosa which automatically coverts it to mono and sampling rate can be handled there as well removing -ac 1  -ar 8000
}

export -f download
mkdir -p ${DATA_DIR}
cat ${CSV} | parallel --bar --colsep ',' download ${DATA_DIR} {1} {2} {3} ${NAME}

#jq -c '.[]' $1 | while read -r line; do
#    read -r f1 f2 f3 f4 f5 <<< $(jq -c '.[]' <<< $line)
#    download $f1 $f4 $2 &
#done

# 1000 audio 913 succesfully downloaded 87 remaining.
