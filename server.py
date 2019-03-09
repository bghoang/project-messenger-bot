import os, sys
from mbdb import MBDataBase
from flask import Flask, request
from pymessenger import Bot
from time import time
import requests
from bs4 import BeautifulSoup as soup
import sys
#Make the Flask app

app = Flask(__name__)

db = MBDataBase()

PAGE_ACCESS_TOKEN = "EAAHuL8qSgV4BAP0lavgFCt2yHqHZAbcm2YTAiPjYCVZBdilNaY94ZCjiPHJchj9zI0Va5qApGEuBR06wia9vQp8lPZBVuVust1RfUZBy0QAGQGm3daggm34AtttgTOesXGEi3USJG6ZAOUtlPXb1HqCXXoKcwS1vWOec19RcZCDNAZDZD"
bot = Bot(PAGE_ACCESS_TOKEN)
VERIFICATION_TOKEN = "chicken123"

@app.route('/', methods=['GET'])
# Webhook validation
def verify():
	if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
		if not request.args.get("hub.verify_token") == VERIFICATION_TOKEN:
			return "Verification token mismatch", 403
		return request.args["hub.challenge"], 200
	return "Success!", 200

# Everytime the bot recieve a message, this function is called
@app.route('/', methods=['POST'])
def webhook():
    welcome ="Welcome! Please enter a date"
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

          # Check if the message_event has a field called message
          if messaging_event.get('message'):
            # Get the text value from the message fieldx
            '''if messaging_event['message'].get('attachments'):
              # Echo picture
              if messaging_event['message']['attachments'][0]['type'] == "image":
                # Get the payload content which is in the first index of the messaging_event['message']['attachments'] list
                payload = messaging_event['message']['attachments'][0]['payload']
                # Get the url link from the payload dict
                url = payload['url']
                bot.send_image_url(sender_id, url)
              # Send button with link
              if messaging_event['message']['attachments'][0]['type'] == "fallback":
                url = messaging_event['message']['attachments'][0]['url']

                url_button=[
                  {
                    "type": "web_url",
                    "url": url,
                    "title": "<BUTTON>"
                  }
                ]
                bot.send_button_message(sender_id, "Click the button to go to the link", url_button)
            # Echo bot
            elif messaging_event['message'].get('text'):
              # Retrieve the message
              response = messaging_event['message']['text']
              # Echo the message
              bot.send_text_message(sender_id, response)
            '''
            # Match status
            if messaging_event['message'].get('text'):
              # Retrieve the message
              response = messaging_event['message']['text']

              #Getting data from the web              
              my_url = 'https://www.goal.com/en-us/premier-league/fixtures-results/' + response + '/2kwbbcootiqqgmrzs6o5inle5'

              # Grab the data from the url page
              data = requests.get(my_url)
              print(data.status_code)
              # Check if the website exist
              if data.status_code != 200:
                bot.send_text_message(sender_id,"There are no matches on this date")
              # Turn this into html raw data
              raw_data = soup(data.content, "html.parser")

              # Get the result of all the teams
              teams = raw_data.findAll("div",attrs={"class":"match-data"})

              # Get the match status
              match_status = raw_data.findAll("span",attrs={"data-bind":"state"})

#print (match_status[0].text)
              # Loop through each team and get the data
              for i in range(len(teams)):
                # Get the list of all the teams
                teamName = teams[i].findAll("span",attrs={"class":"team-name"})
                # Get the goals
                goals = teams[i].findAll("span",attrs={"class":"goals"})
                # Organize all the teams in pairs
                status = match_status[i].text
                result =""
                for j in range(len(teamName)):
                # Print in this format
                  result += teamName[j].text +" "+ goals[j].text + " "
                  #print(result, end=" "),
                  # Go to next line for each pair
                  if j % 2 == 1:
                    result = status + " " + result
                    bot.send_text_message(sender_id, result)
                    #print(result)
                    #print("\n")

              # Echo the message
                  #bot.send_text_message(sender_id, welcome)

            # Get last message, print the time and message to the database
            '''if db.get_user(sender_id) == False:
                user ={}
                user["Last message time"] = time()
                user["message"] = []
                db.create_user(sender_id, user)
            user = db.get_user(sender_id)
            user["Last message time"] = time()
            user["message"].append(messaging_event['message']['text'])
            db.update_user(sender_id, user)
            print(db)
            '''
    return 'OK', 200

# Display the data to
def log(message):
    from pprint import pprint
    pprint(message)
    sys.stdout.flush()

#Run the app (put at bottom)
if __name__ == "__main__":
	app.run()
