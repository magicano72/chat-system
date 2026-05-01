from flask import Flask, request, jsonify
from database import db
from models import Message
from encryption import encrypt_image, decrypt_image
import config
import base64

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# 🔹 create DB
with app.app_context():
    db.create_all()


# ✅ Step 1: verifySessionToken()
def verify_token(token):
    return token == "valid_token"

@app.route('/')
def home():
    return "Chat System Backend Running"

# ✅ UC-04: Send Image
@app.route('/sendMessage', methods=['POST'])
def send_message():
    data = request.json

    session_token = data.get("sessionToken")
    sender_id = data.get("senderID")
    recipient_id = data.get("recipientID")
    text = data.get("text")
    image_base64 = data.get("image")

    # ✅ verifySessionToken
    if not verify_token(session_token):
        return jsonify({"error": "Invalid session"}), 401

    # ❗ لازم يكون فيه text أو image
    if not text and not image_base64:
        return jsonify({"error": "Text or Image is required"}), 400

    image_encrypted = None

    # ✅ لو فيه صورة
    if image_base64:
        import base64
        image_bytes = base64.b64decode(image_base64)
        image_encrypted = encrypt_image(image_bytes, config.SECRET_KEY)

    # ✅ store message
    msg = Message(
        sender_id=sender_id,
        recipient_id=recipient_id,
        text=text,
        image_data=image_encrypted
    )

    db.session.add(msg)
    db.session.commit()

    print(f"[Push] Message {msg.id} sent")

    return jsonify({
        "messageID": msg.id,
        "status": "sent"
    })

# ✅ Receive Image (PC side)
@app.route('/receiveMessage/<int:message_id>', methods=['GET'])
def receive_message(message_id):
    msg = Message.query.get(message_id)

    if not msg:
        return jsonify({"error": "Not found"}), 404

    return jsonify({
        "sender": msg.sender_id,
        "text": msg.text,
        "status": msg.status
    })


# ✅ ACK
@app.route('/ack', methods=['POST'])
def ack():
    data = request.json
    message_id = data.get("messageID")

    msg = Message.query.get(message_id)
    if msg:
        msg.status = "delivered"
        db.session.commit()

    return jsonify({"status": "delivered"})


if __name__ == "__main__":
    app.run(debug=True)