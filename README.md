# H2S
HAR(http archive) to Scraper. Simple HAR file extractor that analyzes the provided HAR file for posisble secutir breaches and automations.

# What is does?
    > Analyze HAR file and produce beautiful data
    > Analyze for automation possiblility. And gives a basic python code to automate
    > Analyze for any Security VLUN if possible.

# What it doesnot ~do~?
    > Produce a readymade scraper that you can sell in dark market
    > List of all securty vlun's that you can use to hack/bounty upon
    > Make You Coffee

# How to use:-
    > pip installl H2S
    > Follow the examples in example directory
    ```python
        from H2S import h2s
        x = h2s.Har("MyHarFile.har")
        pages = x.pages()
        requests_list = x.entries()
        for i in requests_list:
            print(i.request.url)
            print(i.response.content)
            print(i.request.query)
            print(i.request.url)
            ....
    ```
    