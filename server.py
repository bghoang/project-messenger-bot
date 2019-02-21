import os, sys
from mbdb import MBDataBase
from flask import Flask, request
from pymessenger import Bot
from time import time 
#Make the Flask app

app = Flask(__name__)

db = MBDataBase()

PAGE_ACCESS_TOKEN = "EAAHuL8qSgV4BANhmwjnD9ZBpwkTu88K0ZAkKHy3Ltzz7nYZButOQm39NZB5qZAHF2r5998vAuKjjOLC0gSmou8VY7EdVVmA3uIheXDFvJIz8poDjtcBnfDo44SyK4mwlYQF3noNOdGZCx6J8xNwyiGIAvhePQScklGRJZBcOj0ncwZDZD"
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
    # Convert every key to a string
    data = dict([(str(k), v) for k, v in data.items()])
    # Check if the message was sent to my page
    if data['object'] == 'page':
      # Get the 'entry' in the message
      for entry in data['entry']:
        for messaging_event in entry['messaging']:
          sender_id = messaging_event['sender']['id']
                
          # Echo Bot
          if messaging_event.get('message'):
            if messaging_event['message'].get('text'):
              # Retrieve the message
              response = messaging_event['message']['text']
              # Echo the message
              bot.send_text_message(sender_id, response)
 
            # Get last message, print the time and message to the database
            if db.get_user(sender_id) == False:
                user ={}
                user["Last message time"] = time()
                user["message"] = []
                db.create_user(sender_id, user)
            user = db.get_user(sender_id) 
            user["Last message time"] = time()
            user["message"].append(messaging_event['message']['text'])           
            db.update_user(sender_id, user)
            print(db)
            
    return 'OK', 200

# Display the data to 
def log(message):
    from pprint import pprint
    pprint(message)
    sys.stdout.flush()
    
#Run the app (put at bottom)
if __name__ == "__main__":
	app.run()
