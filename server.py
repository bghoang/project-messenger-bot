import os, sys
from mbdb import MBDataBase
from flask import Flask, request
from pymessenger import Bot
from time import time 
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
    data = request.get_json()
    log(data)
    # Convert every key to a string, this will contain all the information 
    # about the message 
    data = dict([(str(k), v) for k, v in data.items()])
    #print("This is the data", data)
    # Check if the message was sent to my page
    if data['object'] == 'page':
      # Get the 'entry' in the message, which is a dictionary
      for entry in data['entry']:
        # For each of the message, get the messaging field
        for messaging_event in entry['messaging']:
          # get the id field in the from the sender field in the dictionary
          sender_id = messaging_event['sender']['id']
            
          '''               Echo Bot                      '''
          # Check if the message_event has a field called message
          if messaging_event.get('message'):
            # Get the text value from the message fieldx
            if messaging_event['message'].get('attachments'):
              print("this might be a link")
              break
            elif messaging_event['message'].get('text'):
              #if messaging_event['message']['attachments'][0]['type'] == "fallback":
                #print("this is a link")

              #else:
                # Retrieve the message
              response = messaging_event['message']['text']
                # Echo the message
              bot.send_text_message(sender_id, response)
                
              
              '''
              url_button=[
                {
                  "type": "web_url",
                  "url": "<URL_TO_OPEN_IN_WEBVIEW>",
                  "title": "<BUTTON_TEXT>",
                }
              ]
              '''
              
            '''             Echo a picture back           '''
            if messaging_event['message'].get('attachments'):
              if messaging_event['message']['attachments'][0]['type'] == "image":
                # Get the payload content which is in the first index of the messaging_event['message']['attachments'] list 
                payload = messaging_event['message']['attachments'][0]['payload']
                # Get the url link from the payload dict
                url = payload['url']
                bot.send_image_url(sender_id, url) 
                
              else: 
                print("it is not an image")
                
              #print("this is the payload content in messaging:", messaging_event['message']['attachments'][0]['type'])
            
    
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
