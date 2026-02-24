import os
from flask import Flask, request
from dotenv import load_dotenv
import time

load_dotenv()

app = Flask(__name__)

ADMIN_NUMBER = os.getenv("ADMIN_NUMBER")

AUTHORIZED_NUMBERS = [ADMIN_NUMBER]
recent_messages = {}
message_times = {}

# Anti-spam intelligent
def anti_spam(sender, message):
    now = time.time()

    # Bloque message identique
    if sender in recent_messages and recent_messages[sender] == message:
        return False

    # Bloque si messages trop rapides (<3 sec)
    if sender in message_times and now - message_times[sender] < 3:
        return False

    recent_messages[sender] = message
    message_times[sender] = now
    return True


@app.route("/")
def home():
    return "Bot actif 24h/24 🚀"


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    sender = data.get("from")
    message = data.get("body")

    if not anti_spam(sender, message):
        return "Spam détecté", 400

    # Commandes ADMIN
    if sender in AUTHORIZED_NUMBERS:
        if message.lower() == "ping":
            return "Pong ✅", 200

        if message.lower() == "info":
            return "Bot opérationnel 24h/24 🔥", 200

    return "Message reçu", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)