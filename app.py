import sqlite3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, jsonify, render_template, request

app = Flask(__name__, template_folder=".", static_folder=".", static_url_path="")

DB_FILE = "Calls.db"

# SMTP Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "your_email@gmail.com"  # Replace with your sending email address
SENDER_PASSWORD = "your_app_password"  # Replace with your Gmail App Password
RECEIVER_EMAIL = "ojasveekumar@gmail.com"


def init_db():
    """Initialize the SQLite database and table."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS calls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            project_type TEXT,
            message TEXT,
            submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def send_email_notification(name, email, project_type, message):
    """Send an email notification using SMTP."""
    subject = f"New Inquiry Received from {name}"
    body = f"""
    New inquiry details:

    Name: {name}
    Email: {email}
    Project Type: {project_type}
    Message:
    {message}
    """

    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
    except Exception as e:
        print(f"Failed to send email: {e}")


@app.route("/")
def index():
    """Serve the main HTML page."""
    return render_template("index.html")


@app.route("/api/submit-inquiry", methods=["POST"])
def submit_inquiry():
    """Receive form submission, insert into SQLite database, and send an email."""
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid payload"}), 400

    name = data.get("name")
    email = data.get("email")
    project_type = data.get("project_type")
    message = data.get("message")

    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO calls (name, email, project_type, message) VALUES (?, ?, ?, ?)",
            (name, email, project_type, message),
        )
        conn.commit()
        conn.close()

        # Send email notification after successful DB save
        send_email_notification(name, email, project_type, message)

        return jsonify({"message": "Data stored and email sent successfully"}), 200
    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({"error": "Database transaction failed"}), 500


if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)