FIASFileDownloader

Coded by: redcorjo

Date    : 20180225

This script is used to download all full and deltas from FIAS site http://fias.nalog.ru

Required:

Python 2.7 installed

Python module rarfile installed

Unrar binary (OS depenedent) pre installed

usage: FIASFileDownloader.py [-h] [--version] [-df] [-dd] [-da] [-x [PROXY]]

                             [-p [PATH]] [-d [DELETE]]

optional arguments:

  -h, --help            show this help message and exit

  --version             show program's version number and exit

  -df, --downloadfull   Download Full database

  -dd, --downloaddelta  Download last delta database

  -da, --downloadall    Download last Full and last Delta database

  -x [PROXY], --proxy [PROXY]
                        HTTP Proxy in format <hostname>:<port>

  -p [PATH], --path [PATH]
                        Path to keep files

  -d [DELETE], --delete [DELETE]
                        Delete older files (default 30 days)