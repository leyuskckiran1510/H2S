
# Scraper Outline
```
ConAnalyzer [h2s._Content -> parser_object ] :- Takes a content object from HAR.entries.reponse.content ; and does a 
        pattren or text based ( fuzzy ) mattching to  filter the only potential content and entries

ReqAnalyzer [h2s._Request -> requests_sequence ]:- It takes a requests object from Har.Entries.request; and tries to formulate the proper
            requests sequence and returns requests_sequence;

ResAnalyzer [h2s._entry -> [parser_object|None ,requests_sequence|None]] :- It takes the entry object and performs necessary 
            analysis to either call the ConAnalyzer and ReqAnalyzer to formulate parser_object and requests_sequence otherwise 
            reject the entry .

Parser_Object [__response[str,bytes] -> Json[int,str]] :- It is a bs4 bundel  as a object for which you can toggle certain, function
        sequence and response sequence , It has three state:-
        i) Dead :- In this state it is just a non functioning bs4 bundel
        ii) Alive :- This is a state after it's purpose is defined (in our case ConAnalyzer will define it's purpose)
        iii)Working :- This is final state now it takes __response or text as bytes|str and does the parsing and returns 
                    the json {index : value}, which the author/coder and look and select the index/key they like in their code
                    and discard other

Requests_Sequence [requests.Requests | Url[str] |urllib.request  -> __response[str,bytes]] :- It is a bundel of requests/http.client
        [one will be choosed for now assume requests moduel ] as a obkect from which we can topggle certain functions/features
        ,It also has same three state:-
        i) Dead :- initial state just a class blueprint
        ii) Alive :- In this state it's purpose is defined and the url it has to follow is also define
                    with necessary cookies/session , headers and queries format and vraibales (used by ReqAnalyzer)
        iii) Working state:- This is a final state that the coder/author use to perform necessary requests and retrice data.
```