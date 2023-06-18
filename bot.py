import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, Updater


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to the Temp Mail Bot!")


def help(update, context):
    help_text = "This bot provides temporary email addresses. Use /generate to get a new address."
    context.bot.send_message(chat_id=update.effective_chat.id, text=help_text)


def generate(update, context):
    api_url = "https://www.1secmail.com/api/v1/"
    response = requests.get(api_url + "/?action=genRandomMailbox&count=1")
    if response.status_code == 200:
        email_address = response.json()[0]
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Your temporary email address is: {email_address}")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Failed to generate a temporary email address.")


def inbox(update, context):
    api_url = "https://www.1secmail.com/api/v1/"
    email_address = "example@example.com"  # Replace with the actual email address
    response = requests.get(api_url + f"/?action=getMessages&login={email_address}&domain=1secmail.com")
    if response.status_code == 200:
        messages = response.json()
        if messages:
            for message in messages:
                subject = message["subject"]
                context.bot.send_message(chat_id=update.effective_chat.id, text=f"Subject: {subject}")
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="No messages in the inbox.")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Failed to retrieve inbox messages.")


def delete_mail(update, context):
    api_url = "https://www.1secmail.com/api/v1/"
    email_address = "example@example.com"  # Replace with the actual email address
    email_id = "12345"  # Replace with the actual email ID of the email you want to delete
    response = requests.get(api_url + f"/?action=deleteMessage&login={email_address}&domain=1secmail.com&id={email_id}")
    if response.status_code == 200:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Email deleted successfully.")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Failed to delete email.")


def inline_buttons(update, context):
    keyboard = [
        [InlineKeyboardButton("Generate Temporary Email", callback_data='generate')],
        [InlineKeyboardButton("Inbox", callback_data='inbox')],
        [InlineKeyboardButton("Help", callback_data='help')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose an option:', reply_markup=reply_markup)


def button_callback(update, context):
    query = update.callback_query
    if query.data == 'generate':
        generate(update, context)
    elif query.data == 'inbox':
        inbox(update, context)
    elif query.data == 'help':
        help(update, context)
    query.answer()


def main():
    updater = Updater(token="YOUR_TELEGRAM_API_TOKEN", use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', help)
    generate_handler = CommandHandler('generate', generate)
    inbox_handler = CommandHandler('inbox', inbox)
    delete_mail_handler = CommandHandler('delete', delete_mail)
    inline_buttons_handler = CallbackQueryHandler(inline_buttons)
    button_callback_handler = CallbackQueryHandler(button_callback)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(generate_handler)
    dispatcher.add_handler(inbox_handler)
    dispatcher.add_handler(delete_mail_handler)
    dispatcher.add_handler(inline_buttons_handler)
    dispatcher.add_handler(button_callback_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
