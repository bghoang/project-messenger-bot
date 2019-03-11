import os, sys
from flask import Flask, request
from pymessenger import Bot
import requests
from bs4 import BeautifulSoup as soup
from england import england, UEFA_League
#from fbmessenger.thread_settings import GreetingText, GetStartedButton, MessengerProfile

# Make a flask app
app = Flask(__name__)

PAGE_ACCESS_TOKEN = "EAAfvXa9cYwkBAB4ntbC9Xe0izOFG5ql7XQpVoHG8V5Ba5sQu3dmwKfZAZAmyB3ORIZCX8ZBekQNTBAZAf9jfN8neaAEj00wMYBE69dQaJVpirwEbJKlUGdhyjg5qqK7p4hTwKxsEC6D4oUOWVsgZCZCZBzxuZBcBMRqRjzt2rhvp44wZDZD"
VERIFICATION_TOKEN = "tmp"
bot = Bot(PAGE_ACCESS_TOKEN)
welcome = "Hello this is a messenger bot to check the score for soccer matches, please enter a date to begin (YYYY-MM-DD): "

@app.route('/', methods=['GET'])
# Webhook validation
def verify():
  if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
    if not request.args.get("hub.verify_token") == VERIFICATION_TOKEN:
      return "Verification token mismatch", 403
    return request.args["hub.challenge"], 200
  # This is for the get started button
  headers = {
    'Content-Type': 'application/json',
  }
  data = '{"get_started":{"payload":"GET_STARTED_PAYLOAD"} }'

  response = requests.post('https://graph.facebook.com/v2.6/me/messenger_profile?access_token=EAAfvXa9cYwkBAB4ntbC9Xe0izOFG5ql7XQpVoHG8V5Ba5sQu3dmwKfZAZAmyB3ORIZCX8ZBekQNTBAZAf9jfN8neaAEj00wMYBE69dQaJVpirwEbJKlUGdhyjg5qqK7p4hTwKxsEC6D4oUOWVsgZCZCZBzxuZBcBMRqRjzt2rhvp44wZDZD', headers=headers, data=data)

  return "Success!", 200

@app.route('/', methods=['POST'])
def webhook():
  data = request.get_json()
  log(data)
  # Convert every key to a string, this will contain all the information
  # about the message
  data = dict([(str(k), v) for k, v in data.items()])
  # Check if the message was sent to my page
  if data['object'] == 'page':
    # Get the 'entry' in the message, which is a dictionary
    for entry in data['entry']:
    # For each of the message, get the messaging field
      for messaging_event in entry['messaging']:
        # get the id field in the from the sender field in the dictionary
        sender_id = messaging_event['sender']['id']

        #if messaging_event['postback']['payload'] == "GET_STARTED_PAYLOAD":
          #print (messaging_event['postback']['payload'])
          #bot.send_text_message(sender_id, welcome)

        # Check if the message_event has a field called message
        if messaging_event.get('message'):
            # Check if the message is a text
            if messaging_event['message'].get('text'):
              # Retrieve the message
              response = messaging_event['message']['text']

              # Update matches from England league
              england(bot, sender_id, response)

              #UEFA_League(bot, sender_id, response)

  return 'OK', 200

# Display the data to
def log(message):
    from pprint import pprint
    pprint(message)
    sys.stdout.flush()

# Run the flask app
if __name__ == "__main__":
	app.run()
