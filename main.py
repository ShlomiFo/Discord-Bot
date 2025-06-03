from utils import *
from flask import Flask, render_template, request, redirect, jsonify
from datetime import timedelta
app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html"), 200


@app.route("/send-message", methods=['POST'])
def send_message():
    try:
        text = request.form['text']
        send_to_discord(text)
        save_to_db(text)

        return redirect("/"), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@app.route("/messages")
def get_messages():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cutoff_time = datetime.now() - timedelta(minutes=30)
        cursor.execute('''
        SELECT message, date FROM messages
        WHERE date > ? 
         ''', (cutoff_time,))

        messages = cursor.fetchall()

        conn.commit()
        conn.close()

        return jsonify({"status": "success", "message": messages}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


if __name__ == '__main__':
    setup_db()
    app.run()
