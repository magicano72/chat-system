# ─────────────────────────────────────────────────────────
# File: auth.py  –  User Login for Android-PC Chat System
# Backend: Python / Flask
# ─────────────────────────────────────────────────────────

import uuid
import bcrypt
from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import sqlite3

app = Flask(__name__)
DB_PATH = "chatapp.db"
SESSION_EXPIRY_HOURS = 24


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ── REGISTER ──────────────────────────────────────────────
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    user_id  = data.get("userID", "").strip()
    password = data.get("password", "").strip()

    if not user_id or not password:
        return jsonify({"error": "Fields cannot be blank"}), 400

    db = get_db()

    # Check if user already exists
    existing = db.execute(
        "SELECT userID FROM users WHERE userID = ?", (user_id,)
    ).fetchone()

    if existing:
        return jsonify({"error": "User ID already taken"}), 409

    # Hash password with BCrypt (cost factor 12)
    hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(12))

    db.execute(
        "INSERT INTO users (userID, passwordHash, createdAt) VALUES (?, ?, ?)",
        (user_id, hashed_pw, datetime.utcnow().isoformat())
    )
    db.commit()
    return jsonify({"message": "Registration successful"}), 201


# ── LOGIN ─────────────────────────────────────────────────
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user_id  = data.get("userID", "").strip()
    password = data.get("password", "").strip()

    # Step 1: Validate input
    if not user_id or not password:
        return jsonify({"error": "Fields cannot be blank"}), 400

    db = get_db()

    # Step 2: Lookup user in database
    user = db.execute(
        "SELECT userID, passwordHash, displayName FROM users WHERE userID = ?",
        (user_id,)
    ).fetchone()

    if user is None:
        # Generic message to prevent user enumeration
        return jsonify({"error": "Invalid credentials"}), 401

    # Step 3: Verify password against BCrypt hash
    stored_hash = user["passwordHash"]
    password_match = bcrypt.checkpw(password.encode("utf-8"), stored_hash)

    if not password_match:
        return jsonify({"error": "Invalid credentials"}), 401

    # Step 4: Generate session token
    session_token = str(uuid.uuid4())
    expiry = datetime.utcnow() + timedelta(hours=SESSION_EXPIRY_HOURS)

    db.execute(
        "INSERT INTO sessions (sessionToken, userID, expiresAt) VALUES (?, ?, ?)",
        (session_token, user_id, expiry.isoformat())
    )
    db.commit()

    # Step 5: Return success response
    return jsonify({
        "sessionToken":  session_token,
        "userID":        user["userID"],
        "displayName":   user["displayName"],
        "expiresAt":     expiry.isoformat()
    }), 200


# ── TOKEN VALIDATION HELPER ───────────────────────────────
def validate_token(session_token: str) -> dict | None:
    """Returns the user record if token is valid and unexpired, else None."""
    db = get_db()
    session = db.execute(
        "SELECT userID, expiresAt FROM sessions WHERE sessionToken = ?",
        (session_token,)
    ).fetchone()

    if session is None:
        return None

    if datetime.utcnow() > datetime.fromisoformat(session["expiresAt"]):
        return None   # Token expired

    return {"userID": session["userID"]}


if __name__ == "__main__":
    app.run(debug=True, port=5000)