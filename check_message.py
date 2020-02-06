from flask import make_response
import googlesheets_send,re

def check(payload):

    message = payload["event"]["text"]
    if bool(re.search('(?:docs.google.com)', payload["event"]["text"])):
        googlesheets_send.send(payload)
        #print("GOOGLE DOCCCCCCCAAAAAAA")
    else:
        print("IT IS NO GOOGLE")
    return make_response("", 200)
