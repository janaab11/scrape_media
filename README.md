This repo is meant to scrape media from the <>pod101.com series of websites. To begin with, set your base website and login details in the `scripts/scraper.py` script. Then run the `run.sh` script in root directory with `--start` and `--end` flags to download the corresponding lessons (starting from 2). For example run:
```
sh run.sh --start=2 --end=101
```

to download the first 100 lessons scraped. If you are feeling generous with your harddisk space, you can also run it will `--all=1` flag to download all the scraped lessons. 

For more details and control, look under the hood of `run.sh`
