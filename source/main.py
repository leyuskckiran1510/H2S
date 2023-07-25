"""
Author :- Leyuskc
Date:- 2023/25/7 [initial]
License :- GNU/MIT

Note:- IT IS IMPLEMENTED AS DESCRIBED BY W3C 
           link:- [https://w3c.github.io/web-performance/specs/HAR/Overview.html]
       @ QUOTE FROM W3C
      "
       This specification defines an archival format for HTTP transactions 
       that can be used by a web browser to export detailed performance data 
       about web pages it loads. The format is intended to be flexible so that
       it can be adopted by various tools. The information that can be represented
       in this archival format includes both information about the web pages themselves
       e.g. the size of individual resources on the page as well as performance data e.g.
       how long did it take to download a particular resource on the page. A standard format
       to represent this information will allow various performance tools to interoperate with
       each other.
       "

       And Me as a author of this code don't take any liablity of 
       this code usage.It is just a HTTP Archive [HAR] parser implemented 
       in python for easy analysis 
        
"""

import json
from urllib.parse import urlencode
from typing import Any, Dict, List, Union
from requests.cookies import cookiejar_from_dict
from requests.structures import CaseInsensitiveDict
from base64 import standard_b64decode as base64decode


class _cookie:
    """
    name [string] - The name of the cookie.
    value [string] - The cookie value.
    path [string, optional] - The path pertaining to the cookie.
    domain [string, optional] - The host of the cookie.
    expires [string, optional] - Cookie expiration time. (ISO 8601 - YYYY-MM-DDThh:mm:ss.sTZD, e.g. 2009-07-24T19:20:30.123+02:00).
    httpOnly [boolean, optional] - Set to true if the cookie is HTTP only, false otherwise.
    secure [boolean, optional] (new in 1.2) - True if the cookie was transmitted over ssl, false otherwise.
    comment [string, optional] (new in 1.2) - A comment provided by the user or the application.
    """

    def __init__(self, dic: Dict[str, Any]) -> None:
        self.name = dic["name"]
        self.value = dic["value"]
        self.path = dic.get("path")
        self.domain = dic.get("domain")
        self.expires = dic.get("expires")
        self.httpOnly = dic.get("httpOnly")
        self.secure = dic.get("secure")
        self.comment = dic.get("comment")

    def __repr__(self) -> str:
        return f"{self.name}={self.value}"

    def __str__(self) -> str:
        return self.__repr__()


class _Cookies:
    """
    Array [
        name [string] - The name of the cookie.
        value [string] - The cookie value.
        path [string, optional] - The path pertaining to the cookie.
        domain [string, optional] - The host of the cookie.
        expires [string, optional] - Cookie expiration time. (ISO 8601 - YYYY-MM-DDThh:mm:ss.sTZD, e.g. 2009-07-24T19:20:30.123+02:00).
        httpOnly [boolean, optional] - Set to true if the cookie is HTTP only, false otherwise.
        secure [boolean, optional] (new in 1.2) - True if the cookie was transmitted over ssl, false otherwise.
        comment [string, optional] (new in 1.2) - A comment provided by the user or the application.
    ]
    """

    def __init__(self, dics: List[Dict[str, Any]] | None):
        self.empty = False
        if not dics:
            self.empty = True
            return
        self._cookies = [_cookie(i) for i in dics]
        self.cookieDic = {i.name: i.value for i in self._cookies}

    @property
    def cookies(self) -> Dict[str, Any]:
        return cookiejar_from_dict(self.cookieDic)

    def __call__(self) -> Any:
        return cookiejar_from_dict(self.cookieDic)

    # def __setattr__(self, __name: str, __value: Any) -> None:
    #     self.cookieDic[__name] = __value

    # def __getattribute__(self, __name: str) -> Any:
    #     return self.cookieDic[__name]

    def __repr__(self) -> str:
        if not self.empty:
            return "; ".join([str(i) for i in self._cookies])
        else:
            return f"[]"

    def __str__(self) -> str:
        return self.__repr__()


class _header:
    """
    name [string] - The name of the header.
    value [string] - The header value.
    comment [string, optional] (new in 1.2) - A comment provided by the user or the application.
    """

    def __init__(self, dic: Dict[str, Any]) -> None:
        self.name = dic["name"]
        self.value = dic["value"]
        self.comment = dic.get("comment")

    def __repr__(self) -> str:
        return f"{self.name}"

    def __str__(self) -> str:
        return self.__repr__()


class _Headers:
    """
    Array [
        name [string] - The name of the header.
        value [string] - The header value.
        comment [string, optional] (new in 1.2) - A comment provided by the user or the application.
    ]
    """

    def __init__(self, dics: List[Dict[str, Any]] | None):
        self.empty = False
        if not dics:
            self.empty = True
            return
        self.__headersList = [_header(i) for i in dics]
        self.headerDic = {i.name: i.value for i in self.__headersList}

    @property
    def headers(self):
        return CaseInsensitiveDict(self.headerDic)

    def __repr__(self) -> str:
        if not self.empty:
            return "; ".join([f"{i.name}={i.value}" for i in self.__headersList])
        else:
            return "[]"

    def __str__(self) -> str:
        return self.__repr__()

    # def __setattr__(self, __name: str, __value: Any) -> None:
    #     self.headerDic[__name] = __value

    # def __getattribute__(self, __name: str) -> Any:
    #     return self.headerDic[__name]

    def __call__(self) -> Any:
        return CaseInsensitiveDict(self.headerDic)


class _query:
    """
    name [string] - The name of the query.
    value [string] - The query value.
    comment [string, optional] (new in 1.2) - A comment provided by the user or the application."""

    def __init__(self, dic: Dict[str, Any]):
        self.name = dic["name"]
        self.value = dic["value"]
        self.comment = dic.get("comment")

    def __repr__(self) -> str:
        return f"{self.name}={self.value}"


class _Query:
    """
    Array [
        name [string] - The name of the query.
        value [string] - The query value.
        comment [string, optional] (new in 1.2) - A comment provided by the user or the application.
    ]
    """

    def __init__(self, dics: List[Dict[str, Any]] | None):
        self.empty = False
        if not dics:
            self.empty = True
            return
        self.__queryList = [_query(i) for i in dics]
        self.queryDic = {i.name: i.value for i in self.__queryList}

    # def __setattr__(self, __name: str, __value: Any) -> None:
    #     self.queryDic[__name] = __value

    # def __getattribute__(self, __name: str) -> Any:
    #     return self.queryDic[__name]

    def __call__(self) -> Any:
        return urlencode(self.queryDic)

    @property
    def query(self):
        return urlencode(self.queryDic)

    def __repr__(self) -> str:
        if self.empty:
            return f"[]"
        else:
            return f"[{' , '.join([str(i) for i in self.__queryList])}]"

    def __str__(self) -> str:
        return self.query


class _param:
    """
    name [string] - name of a posted parameter.
    value [string, optional] - value of a posted parameter or content of a posted file.
    fileName [string, optional] - name of a posted file.
    contentType [string, optional] - content type of a posted file.
    comment [string, optional] (new in 1.2) - A comment provided by the user or the application.
    """

    def __init__(self, dic: Dict[str, Any] | None) -> None:
        self.empty = False
        if not dic:
            self.empty = True
            return
        self.name = dic.get("name")
        self.value = dic.get("value")
        self.fileName = dic.get("fileName")
        self.contentType = dic.get("contentType")
        self.comment = dic.get("comment")

    def __repr__(self) -> str:
        if not self.empty:
            return f"{self.name}={self.value}"
        else:
            return ""

    def __str__(self) -> str:
        return self.__repr__()


class _Params:
    """
    Array [
        name [string] - name of a posted parameter.
        value [string, optional] - value of a posted parameter or content of a posted file.
        fileName [string, optional] - name of a posted file.
        contentType [string, optional] - content type of a posted file.
        comment [string, optional] (new in 1.2) - A comment provided by the user or the application.
    ]
    """

    def __init__(self, dics: List[Dict[str, Any]] | None) -> None:
        self.empty = False
        if not dics:
            self.empty = True
            return
        self.__paramsList = [_param(i) for i in dics]
        self.paramDic = {i: i for i in self.__paramsList}

    def __call__(self) -> Any:
        return self.paramDic

    def __repr__(self) -> str:
        if not self.empty:
            return f"[{[i for i in self.__paramsList]}]"
        else:
            return "[]"

    def __str__(self) -> str:
        return self.__repr__()


class _PostData:
    """
    mimeType [string] - Mime type of posted data.
    params [array] - List of posted parameters (in case of URL encoded parameters).
    text [string] - Plain text posted data
    comment [string, optional] (new in 1.2) - A comment provided by the user or the application.
    """

    def __init__(self, dic: Dict[str, Any] | None):
        self.empty = False
        if not dic:
            self.empty = True
            return
        self.mimeType = dic.get("mimeType")
        self.text = dic.get("text")
        self.params = _Params(dic.get("params"))
        self.comment = dic.get("comment")

    @property
    def postData(self):
        if self.text:
            # multipart parsing ignored currenlty
            return self.text
        else:
            if not self.params.empty:
                return urlencode(self.params())
            else:
                return ""

    def __call__(self) -> Any:
        if self.text:
            # multipart parsing ignored currenlty
            return self.text
        else:
            if not self.params.empty:
                return urlencode(self.params())
            else:
                return ""

    def __repr__(self) -> str:
        if self.empty:
            return f"Null"
        else:
            return f"{self.postData}"

    def __str__(self) -> str:
        return self.__repr__()


class _Content:
    """
    size [number] - Length of the returned content in bytes. Should be equal to response.bodySize if there is no compression and bigger when the content has been compressed.
    compression [number, optional] - Number of bytes saved. Leave out this field if the information is not available.
    mimeType [string] - MIME type of the response text (value of the Content-Type response header). The charset attribute of the MIME type is included (if available).
    text [string, optional] - Response body sent from the server or loaded from the browser cache. This field is populated with textual content only. The text field is either HTTP decoded text or a encoded (e.g. "base64") representation of the response body. Leave out this field if the information is not available.
    encoding [string, optional] (new in 1.2) - Encoding used for response text field e.g "base64". Leave out this field if the text field is HTTP decoded (decompressed & unchunked), than trans-coded from its original character set into UTF-8.
    comment [string, optional] (new in 1.2) - A comment provided by the user or the application.
    """

    def __init__(self, dic: Dict[str, Any] | None) -> None:
        self.empty = False
        if not dic:
            self.empty = True
            return
        self.size = dic.get("size")
        self.compression = dic.get("compression")
        self.mimeType = dic.get("mimeType")
        self.text = dic.get("text")
        self.content = self.text
        self.comment = dic.get("comment")
        self.encoding = dic.get("encoding")
        self.check()

    def check(self):
        if self.encoding:
            if self.encoding == "base64" and self.text:
                self.content = base64decode(self.text)
                self.__delattr__("text")
            else:
                raise ReferenceError("Could not Find the encoding ", self.encoding)

    def __call__(self, *args: Any, **kwds: Any) -> str | bytes | None:
        return self.content

    def __repr__(self) -> str:
        if not self.empty:
            return f"content = {self.content:.25!r}"
        else:
            return "empty"

    def __str__(self) -> str:
        return self.__repr__()


class _Request:
    """
    method [string] - Request method (GET, POST, ...).
    url [string] - Absolute URL of the request (fragments are not included).
    httpVersion [string] - Request HTTP Version.
    cookies [array] - List of cookie objects.
    headers [array] - List of header objects.
    queryString [array] - List of query parameter objects.
    postData [object, optional] - Posted data info.
    headersSize [number] - Total number of bytes from the start of the HTTP request message until (and including) the double CRLF before the body. Set to -1 if the info is not available.
    bodySize [number] - Size of the request body (POST data payload) in bytes. Set to -1 if the info is not available.
    comment [string, optional] (new in 1.2) - A comment provided by the user or the application.
    """

    def __init__(self, dic: Dict[str, Any] | None):
        self.empty = False
        if not dic:
            self.empty = True
            return
        self.url = dic.get("url", "")
        self.method = dic.get("method")
        self.comment = dic.get("comment")
        self.bodySize = dic.get("bodySize")
        self.headerSize = dic.get("headersSize")
        self.httpVersion = dic.get("httpVersion")
        self._query = _Query(dic.get("queryString"))
        self._cookies = _Cookies(dic.get("cookies"))
        self._headers = _Headers(dic.get("headers"))
        self._postData = _PostData(dic.get("postData"))

        # self.queryString = self.query
        self.headersSize = self.headerSize

    def __repr__(self) -> str:
        if not self.empty:
            return f"Url = {self.url.split('?')[0]}({self.method})"
        else:
            return ""

    def __str__(self) -> str:
        return self.__repr__()

    @property
    def query(self):
        return self._query()

    @property
    def cookies(self):
        return self._cookies()

    @property
    def headers(self):
        return self._headers()

    @property
    def postData(self):
        return self._postData()


class _Response:
    """
    status [number] - Response status.
    statusText [string] - Response status description.
    httpVersion [string] - Response HTTP Version.
    cookies [array] - List of cookie objects.
    headers [array] - List of header objects.
    content [object] - Details about the response body.
    redirectURL [string] - Redirection target URL from the Location response header.
    headersSize [number]* - Total number of bytes from the start of the HTTP response message until (and including) the double CRLF before the body. Set to -1 if the info is not available.
    bodySize [number] - Size of the received response body in bytes. Set to zero in case of responses coming from the cache (304). Set to -1 if the info is not available.
    comment [string, optional] (new in 1.2) - A comment provided by the user or the application.
    """

    def __init__(self, dic: Dict[str, Any] | None):
        self.empty = False
        if not dic:
            self.empty = True
            return
        self.status = dic.get("status", 0)
        self.comment = dic.get("comment")
        self.bodySize = dic.get("bodySize")
        self.statusText = dic.get("statusText")
        self.headerSize = dic.get("headersSize")
        self.httpVersion = dic.get("httpVersion")
        self.redirectUrl = dic.get("redirectURL")
        self._cookies = _Cookies(dic.get("cookies"))
        self._headers = _Headers(dic.get("headers"))
        self._content = _Content(dic.get("content"))

        self.headersSize = self.headerSize
        self.redirectURL = self.redirectUrl

    def __repr__(self) -> str:
        if not self.empty:
            return f"{self.content:.25}"
        else:
            return ""

    def __str__(self) -> str:
        return self.__repr__()

    @property
    def cookies(self):
        return self._cookies()

    @property
    def headers(self):
        return self._headers()

    @property
    def content(self):
        return self._content()


class _Cache:
    """
    beforeRequest [object, optional] - State of a cache entry before the request. Leave out this field if the information is not available.
    afterRequest [object, optional] - State of a cache entry after the request. Leave out this field if the information is not available.
    comment [string, optional] (new in 1.2) - A comment provided by the user or the application.

    ++++++
    Both beforeRequest and afterRequest object share the following structure.
    ++++++

    expires [string, optional] - Expiration time of the cache entry.
    lastAccess [string] - The last time the cache entry was opened.
    eTag [string] - Etag
    hitCount [number] - The number of times the cache entry has been opened.
    comment [string, optional] (new in 1.2) - A comment provided by the user or the application.

    +++++


    """

    def __init__(self, dic: Dict[str, Any] | None):
        self.empty = False
        if not dic:
            self.empty = True
            return

        self.beforeRequest = dic.get("beforeRequest")
        self.afterRequest = dic.get("afterRequest")
        self.comment = dic.get("comment")

        self.before = self.beforeRequest
        self.after = self.afterRequest

    def __repr__(self) -> str:
        if not self.empty:
            return f"[Cache ] {self.before} -> {self.after}"
        else:
            return ""

    def __str__(self) -> str:
        return self.__repr__()


class _Timings:
    """
    blocked [number, optional] - Time spent in a queue waiting for a network connection. Use -1 if the timing does not apply to the current request.
    dns [number, optional] - DNS resolution time. The time required to resolve a host name. Use -1 if the timing does not apply to the current request.
    connect [number, optional] - Time required to create TCP connection. Use -1 if the timing does not apply to the current request.
    send [number] - Time required to send HTTP request to the server.
    wait [number] - Waiting for a response from the server.
    receive [number] - Time required to read entire response from the server (or cache).
    ssl [number, optional] (new in 1.2) - Time required for SSL/TLS negotiation. If this field is defined then the time is also included in the connect field (to ensure backward compatibility with HAR 1.1). Use -1 if the timing does not apply to the current request.
    comment [string, optional] (new in 1.2) - A comment provided by the user or the application.
    """

    def __init__(self, dic: Dict[str, str | int] | None):
        self.empty = False
        if not dic:
            self.empty = True
            return
        self.blocked = int(dic.get("blocked", 0))
        self.dns = int(dic.get("dns", 0))
        self.connect = int(dic.get("connect", 0))
        self.send = int(dic.get("send", 0))
        self.wait = int(dic.get("wait", 0))
        self.receive = int(dic.get("receive", 0))
        self.ssl = int(dic.get("ssl", 0))
        self.comment = int(dic.get("comment", 0))
        self.costumes = parse_costume(dic=dic)
        self.total = self.blocked + self.dns + self.connect + self.send + self.wait + self.receive

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.total

    def __repr__(self) -> str:
        if not self.empty:
            return f"Timming: {self.total}"
        else:
            return "Timming:- ?"

    def __str__(self) -> str:
        return self.__repr__()


class Creator:
    """
    name [string, Required] -  The name of the application that created the log.
    version [string, Required] -  The version number of the application that created the log.
    comment [string, Optional] -  A comment provided by the user or the application.
    """

    def __init__(self, dic: Dict[str, str]) -> None:
        self.name: str = dic["name"]
        self.version: str = dic["version"]
        self.comment: (str | None) = dic.get("comment")
        self.costumes = parse_costume(dic=dic)

    def __repr__(self) -> str:
        return f"{self.name} -V({self.version})"

    def __str__(self) -> str:
        return self.__repr__()


class Browser(Creator):
    """
    name [string, Required] -  The name of the browser that created the log.
    version [string, Required] - The version number of the browser that created the log.
    comment [string, Optional] - A comment provided by the user or the browser.
    """

    def __init__(self, dic: Dict[str, str] | None) -> None:
        self.empty = True
        if dic:
            self.empty = False
            super().__init__(dic)

    def __repr__(self) -> str:
        if not self.empty:
            return f"{self.name} -V({self.version})"
        else:
            return ""

    def __str__(self) -> str:
        return self.__repr__()


class _page:
    """
    startedDateTime [string] - Date and time stamp for the beginning of the page load (ISO 8601 - YYYY-MM-DDThh:mm:ss.sTZD, e.g. 2009-07-24T19:20:30.45+01:00).
    id [string] - Unique identifier of a page within the . Entries use it to refer the parent page.
    title [string] - Page title.
    pageTimings[object] - Detailed timing info about page load.
    comment [string, optional] (new in 1.2) - A comment provided by the user or the application.
    """

    def __init__(self, dic: Dict[str, str | dict] | None) -> None:
        self.empty = True
        if dic:
            self.empty = False
            self.id = dic.get("id")
            self.title = dic.get("title")
            self.started = dic.get("startedDateTime")
            if isinstance(dic["pageTimings"], dict):
                self.pageTimings = dic["pageTimings"]
                self.loadDiff = self.pageTimings.get("onContentLoad", 0) - self.pageTimings.get("onLoad", 0)
                #    milliseconds since page load started
                self.loadtime = self.pageTimings.get("onLoad", -1)
            self.costumes = parse_costume(dic=dic)

    def __repr__(self) -> str:
        if not self.empty:
            return f"Page:- {self.id}"
        else:
            return f"Page:-  ?"

    def __str__(self) -> str:
        return self.__repr__()


class Pages:
    """
    Array [
        startedDateTime [string] - Date and time stamp for the beginning of the page load (ISO 8601 - YYYY-MM-DDThh:mm:ss.sTZD, e.g. 2009-07-24T19:20:30.45+01:00).
        id [string] - Unique identifier of a page within the . Entries use it to refer the parent page.
        title [string] - Page title.
        pageTimings[object] - Detailed timing info about page load.
        comment [string, optional] (new in 1.2) - A comment provided by the user or the application.
        ]
    """

    def __init__(self, dics: List[Dict[str, str | dict] | None]) -> None:
        self.__pageList = [_page(i) for i in dics]
        self.pageDic = {i.id: i for i in self.__pageList}

    # def __getattribute__(self, __name: str) -> Any:
    #     return self.pageDic[__name]

    def __repr__(self) -> str:
        return f"{self.__pageList}"

    def __str__(self) -> str:
        return self.__repr__()

    def __call__(self) -> Any:
        return self.pageDic


class _entry:
    """
    pageref [string, unique, optional] - Reference to the parent page. Leave out this field if the application does not support grouping by pages.
    startedDateTime [string] - Date and time stamp of the request start (ISO 8601 - YYYY-MM-DDThh:mm:ss.sTZD).
    time [number] - Total elapsed time of the request in milliseconds. This is the sum of all timings available in the timings object (i.e. not including -1 values) .
    request [object] - Detailed info about the request.
    response [object] - Detailed info about the response.
    cache [object] - Info about cache usage.
    timings [object] - Detailed timing info about request/response round trip.
    serverIPAddress [string, optional] (new in 1.2) - IP address of the server that was connected (result of DNS resolution).
    connection [string, optional] (new in 1.2) - Unique ID of the parent TCP/IP connection, can be the client port number. Note that a port number doesn't have to be unique identifier in cases where the port is shared for more connections. If the port isn't available for the application, any other unique connection ID can be used instead (e.g. connection index). Leave out this field if the application doesn't support this info.
    comment [string, optional] (new in 1.2) - A comment provided by the user or the application.
    """

    def __init__(self, dic: Dict[str, Union[Dict[str, Any], Any]]):
        self.pageref = dic.get("pageref")
        self.started = dic.get("startedDateTime")
        self.startedDateTime = self.started
        self.comment = dic.get("comment")
        self.timeTaken = dic.get("time")
        self.time = self.timeTaken
        self.request = _Request(dic.get("request"))
        self.response = _Response(dic.get("response"))
        self.cache = _Cache(dic.get("cache"))
        self.timings = _Timings(dic.get("timings"))
        self.serverIp = dic.get("serverIPAddress")
        self.ip = self.serverIp
        self.connection = dic.get("connection")
        self.costumes = parse_costume(dic)

    def __repr__(self) -> str:
        return f" {self.request} "

    def __str__(self) -> str:
        return self.__repr__()


class Entries:
    """
    Array [
        pageref [string, unique, optional] - Reference to the parent page. Leave out this field if the application does not support grouping by pages.
        startedDateTime [string] - Date and time stamp of the request start (ISO 8601 - YYYY-MM-DDThh:mm:ss.sTZD).
        time [number] - Total elapsed time of the request in milliseconds. This is the sum of all timings available in the timings object (i.e. not including -1 values) .
        request [object] - Detailed info about the request.
        response [object] - Detailed info about the response.
        cache [object] - Info about cache usage.
        timings [object] - Detailed timing info about request/response round trip.
        serverIPAddress [string, optional] (new in 1.2) - IP address of the server that was connected (result of DNS resolution).
        connection [string, optional] (new in 1.2) - Unique ID of the parent TCP/IP connection, can be the client port number. Note that a port number doesn't have to be unique identifier in cases where the port is shared for more connections. If the port isn't available for the application, any other unique connection ID can be used instead (e.g. connection index). Leave out this field if the application doesn't support this info.
        comment [string, optional] (new in 1.2) - A comment provided by the user or the application.
    ]
    """

    def __init__(self, dics: List[Dict[str, Union[Dict[str, Any], Any]]]):
        self.entries = [_entry(i) for i in dics]

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.entries

    def __repr__(self) -> str:
        return f"{self.entries}"

    def __str__(self) -> str:
        return self.__repr__()


class Har:
    """

    Examples:-
    >> x = Har("./test.har")
    >> x.version


    version [ string, Required] -  Version number of the format.
    creator [ object, Required] -  An object of type creator that contains the name and version information of the log creator application.
    browser [ object, Optional] -  An object of type browser that contains the name and version information of the user agent.
    pages [ array,  Optional] -  An array of objects of type page, each representing one exported (tracked) page. Leave out this field if the application does not support grouping by pages.
    entries [ array,  Required] -  An array of objects of type entry, each representing one exported (tracked) HTTP request.
    comment [ string, Optional] -  A comment provided by the user or the application.
    """

    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.parse()
        self.clean()

    def parse(self):
        __file_pointer = open(self.filename, "r")
        print(__file_pointer.readable())
        if __file_pointer.readable():
            self.raw_dic = json.load(__file_pointer)
        else:
            self.error(1)
        __file_pointer.close()
        # self.__delattr__("_HAR__file_pointer")

    def error(self, kind):
        match kind:
            case 0:
                raise ValueError("File is empty or not a HAR file")
            case 1:
                raise IOError("Unable to read file ")

    def clean(self):
        __log = self.raw_dic.get("log")
        if not __log:
            self.error(0)
        self.version = __log.get("version")
        self.creator = Creator(__log.get("creator"))
        self.entries = Entries(__log.get("entries"))

        # Optional Headers or Entires
        self.browser = Browser(__log.get("browser", None))
        self.pages = Pages(__log.get("pages", None))
        self.comment = __log.get("comment", None)
        self.costumes = parse_costume(dic=__log)


def parse_costume(dic: Dict[str, Any]) -> Dict[str, Any]:
    return {i: dic[i] for i in dic if i.startswith("_")}


q = exit
