from flask import Flask, request
import json

app = Flask(__name__)
user_states = {}

VERIFY_TOKEN = "sandwichtoken"

@app.route("/webhook", methods=["GET"])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    else:
        return "Verification failed", 403

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print("Incoming message:", json.dumps(data, indent=2))

    user_number = data['entry'][0]['changes'][0]['value']['messages'][0]['from']
    msg_text = data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body'].strip().lower()

    step = user_states.get(user_number, "start")

    if step == "start":
        reply = "Welcome to Sandwich Bot! 🥪\nWould you like to order:\n1. Breakfast\n2. Lunch"
        user_states[user_number] = "choose_meal"

    elif step == "choose_meal":
        if msg_text == "1" or msg_text == "2":
            reply = "Choose your bread:\n1. White\n2. Wholegrain\n3. Rye"
            user_states[user_number] = "choose_bread"
        else:
            reply = "Please reply with 1 for Breakfast or 2 for Lunch"

    elif step == "choose_bread":
        reply = "Pick a filling:\n1. Egg\n2. Bacon\n3. Cheese"
        user_states[user_number] = "choose_filling"

    elif step == "choose_filling":
        reply = "Great choice! 🧾 Your sandwich order is received.\nWe’ll contact you soon to confirm delivery."
        user_states[user_number] = "done"

    else:
        reply = "Say 'Hi' to start your order."

    response = {
        "messaging_product": "whatsapp",
        "to": user_number,
        "type": "text",
        "text": {"body": reply}
    }

    return json.dumps(response), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
