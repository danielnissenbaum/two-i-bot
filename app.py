from flask import Flask,render_template,request,redirect,g,make_response,Response
import requests,os,json,base64,urllib
import slack_response_logic,slack_post

#set up app/server variables

app = Flask(__name__)
app.vars={}

slack_message_token = []
BOT_USER_TOKEN = os.environ.get('BOT_USER_TOKEN')
CLIENT_SIDE_URL = "http://127.0.0.1"
SERVER_SIDE_URL = "https://two-i-bot.herokuapp.com"
PORT = 8080
REDIRECT_URI = "{}/callback/q".format(SERVER_SIDE_URL)
STATE = ""
SHOW_DIALOG_bool = True
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()

#message to display if someone GETs our URL

@app.route('/',methods=['GET'])
def you_got_me():
    target = os.environ.get('TARGET', 'World')
    return 'Hello {}!\n'.format(target)

#if we receive a URL verification 'challenge' from slack

@app.route('/slack/challenge',methods=['POST'])
def challenge():
    in_payload = request.get_json()
    challenge = in_payload["challenge"]
    print(challenge)
    url = ""
    headers = {"Content-type":"application/json;charset=utf-8", "Authorization":"Bearer "+ str(BOT_USER_TOKEN)}
    r = requests.post("https://slack.com/api/events", headers=headers, data={"challenge":challenge)

    return make_response("", 200)

#if we receive a message POST from slack

@app.route('/slack',methods=['POST'])
def message_from_slack():
    global CHANNEL_ID
    global slack_message_token
    in_payload = request.get_json()
    CHANNEL_ID = in_payload["event"]["channel"]
    token = in_payload['event']['client_msg_id']

    if token in slack_message_token:
        print("duplicate message recieved")
    else:
        response = slack_response_logic.logic(in_payload)
        slack_message_token.append(token)
        slack_post.post(response)

    return make_response("", 200)

#if we receive a POST from slack about a user action, eg a button press

@app.route('/slack/actions',methods=['POST'])
def action_from_slack():

    in_payload = json.loads(request.form["payload"])

    #if the user pressed a button we can create a dialog box

    if in_payload["type"] == "block_actions":
        trigger_id = in_payload["trigger_id"]

        out_payload = {
        "trigger_id": trigger_id,
        "dialog": {
            "callback_id": "MAKE AN ID",
            "title": "TITLE OF DIALOG BOX",
            "submit_label": "TEXT THAT GOES ON SUBMIT BUTTON",
            "state": "Limo",
            "elements": [
                {
                    "type": "text",
                    "label": "LABEL THE USER SEES FOR TEXT ENTRY",
                    "name": "VARIABLE NAME FOR TEXT ENTRY"
                },
                {
                    "type": "text",
                    "label": "LABEL THE USER SEES FOR TEXT ENTRY 2",
                    "name": "VARIABLE NAME FOR TEXT ENTRY 2"
                }
            ]
        }
        }

        headers = {"Content-type":"application/json;charset=utf-8", "Authorization":"Bearer "+ str(BOT_USER_TOKEN)}
        r = requests.post("https://slack.com/api/dialog.open", headers=headers, data=json.dumps(out_payload))
        return make_response("", 200)

        #if the user submitted a dialog box

    elif in_payload["type"] == "dialog_submission":
        req = requests.request('GET', in_payload["response_url"])


        out_payload = {
        "channel": CHANNEL_ID,
        "token": str(BOT_USER_TOKEN),
        "text": "SAY SOMETHIN",
        "attachments": [
            {
                "fallback": "Confirm your playlist, ya filthy animal" + auth_url,
                "actions": [
                    {
                        "type": "button",
                        "text": "BUTTON TEXT",
                        "url": auth_url
                    }
                ]
            }
        ]
        }


        headers = {"Content-type":"application/json;charset=utf-8", "Authorization":"Bearer "+ str(BOT_USER_TOKEN)}
        r = requests.post("https://slack.com/api/chat.postMessage", headers=headers, data=json.dumps(out_payload))
        return make_response("", 200)



@app.route("/redirect")
def testing():
    return "hello daniel"

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
