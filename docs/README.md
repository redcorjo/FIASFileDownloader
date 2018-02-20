GetLastDownloadFileInfo

Возвращает информацию о последней версии файлов, доступных для скачивания

Тест

Форма для тестирования доступна только для запросов от локальных компьютеров.
SOAP 1.1

В следующем примере показаны запрос и ответ SOAP 1.1. Вместо элементов-заполнителей следует подставить фактические значения.

POST /WebServices/Public/DownloadService.asmx HTTP/1.1
Host: fias.nalog.ru
Content-Type: text/xml; charset=utf-8
Content-Length: length
SOAPAction: "http://fias.nalog.ru/WebServices/Public/DownloadService.asmx/GetLastDownloadFileInfo"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetLastDownloadFileInfo xmlns="http://fias.nalog.ru/WebServices/Public/DownloadService.asmx" />
  </soap:Body>
</soap:Envelope>
HTTP/1.1 200 OK
Content-Type: text/xml; charset=utf-8
Content-Length: length

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetLastDownloadFileInfoResponse xmlns="http://fias.nalog.ru/WebServices/Public/DownloadService.asmx">
      <GetLastDownloadFileInfoResult>
        <VersionId>int</VersionId>
        <TextVersion>string</TextVersion>
        <FiasCompleteDbfUrl>string</FiasCompleteDbfUrl>
        <FiasCompleteXmlUrl>string</FiasCompleteXmlUrl>
        <FiasDeltaDbfUrl>string</FiasDeltaDbfUrl>
        <FiasDeltaXmlUrl>string</FiasDeltaXmlUrl>
        <Kladr4ArjUrl>string</Kladr4ArjUrl>
        <Kladr47ZUrl>string</Kladr47ZUrl>
      </GetLastDownloadFileInfoResult>
    </GetLastDownloadFileInfoResponse>
  </soap:Body>
</soap:Envelope>
SOAP 1.2

В следующем примере показаны запрос и ответ SOAP 1,2. Вместо элементов-заполнителей следует подставить фактические значения.

POST /WebServices/Public/DownloadService.asmx HTTP/1.1
Host: fias.nalog.ru
Content-Type: application/soap+xml; charset=utf-8
Content-Length: length

<?xml version="1.0" encoding="utf-8"?>
<soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
  <soap12:Body>
    <GetLastDownloadFileInfo xmlns="http://fias.nalog.ru/WebServices/Public/DownloadService.asmx" />
  </soap12:Body>
</soap12:Envelope>
HTTP/1.1 200 OK
Content-Type: application/soap+xml; charset=utf-8
Content-Length: length

<?xml version="1.0" encoding="utf-8"?>
<soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
  <soap12:Body>
    <GetLastDownloadFileInfoResponse xmlns="http://fias.nalog.ru/WebServices/Public/DownloadService.asmx">
      <GetLastDownloadFileInfoResult>
        <VersionId>int</VersionId>
        <TextVersion>string</TextVersion>
        <FiasCompleteDbfUrl>string</FiasCompleteDbfUrl>
        <FiasCompleteXmlUrl>string</FiasCompleteXmlUrl>
        <FiasDeltaDbfUrl>string</FiasDeltaDbfUrl>
        <FiasDeltaXmlUrl>string</FiasDeltaXmlUrl>
        <Kladr4ArjUrl>string</Kladr4ArjUrl>
        <Kladr47ZUrl>string</Kladr47ZUrl>
      </GetLastDownloadFileInfoResult>
    </GetLastDownloadFileInfoResponse>
  </soap12:Body>
</soap12:Envelope>