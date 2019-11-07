from googlesheets-send import send

def check(payload):

    message = payload["event"]["text"]
    if bool(re.search('(?:docs.google.com', payload["event"]["text"])):
        send(payload)
return
