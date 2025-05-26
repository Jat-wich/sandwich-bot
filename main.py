
# main.py
import os
import requests
from flask import Flask, request
from models import Session, Order

app = Flask(__name__)

VERIFY_TOKEN = "test"
WHATSAPP_TOKEN = os.getenv("EAAsbZAJMBnzABO1GVHXheG2jiZAZAkXZCZBLexvsNGk3cqvc9KkCYEkZCPqZCVpN2oWShkERt9ZAPRT5vTHdc5adPT4fjxRcnExXTbSqRIGT2ZCYy0uKMKoHxCZCG4V5g6JX9DdEsdJQgCC64fFYvMPjEJG4wn3iAdCtjfEHd9NJ2gA1UFSB7moLWkIBX9idxejHT3JzPNpfD8YyMX5FhOzwz0CqPdk4B22HoZD")
WHATSAPP_PHONE_ID = os.getenv("687958281065917")

user_states = {}

@app.route("/")
def home():
    return "Sandwich Bot is live!"

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        return "Invalid verify token", 403

    data = request.get_json()
    try:
        entry = data["entry"][0]
        changes = entry["changes"][0]
        value = changes["value"]
        messages = value.get("messages")
        if messages:
            message = messages[0]
            user_number = message["from"]
            msg_text = message["text"]["body"].strip().lower()

            reply = handle_message(user_number, msg_text)
            send_reply(user_number, reply)
    except Exception as e:
        print("Error handling message:", e)
    return "ok", 200

def handle_message(user_number, msg_text):
    step = user_states.get(user_number, "start")

    if step == "start":
        session = Session()
        last_order = session.query(Order).filter_by(user_number=user_number).order_by(Order.id.desc()).first()
        session.close()

        if last_order:
            user_states[user_number] = "repeat_or_change"
            return f"Welcome back! 🥪 Last time you ordered:\nBread: {last_order.bread}\nFilling: {last_order.filling}\n\nReply 'same' to repeat or 'change' to start a new one."
        else:
            user_states[user_number] = "choose_meal"
            return "Welcome to Sandwich Bot! 🥪\nWould you like to order:\n1. Breakfast\n2. Lunch"

    elif step == "repeat_or_change":
        if msg_text == "same":
            return "👍 Your last order will be repeated today!"
        elif msg_text == "change":
            user_states[user_number] = "choose_meal"
            return "Would you like to order:\n1. Breakfast\n2. Lunch"
        else:
            return "Please type 'same' to repeat or 'change' to create a new order."

    elif step == "choose_meal":
        if msg_text in ["1", "breakfast"]:
            user_states[user_number] = "choose_bread"
            return "Great! Choose your bread:\n1. White\n2. Wheat\n3. Multigrain"
        elif msg_text in ["2", "lunch"]:
            user_states[user_number] = "choose_bread"
            return "Great! Choose your bread:\n1. Baguette\n2. Sourdough\n3. Rye"
        else:
            return "Please choose 1 for Breakfast or 2 for Lunch."

    elif step == "choose_bread":
        user_states[user_number + "_bread"] = msg_text
        user_states[user_number] = "choose_filling"
        return "Yum! Now choose your filling:\n1. Egg\n2. Chicken\n3. Veggie Delight"

    elif step == "choose_filling":
        bread = user_states.get(user_number + "_bread", "Unknown")
        filling = msg_text

        session = Session()
        order = Order(user_number=user_number, bread=bread, filling=filling)
        session.add(order)
        session.commit()
        session.close()

        user_states[user_number] = "done"
        return f"Thanks! 🧾 Your sandwich with {bread} bread and {filling} filling is confirmed."

    else:
        return "Type 'start' to start your sandwich order 🍞."

def send_reply(phone_number, message):
    url = f"https://graph.facebook.com/v19.0/{WHATSAPP_PHONE_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "text",
        "text": {"body": message}
    }
    response = requests.post(url, headers=headers, json=data)
    print("Sent:", response.status_code, response.text)

if __name__ == "__main__":
    app.run(debug=True)
