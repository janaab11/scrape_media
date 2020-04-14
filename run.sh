#! /bin/bash
# run.sh [--all=BOOLEAN] [--start=LINE_NUMBER] [--end=LINE_NUMBER] [--download|-d <download-dir>]

ALL=0
START=2
END=101
DOWNLOAD_DIR=data

# Loop through arguments and process them
for arg in "$@"
do
    case $arg in
        --all=*)
        ALL="${arg#*=}"
        shift # Remove --cache= from processing
        ;;
        --start=*)
        START="${arg#*=}"
        shift # Remove --cache= from processing
        ;;
        --end=*)
        END="${arg#*=}"
        shift # Remove --cache= from processing
        ;;
        -d|--download)
        DOWNLOAD_DIR="$2"
        shift # Remove argument name from processing
        shift # Remove argument value from processing
        ;;
        OTHERS+="$1")
        shift # Remove generic argument from processing
        ;;
    esac
done

if [ ! -f raw/media.csv ]
then
	# run scrapy spider
	scrapy runspider scripts/scraper.py
fi

# clean collected links
python3 scripts/clean_links.py raw/media.csv
# # calculate link url sizes
# python3 scripts/total_size.py raw/media.csv

for name in lesson review dialog notes
do
	# build csv for download
	python3 scripts/build_final.py raw/media.csv ${name}

	if [ "$ALL" -eq "1" ]
	then
		cat raw/media_${name}.csv > raw/temp.csv
	else
		# build subset of csv
		sed -n -e ${START},${END}p -e 1p raw/media_${name}.csv > raw/temp.csv
	fi

	# download all urls in csv
	python3 scripts/get_audios.py -f raw/temp.csv -n ${name} -d ${DOWNLOAD_DIR}
done

# print size of download directory
du -hs $DOWNLOAD_DIR
