import requests

ACCESS_TOKEN = "YOUR_WHATSAPP_TOKEN"
PHONE_NUMBER_ID = "YOUR_PHONE_NUMBER_ID"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print("Incoming message:", json.dumps(data, indent=2))

    # Safety check
    if "messages" not in data["entry"][0]["changes"][0]["value"]:
        return "ok", 200

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

    # SEND MESSAGE TO WHATSAPP API
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": user_number,
        "type": "text",
        "text": {"body": reply}
    }
    r = requests.post(url, headers=headers, json=payload)
    print("Message sent:", r.status_code, r.text)

    return "ok", 200
