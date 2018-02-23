import urllib2
import os
from urllib2 import urlopen, URLError, HTTPError
import time
import re
import argparse

def checkFiles():
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

    # # #IF YOU ARE NOT BEHIND A PROXY, DELETE THIS BLOCK
    # http_proxy_server = "127.0.0.1"
    # http_proxy_port = "3128"
    # http_proxy_realm = http_proxy_server
    # http_proxy_full_auth_string = "http://%s:%s" % (http_proxy_server, http_proxy_port)
    # proxy = urllib2.ProxyHandler({'http': http_proxy_full_auth_string})
    # opener = urllib2.build_opener(proxy)
    # urllib2.install_opener(opener)
    # # #END OF --> IF YOU ARE NOT BEHIND A PROXY, DELETE THIS BLOCK
    if proxy:
        useProxy()

    response = urllib2.urlopen(request_object)
    html_string = response.read()
    return html_string

def useProxy():
    # #IF YOU ARE NOT BEHIND A PROXY, DELETE THIS BLOCK
    http_proxy_server = "127.0.0.1"
    http_proxy_port = "3128"
    http_proxy_realm = http_proxy_server
    http_proxy_full_auth_string = "http://%s:%s" % (http_proxy_server, http_proxy_port)
    proxy = urllib2.ProxyHandler({'http': http_proxy_full_auth_string})
    opener = urllib2.build_opener(proxy)
    urllib2.install_opener(opener)
    # #END OF --> IF YOU ARE NOT BEHIND A PROXY, DELETE THIS BLOCK

def downloadLastDelta(url=""):
    if url == "":
        url_delta = "http://fias.nalog.ru/Public/Downloads/Actual/fias_delta_xml.rar"
    else:
        url_delta = url
    filename = url_delta.split("/")[-1]
    print "Downloading last delta {0}".format(url_delta)
    downloadLargeFile(url_delta, filename)
    pass

def downloadLastFull(url=""):
    if url == "":
        url_full = "http://fias.nalog.ru/Public/Downloads/Actual/fias_xml.rar"
    else:
        url_full = url
    #url_full = "http://fias.nalog.ru/Public/Downloads/20180215/fias_dbf.rar"
    filename = url_full.split("/")[-1]
    #downloadfile(url_full, filename)
    print "Downloading last full {0}".format(url_full)
    downloadLargeFile(url_full, filename)
    pass

def downloadfile(url, filename):
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
    """Helper to download large files
        the only arg is a url
       this file will go to a temp directory
       the file will also be downloaded
       in chunks and print out how much remains
    """

    baseFile = os.path.basename(url)

    # move the file to a more uniq path
    os.umask(0002)
    #temp_path = "./downloads"
    temp_path = downloadpath
    if not os.path.exists(temp_path):
        os.makedirs(temp_path)
    baselinetime = time.time()
    try:
        #file = os.path.join(temp_path, baseFile)
        file = os.path.join(temp_path, filename)

        if proxy:
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
                percentage = int (( float(downloaded) / float(total_size) ) * 100.00 )
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
                if not chunk:
                    #pass
                    break
                if downloaded == total_size:
                    print "Complete downloaded"
                    break
                fp.write(chunk)
    except urllib2.HTTPError, e:
        print "HTTP Error:", e.code, url
        return False
    except urllib2.URLError, e:
        print "URL Error:", e.reason, url
        return False

    return file

def main():
    print "main"
    parser = argparse.ArgumentParser()
    parser.add_argument("-df","--downloadfull", help="Download Full database", action="store_true")
    parser.add_argument("-dd","--downloaddelta", help="Download last delta database", action="store_true")
    parser.add_argument("-x", "--proxy", help="HTTP Proxy in format <hostname>:<port>", nargs='?', type=str)
    parser.add_argument("-p", "--path", help="Path to keep files", nargs='?', const="downloads", type=str, default="downloads")
    args = parser.parse_args()

    global downloadpath
    downloadpath = args.path

    global proxy
    proxy = args.proxy

    html_string = checkFiles()
    p = re.compile(r".+FiasCompleteXmlUrl>(http://[^<]+)</.+", re.IGNORECASE)
    results = p.search(html_string)
    urllastfull = results.group(1)

    p = re.compile(r".+FiasDeltaXmlUrl>(http://[^<]+)</.+", re.IGNORECASE)
    results = p.search(html_string)
    urllastdelta = results.group(1)

    p = re.compile(r".+VersionId>([0-9]+)</.+", re.IGNORECASE)
    results = p.search(html_string)
    version = results.group(1)

    print "Lst Version:{0} Lastfull:{1} Lastdelta:{2}".format(version, urllastfull, urllastfull)
    if args.downloaddelta:
        downloadLastDelta(url=urllastdelta)
    if args.downloadfull:
        downloadLastFull(url=urllastfull)
    pass

if __name__ == "__main__":
    main()