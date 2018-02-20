import urllib2
import os
from urllib2 import urlopen, URLError, HTTPError

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

    # #IF YOU ARE NOT BEHIND A PROXY, DELETE THIS BLOCK
    # http_proxy_server = "10.115.4.2"
    # http_proxy_port = "8080"
    # http_proxy_realm = http_proxy_server
    # http_proxy_full_auth_string = "http://%s:%s" % (http_proxy_server, http_proxy_port)
    # proxy = urllib2.ProxyHandler({'http': http_proxy_full_auth_string})
    # opener = urllib2.build_opener(proxy)
    # urllib2.install_opener(opener)
    # #END OF --> IF YOU ARE NOT BEHIND A PROXY, DELETE THIS BLOCK

    response = urllib2.urlopen(request_object)
    html_string = response.read()
    return html_string

def downloadLastDelta():
    url_delta = "http://fias.nalog.ru/Public/Downloads/Actual/fias_delta_xml.rar"
    filename = url_delta.split("/")[-1]
    downloadfile(url_delta, filename)
    pass

def downloadLastFull():
    url_full = "http://fias.nalog.ru/Public/Downloads/Actual/fias_xml.rar"
    filename = url_full.split("/")[-1]

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

def main():
    print "main"
    html_string = checkFiles()
    downloadLastDelta()
    print html_string

if __name__ == "__main__":
    main()