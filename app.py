from flask import Flask,render_template,request,redirect,g,make_response,Response
import requests,os,json,base64,urllib
import bowie3,slack_post

app = Flask(__name__)
app.vars={}

slack_message_token = []
BOT_USER_TOKEN = os.environ['BOT_USER_TOKEN']
CLIENT_SIDE_URL = "http://127.0.0.1"
SERVER_SIDE_URL = "https://slackifybot.herokuapp.com"
PORT = 8080
REDIRECT_URI = "{}/callback/q".format(SERVER_SIDE_URL)
STATE = ""
SHOW_DIALOG_bool = True
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()



@app.route('/',methods=['GET'])
def deftones():
    target = os.environ.get('TARGET', 'World')
    return 'Hello {}!\n'.format(target)



@app.route('/slack',methods=['POST'])
def weezer():
    global CHANNEL_ID
    global slack_message_token
    in_payload = request.get_json()
    CHANNEL_ID = in_payload["event"]["channel"]
    token = in_payload['event']['client_msg_id']

    if token in slack_message_token:
        print("duplicate message recieved")
    else:
        response = bowie3.ziggy(in_payload)
        slack_message_token.append(token)
        slack_post.post(response)

    return make_response("", 200)


@app.route('/slack/actions',methods=['POST'])
def wheatus():
    global playlist_name
    global playlist_theme
    in_payload = json.loads(request.form["payload"])

    if in_payload["type"] == "block_actions":
        trigger_id = in_payload["trigger_id"]

        out_payload = {
        "trigger_id": trigger_id,
        "dialog": {
            "callback_id": "playlist_button",
            "title": "Create a playlist",
            "submit_label": "Create",
            "state": "Limo",
            "elements": [
                {
                    "type": "text",
                    "label": "Playlist name",
                    "name": "playlist_name_input"
                },
                {
                    "type": "text",
                    "label": "What's the theme?",
                    "name": "theme_input"
                }
            ]
        }
        }

        headers = {"Content-type":"application/json;charset=utf-8", "Authorization":"Bearer "+ str(BOT_USER_TOKEN)}
        r = requests.post("https://slack.com/api/dialog.open", headers=headers, data=json.dumps(out_payload))
        return make_response("", 200)

    elif in_payload["type"] == "dialog_submission":
        req = requests.request('GET', in_payload["response_url"])
        playlist_name = in_payload["submission"]["playlist_name_input"]
        playlist_theme = in_payload["submission"]["theme_input"]

        out_payload = {
        "channel": CHANNEL_ID,
        "token": str(BOT_USER_TOKEN),
        "text": "Hey <@" + in_payload["user"]["name"] + ">. I'm creating a playlist called \"" + in_payload["submission"]["playlist_name_input"] + "\"",
        "attachments": [
            {
                "fallback": "Confirm your playlist, ya filthy animal" + auth_url,
                "actions": [
                    {
                        "type": "button",
                        "text": ":musical_note: Confirm",
                        "url": auth_url
                    }
                ]
            }
        ]
        }


        headers = {"Content-type":"application/json;charset=utf-8", "Authorization":"Bearer "+ str(BOT_USER_TOKEN)}
        r = requests.post("https://slack.com/api/chat.postMessage", headers=headers, data=json.dumps(out_payload))
        return make_response("", 200)



@app.route("/test/q")
def testing():
    return "hello daniel"

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))

