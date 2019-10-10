#all the json elements Slack wants

call_to_action_text = "CALL THOSE MOTHERS TO ACTION"
call_to_action_attachement = [
                {
                    "blocks": [
                        {
                            "type": "actions",
                            "elements": [
                                {
                                    "type": "button",
                                    "text": {
                                        "type": "plain_text",
                                        "text": "TEXT ON THE BUTTON"
                                        },
                                    "value": "BUTTON VARIABLE NAME",
                                    "action_id":"BUTTON ID"
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
    "Can I help you?",
    "GENERIC_BOT_RESPONSE.TXT"
    ]
