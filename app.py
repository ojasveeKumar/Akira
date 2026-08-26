from flask import Flask, request, jsonify, render_template
import sqlite3

# Set template_folder='.' and static_folder='.' so Flask serves HTML and CSS from the root folder
app = Flask(__name__, template_folder='.', static_folder='.', static_url_path='')

DB_FILE = 'Calls.db'

def init_db():
    """Initialize the SQLite database and table."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS calls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            project_type TEXT,
            message TEXT,
            submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    """Serve the main HTML page."""
    return render_template('index.html')

@app.route('/api/submit-inquiry', methods=['POST'])
def submit_inquiry():
    """Receive form submission and insert into SQLite database."""
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Invalid payload'}), 400

    name = data.get('name')
    email = data.get('email')
    project_type = data.get('project_type')
    message = data.get('message')

    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO calls (name, email, project_type, message) VALUES (?, ?, ?, ?)",
            (name, email, project_type, message)
        )
        conn.commit()
        conn.close()
        return jsonify({'message': 'Data stored successfully'}), 200
    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({'error': 'Database transaction failed'}), 500

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)