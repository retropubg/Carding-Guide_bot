import random
import string
import aiosqlite
from config import ADMIN_USER_IDS, DATABASE_PATH, BOT_TOKEN
from aiogram import Bot
from utils.admin_utils import *



def generate_ticket_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

async def save_ticket(user_id, ticket_id, inquiry_type, message):
    # This function would typically interact with a database
    # For this example, we'll just log the ticket
    logging.info(f"Saving ticket: User ID: {user_id}, Ticket ID: {ticket_id}, Type: {inquiry_type}, Message: {message}")

async def notify_admin(ticket_id, inquiry_type, message):
    # This function would typically send a message to an admin
    # For this example, we'll just log the notification
    logging.info(f"Admin notification: New ticket {ticket_id} ({inquiry_type}): {message}")

async def get_user_tickets(user_id, status=None):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        if status:
            query = 'SELECT ticket_id, inquiry_type, status, message FROM tickets WHERE user_id = ? AND status = ?'
            params = (user_id, status)
        else:
            query = 'SELECT ticket_id, inquiry_type, status, message FROM tickets WHERE user_id = ?'
            params = (user_id,)
        
        async with db.execute(query, params) as cursor:
            return await cursor.fetchall()

async def close_ticket(ticket_id):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute('UPDATE tickets SET status = ? WHERE ticket_id = ?', ('closed', ticket_id))
        await db.commit()
    logger.info(f"Closed ticket {ticket_id}")

async def reopen_ticket(ticket_id):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute('UPDATE tickets SET status = ? WHERE ticket_id = ?', ('open', ticket_id))
        await db.commit()
    logger.info(f"Reopened ticket {ticket_id}")

async def get_ticket_details(ticket_id):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute('SELECT * FROM tickets WHERE ticket_id = ?', (ticket_id,)) as cursor:
            row = await cursor.fetchone()
            if row:
                return {
                    'id': row[1],
                    'user_id': row[0],
                    'type': row[2],
                    'message': row[3],
                    'status': row[4],
                    'created_at': row[5]
                }
            return None

async def notify_admin(ticket_id, inquiry_type, message):
    bot = Bot(token=BOT_TOKEN)
    
    for admin_id in ADMIN_USER_IDS:
        try:
            await bot.send_message(
                admin_id,
                f"New ticket submitted:\n"
                f"Ticket ID: {ticket_id}\n"
                f"Type: {inquiry_type}\n"
                f"Message: {message}"
            )
        except Exception as e:
            logger.error(f"Failed to notify admin {admin_id}: {e}")

async def setup_database():
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS tickets (
                user_id INTEGER,
                ticket_id TEXT PRIMARY KEY,
                inquiry_type TEXT,
                message TEXT,
                status TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        await db.commit()