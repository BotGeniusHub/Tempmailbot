import os
import requests
from pyrogram import Client, filters, idle
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import API_ID, API_HASH, BOT_TOKEN

app = Client("tempmailbot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN) 

@app.on_message(filters.command("start"))
def start(client, message):
    client.send_message(chat_id=message.chat.id, text="Welcome to the TempMailBot!")


@app.on_message(filters.command("help"))
def help(client, message):
    help_text = "This bot provides temporary email addresses. Use /generate to get a new address."
    client.send_message(chat_id=message.chat.id, text=help_text)


@app.on_message(filters.command("generate"))
def generate(client, message):
    api_url = "https://www.1secmail.com/api/v1/"
    response = requests.get(api_url + "/?action=genRandomMailbox&count=1")
    if response.status_code == 200:
        email_address = response.json()[0]
        client.send_message(chat_id=message.chat.id, text=f"Your temporary email address is: {email_address}")
    else:
        client.send_message(chat_id=message.chat.id, text="Failed to generate a temporary email address.")


@app.on_message(filters.command("inbox"))
def inbox(client, message):
    api_url = "https://www.1secmail.com/api/v1/"
    email_address = "example@example.com"  # Replace with the actual email address
    response = requests.get(api_url + f"/?action=getMessages&login={email_address}&domain=1secmail.com")
    if response.status_code == 200:
        messages = response.json()
        if messages:
            for message in messages:
                subject = message["subject"]
                client.send_message(chat_id=message.chat.id, text=f"Subject: {subject}")
        else:
            client.send_message(chat_id=message.chat.id, text="No messages in the inbox.")
    else:
        client.send_message(chat_id=message.chat.id, text="Failed to retrieve inbox messages.")


@app.on_message(filters.command("delete"))
def delete_mail(client, message):
    api_url = "https://www.1secmail.com/api/v1/"
    email_address = "example@example.com"  # Replace with the actual email address
    email_id = "12345"  # Replace with the actual email ID of the email you want to delete
    response = requests.get(api_url + f"/?action=deleteMessage&login={email_address}&domain=1secmail.com&id={email_id}")
    if response.status_code == 200:
        client.send_message(chat_id=message.chat.id, text="Email deleted successfully.")
    else:
        client.send_message(chat_id=message.chat.id, text="Failed to delete email.")


@app.on_message(filters.command("inline"))
def inline_buttons(client, message):
    keyboard = [
        [InlineKeyboardButton("Generate Temporary Email", callback_data='generate')],
        [InlineKeyboardButton("Inbox", callback_data='inbox')],
        [InlineKeyboardButton("Help", callback_data='help')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    client.send_message(chat_id=message.chat.id, text='Please choose an option:', reply_markup=reply_markup)


@app.on_callback_query()
def button_callback(client, callback_query):
    query = callback_query
    if query.data == 'generate':
        generate(client, query.message)
    elif query.data == 'inbox':
        inbox(client, query.message)
    elif query.data == 'help':
        help_text = "This bot provides temporary email addresses. Use /generate to get a new address."
        client.send_message(chat_id=query.message.chat.id, text=help_text)
    query.answer()


if __name__ == '__main__':
    app.run()
idle() 
