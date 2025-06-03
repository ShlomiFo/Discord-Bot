from discord_webhook import DiscordWebhook
import sqlite3
from datetime import datetime

DISCORD_WEBHOOK_URL = "https://discordapp.com/api/webhooks/1379444307181834246/92yy46FU3GOu4YSy38Eo8M2eBjSgL3XMn-LeU7vorXFZ3rpqYpwcoo4wRPAIC3Y9v4db"
TIME_FORMAT = "%y-%m-%d:%H-%M-%S"

def send_to_discord(text):
    webhook = DiscordWebhook(url=DISCORD_WEBHOOK_URL, content=text)
    webhook.execute()

def get_db_connection():
    return sqlite3.connect("messages.db")

def setup_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY,
    message TEXT,
    date TEXT
)  
''')
    conn.commit()
    conn.close()

def save_to_db(text):
    date = datetime.now().strftime(TIME_FORMAT)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO messages (message, date)
    VALUES (?,?)
     ''', (text, date))
    conn.commit()
    conn.close()
