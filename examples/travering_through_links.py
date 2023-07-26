from H2S.h2s import Har

harFile = "./HAR_FILE.har"

x = Har(harFile)
pages = x.pages()
requests_list = x.entries()
for i in requests_list:
    print(i.request.url)
    print(i.response.content)
    print(i.request.query)
    print(i.request.url)
