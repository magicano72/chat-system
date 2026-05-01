# 📱 Android-PC Chatting & Image Sharing System

## 🎯 Implemented Use Cases

* UC-03: Send Text Message
* UC-04: Send Image
* UC-05: Receive Message
* UC-06: Acknowledge Delivery

---

# 🔁 Sequence Diagram → Implementation Mapping

## 📌 UC-04: Send Image (Mobile → PC)

### Flow:

1. Mobile → `POST /sendMessage`
2. Backend:

   * Verify session token
   * Encrypt image
   * Store in database
   * Send notification (simulated)
3. PC → `GET /receiveMessage/{id}`
4. Backend:

   * Decrypt image
   * Return data
5. PC → `POST /ack`

---

## 📌 UC-03: Send Text Message

### Flow:

1. Mobile → `POST /sendMessage`
2. Backend:

   * Verify session token
   * Store text message
3. PC → `GET /receiveMessage/{id}`
4. PC → `POST /ack`

---

# 🌐 API Endpoints

## 🔹 1. Send Message (Text / Image)

**POST** `/sendMessage`

### Request Body:

```json
{
  "sessionToken": "valid_token",
  "senderID": "user1",
  "recipientID": "user2",
  "text": "Hello",
  "image": "BASE64_IMAGE"
}
```

### Rules:

* At least one of `text` or `image` is required

### Response:

```json
{
  "messageID": 1,
  "status": "sent"
}
```

---

## 🔹 2. Receive Message

**GET** `/receiveMessage/{message_id}`

### Response:

```json
{
  "sender": "user1",
  "text": "Hello",
  "image": "BASE64_IMAGE",
  "status": "sent"
}
```

---

## 🔹 3. Acknowledge Message

**POST** `/ack`

### Request:

```json
{
  "messageID": 1
}
```

### Response:

```json
{
  "status": "delivered"
}
```

---

# 🗄️ Database Schema

## Message Table

| Column       | Type     |
| ------------ | -------- |
| id           | Integer  |
| sender_id    | String   |
| recipient_id | String   |
| text         | Text     |
| image_data   | Binary   |
| timestamp    | DateTime |
| status       | String   |

---

# 🧪 Test Cases

## ✅ TC-01: Send Text Message

**Input:**

```json
{
  "sessionToken": "valid_token",
  "senderID": "user1",
  "recipientID": "user2",
  "text": "Hello"
}
```

**Expected:**

* Status: 200
* messageID returned
* status = sent

---

## ✅ TC-02: Send Image

**Input:**

```json
{
  "sessionToken": "valid_token",
  "senderID": "user1",
  "recipientID": "user2",
  "image": "BASE64_IMAGE"
}
```

**Expected:**

* Image encrypted and stored
* messageID returned

---

## ❌ TC-03: Invalid Token

**Input:**

```json
{
  "sessionToken": "wrong",
  "senderID": "user1",
  "recipientID": "user2",
  "text": "Hello"
}
```

**Expected:**

* 401 Unauthorized

---

## ❌ TC-04: Empty Message

**Input:**

```json
{
  "sessionToken": "valid_token",
  "senderID": "user1",
  "recipientID": "user2"
}
```

**Expected:**

* 400 Error
* "Text or Image is required"

---

## ✅ TC-05: Receive Message

**Request:**

```
GET /receiveMessage/1
```

**Expected:**

* Returns message content (text/image)

---

## ❌ TC-06: Invalid Message ID

**Request:**

```
GET /receiveMessage/999
```

**Expected:**

* 404 Not Found

---

## ✅ TC-07: ACK Message

**Input:**

```json
{
  "messageID": 1
}
```

**Expected:**

* status = delivered

---

# ▶️ Running Instructions

## 1. Install Dependencies

```bash
pip install -r requirements.txt
```

## 2. Run Server

```bash
python app.py
```

## 3. Test Using Postman

* Use endpoints above
* Send JSON requests

---

# 🔐 Security

* Images are encrypted using AES-based encryption
* Session token validation is applied

---

# 📌 Notes

* System supports:

  * Text messages
  * Image messages
* Platform independent (Mobile + PC)
* No group chat (as per requirements)

---

# 🚀 Conclusion

The system successfully implements:

* Secure image sharing
* Text messaging
* Cross-platform communication
* End-to-end flow matching sequence diagrams

---
