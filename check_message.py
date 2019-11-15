import googlesheets_send

def check(payload):

    message = payload["event"]["text"]
    if bool(re.search('(?:docs.google.com', payload["event"]["text"])):
        #send(payload)
        print("GOOGLE DOCCCCCCCAAAAAAA")
    else:
        print("IT IS NO GOOGLE")
    return
