from H2S.h2s import Har

harFile = "./HAR_FILE.har"

x = Har(harFile)
for i in x.entries():
    content = i.response.content
