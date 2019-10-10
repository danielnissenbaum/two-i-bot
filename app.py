from flask import Flask,render_template,request,redirect,g,make_response,Response
import requests,os,json,base64,urllib
import bowie3,slack_post

app = Flask(__name__)
app.vars={}
slack_message_token = []

# Spotify Client Keys
CLIENT_ID = os.environ['SP_CLIENT_ID']
CLIENT_SECRET = os.environ['SP_CLIENT_SECRET']
BOT_USER_TOKEN = os.environ['BOT_USER_TOKEN']

# Spotify URLS
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)

# Server-side Parameters
CLIENT_SIDE_URL = "http://127.0.0.1"
SERVER_SIDE_URL = "https://slackifybot.herokuapp.com"
PORT = 8080
REDIRECT_URI = "{}/callback/q".format(SERVER_SIDE_URL)
SCOPE = "playlist-modify-public playlist-modify-private playlist-read-private playlist-read-collaborative"
STATE = ""
SHOW_DIALOG_bool = True
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()

auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    "client_id": CLIENT_ID
}


url_args = "&".join(["{}={}".format(key,urllib.parse.quote(val)) for key,val in auth_query_parameters.items()])
auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)

playlist_data = {}
playlist_name = "holder"
playlist_theme = "noddy"

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

@app.route("/callback/q")
def callback():
    global playlist_data
    global access_token
    # Auth Step 4: Requests refresh and access tokens
    auth_token = request.args['code']
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": REDIRECT_URI
    }
    data = "{}:{}".format(CLIENT_ID, CLIENT_SECRET)
    base64encoded = base64.b64encode(data.encode())
    headers = {"Authorization": "Basic {}".format(base64encoded.decode())}
    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload, headers=headers)

    # Auth Step 5: Tokens are Returned to Application
    response_data = json.loads(post_request.text)
    access_token = response_data["access_token"]
    refresh_token = response_data["refresh_token"]
    token_type = response_data["token_type"]
    expires_in = response_data["expires_in"]

    # Auth Step 6: Use the access token to access Spotify API
    authorization_header = {"Authorization":"Bearer {}".format(access_token)}
    authorization_header["Content-Type"] = "application/json"
    data = {}

    data["name"] = "#music " + playlist_name
    data["description"] = playlist_theme
    data["collaborative"] = True
    data["public"] = False
    payload = json.dumps(data)

    user_profile_api_endpoint = "{}/me".format(SPOTIFY_API_URL)
    profile_response = requests.get(user_profile_api_endpoint, headers=authorization_header)
    profile_data = json.loads(profile_response.text)

    playlist_api_endpoint = "{}/playlists".format(profile_data["href"])
    playlists_response = requests.post(playlist_api_endpoint, headers=authorization_header, data=payload)
    playlist_data = playlists_response.json()
    playlist_url = playlist_data["external_urls"]["spotify"]

    writedata.writer(playlist_data,loc)

    slack_response = {"text":"","attachments":""}
    slack_response["text"] = "I've made a playlist called \"" + playlist_name + "\". The theme is \"" + playlist_theme + "\"\n\nHere's the link: " + playlist_url
    slack_post.post(slack_response)

    return "All done. I've posted the link to the playlist in the #music channel. You can close this window now."

@app.route("/test/q")
def testing():
    return "hello daniel"

if __name__ == "__main__":
    app.run()

############################



@app.route('/')
def hello_world():
    target = os.environ.get('TARGET', 'World')
    return 'Hello {}!\n'.format(target)

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
