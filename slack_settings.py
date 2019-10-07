#all the json elements Slack wants

playlist_text = "So, ya wanna make a playlist, eh?"
playlist_attachement = [
                {
                    "blocks": [
                        {
                            "type": "actions",
                            "elements": [
                                {
                                    "type": "button",
                                    "text": {
                                        "type": "plain_text",
                                        "text": ":guitar: Let's go!"
                                        },
                                    "value": "create_playlist",
                                    "action_id":"playlist_button"
                                }
                            ]
                        }
                    ]
                }
            ]

mention_text_list = [
    "Hi, it's a wonderful day to be alive isn't it. How can I help you?",
    "I wonder what this weeks playlist theme will be? What do you think?",
    "Did you know, my first word was 'goose'?",
    "don't worry, i'm not sentient, these are just words someone told me to say....or did they! But that's not the point, how can I be of service?",
    "What's up?",
    "Sup?",
    "Can I help you?"
    ]

