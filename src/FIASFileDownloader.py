import urllib2
import os
from urllib2 import urlopen, URLError, HTTPError
import time
import re
import argparse
# https://pypi.python.org/pypi/rarfile
import rarfile

def checkFiles():
    """
    Check last version of files to download from fias.nalog.ru using avaiable SOAP APIs from site
    :return:
    """
    url = "http://fias.nalog.ru/WebServices/Public/DownloadService.asmx?WSDL"

    post_data = """
    <soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
      <soap12:Body>
        <GetLastDownloadFileInfo xmlns="http://fias.nalog.ru/WebServices/Public/DownloadService.asmx" />
      </soap12:Body>
    </soap12:Envelope>"""
    length = len(post_data)

    http_headers = {
        "Accept": "application/soap+xml,multipart/related,text/*",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "Host": "fias.nalog.ru",
        "Content-Type": "application/soap+xml; charset=utf-8",
        "Content-Length": length
    }

    request_object = urllib2.Request(url, post_data, http_headers)

    if myproxy:
        useProxy()

    try:
        response = urllib2.urlopen(request_object)
        html_string = response.read()
    except Exception,e:
        print "Error downloading from url. Error code: {0}".format(str(e))
        html_string = ""
    return html_string

def useProxy():
    """
    Implement HTTP proxy for outbound access
    :return:
    """
    http_proxy_server = myproxy.split(":")[0]
    http_proxy_port = myproxy.split(":")[1]
    http_proxy_realm = http_proxy_server
    http_proxy_full_auth_string = "http://%s:%s" % (http_proxy_server, http_proxy_port)
    proxy = urllib2.ProxyHandler({'http': http_proxy_full_auth_string})
    opener = urllib2.build_opener(proxy)
    urllib2.install_opener(opener)

def downloadLastDelta(url=""):
    """
    Method used to download the last delta file using predefined hardened link
    :param url:
    :return:
    """
    if url == "":
        url_delta = "http://fias.nalog.ru/Public/Downloads/Actual/fias_delta_xml.rar"
    else:
        url_delta = url
    filename = url_delta.split("/")[-1]
    print "Downloading last delta {0}".format(url_delta)
    downloadLargeFile(url_delta, filename)
    unrarFile(downloadpath + "/" + filename)
    pass

def downloadLastFull(url=""):
    """
    Method used to download the last delta file using predefined hardened link
    :param url:
    :return:
    """
    if url == "":
        url_full = "http://fias.nalog.ru/Public/Downloads/Actual/fias_xml.rar"
    else:
        url_full = url
    #url_full = "http://fias.nalog.ru/Public/Downloads/20180215/fias_dbf.rar"
    filename = url_full.split("/")[-1]
    #downloadfile(url_full, filename)
    print "Downloading last full {0}".format(url_full)
    downloadLargeFile(url_full, filename)
    unrarFile(downloadpath + "/" + filename)
    pass

def downloadfile(url, filename):
    """
    Method to download files. Only suitable when files are not large
    :param url:
    :param filename:
    :return:
    """
    # Open the url
    print "Downloading file {0} from URL {1}".format(filename,url)
    try:
        f = urlopen(url)
        print "downloading " + url

        # Open our local file for writing
        with open(filename, "wb") as local_file:
            local_file.write(f.read())
    #handle errors
    except HTTPError, e:
        print "HTTP Error:", e.code, url
    except URLError, e:
        print "URL Error:", e.reason, url

def downloadLargeFile(url, filename):
    """
    Method used to download large files by chunks of data
    :param url:
    :param filename:
    :return:
    """

    baseFile = os.path.basename(url)

    temp_path = downloadpath
    if not os.path.exists(temp_path):
        os.makedirs(temp_path)
    baselinetime = time.time()
    try:
        file = os.path.join(temp_path, filename)

        if myproxy:
            useProxy()
        req = urllib2.urlopen(url)
        total_size = int(req.info().getheader('Content-Length').strip())
        downloaded = 0
        CHUNK = 256 * 10240
        with open(file, 'wb') as fp:
            while True:
                chunk = req.read(CHUNK)
                currenttime = time.time()
                deltatime = int (currenttime - baselinetime)
                percentage = float((float(downloaded) / float(total_size)) * 100.00)
                if percentage > 0:
                    totaltime = int (( float(deltatime) / float(percentage) ) * 100.00)
                    if deltatime > totaltime:
                        remainingtime = "N/A"
                    else:
                        remainingtime = totaltime - deltatime
                else:
                    totaltime = "N/A"
                    remainingtime = "N/A"
                downloaded += len(chunk)
                print "Total size:{0}bytes Downloaded:{1}bytes - Downloaded Percentage:{2}% TimeElapsed:{3}s TotalExpectedtime:{4}s RemainingTime:{5}s ".format(total_size, downloaded, int(percentage), deltatime, totaltime, remainingtime )
                if not chunk and downloaded == total_size:
                    print "Download completed"
                    break
                elif not chunk and not downloaded == total_size:
                    print "Cancelled transfer"
                    break
                fp.write(chunk)
    except urllib2.HTTPError, e:
        print "HTTP Error:", e.code, url
        return False
    except urllib2.URLError, e:
        print "URL Error:", e.reason, url
        return False

    return file

def unrarFile(filename):
    """
    Method to unrar the file. It uses python module unrar, and binary unrar at OS
    :param filename:
    :return:
    """
    rf = rarfile.RarFile(filename)
    for f in rf.infolist():
        print f.filename, f.file_size
        try:
            rf.extract(f.filename,path=downloadpath)
        except Exception,e:
            print "Exception {0} for file {1}".format(str(e),f.filename)
    rf.close()


def cleanupOldFiles(aging=40):
    """
    Method to cleanup (housekeep) older files
    :param aging:
    :return:
    """
    print "Purging files older than {0} days from folder {1}".format(aging, downloadpath)
    if os.path.exists(downloadpath) and os.path.isdir(downloadpath):
        now = time.time()
        for myfile in os.listdir(downloadpath):
            if os.stat(os.path.join(downloadpath, myfile)).st_mtime < now - aging * 86400 and \
                    ( myfile.lower().endswith("xml") or myfile.lower().endswith("rar") ):
                filetodelete = os.path.join(downloadpath, myfile)
                print "Delete file {0}".format(filetodelete)
                os.remove(filetodelete)

    else:
        print "Path not valid"

def main():
    """
    Main entry point to the execution
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', action='version', version='%(prog)s 0.4')
    parser.add_argument("-df","--downloadfull", help="Download Full database", action="store_true")
    parser.add_argument("-dd","--downloaddelta", help="Download last delta database", action="store_true")
    parser.add_argument("-da", "--downloadall", help="Download last Full and last Delta database", action="store_true")
    parser.add_argument("-x", "--proxy", help="HTTP Proxy in format <hostname>:<port>", nargs='?', type=str)
    parser.add_argument("-p", "--path", help="Path to keep files", nargs='?', const="downloads", type=str, default="downloads")
    parser.add_argument("-d", "--delete", help="Delete older files (default 30 days)", nargs='?', const=30, type=int,
                        default=30)
    args = parser.parse_args()

    global downloadpath
    downloadpath = args.path

    global myproxy
    myproxy = args.proxy

    aging = args.delete

    if args.downloaddelta or args.downloadfull or args.downloadall:
        html_string = checkFiles()
        if not html_string == "":
            metadata = os.path.join(downloadpath, "metadata.xml")
            with open(metadata,"w") as metadatafile:
                metadatafile.write(html_string)

            p = re.compile(r".+FiasCompleteXmlUrl>(http://[^<]+)</.+", re.IGNORECASE)
            results = p.search(html_string)
            urllastfull = results.group(1)

            p = re.compile(r".+FiasDeltaXmlUrl>(http://[^<]+)</.+", re.IGNORECASE)
            results = p.search(html_string)
            urllastdelta = results.group(1)

            p = re.compile(r".+VersionId>([0-9]+)</.+", re.IGNORECASE)
            results = p.search(html_string)
            version = results.group(1)

            print "Last Version:{0} Lastfull:{1} Lastdelta:{2}".format(version, urllastfull, urllastfull)

    if html_string != "" and ( args.downloaddelta or args.downloadall ):
        downloadLastDelta(url=urllastdelta)

    if html_string != "" and ( args.downloadfull or args.downloadall ):
        downloadLastFull(url=urllastfull)

    cleanupOldFiles(aging=aging)

    pass

if __name__ == "__main__":
    main()