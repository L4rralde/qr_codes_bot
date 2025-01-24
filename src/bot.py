"""
Code to run a telegram bot which generates an image with aggregated qr co
"""

import os

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from my_secrets import BOT_TOKEN
from db import AMIGOS
from generate_qr import generate_agg_qr, AmigoQR
from misc import GIT_ROOT

#Add missing dirs
if not os.path.exists(f"{GIT_ROOT}/images"):
    os.makedirs(f"{GIT_ROOT}/images")

# Initialize the bot
bot = telebot.TeleBot(BOT_TOKEN)

# A dictionary to store the user's checkbox state
checkbox_states = {}

amigos_dict = {
    amigo.name: amigo
    for amigo in AMIGOS
}

@bot.message_handler(commands=['start'])
def send_checkbox_list(message):
    """
    Main function of the bot. Start command
    Sends a checkbox list comprised by the list of all Amigos
    """
    chat_id = message.chat.id

    # Initialize the checkbox states for the user
    checkbox_states[chat_id] = {
        amigo.name: False
        for amigo in AMIGOS
    }

    # Send the checkbox list
    bot.send_message(
        chat_id,
        "Selecciona pasajeros:",
        reply_markup=generate_checkbox_markup(chat_id)
    )


def generate_checkbox_markup(chat_id):
    """
    Function to generate the inline keyboard with checkboxes
    """
    markup = InlineKeyboardMarkup()

    for option, state in checkbox_states[chat_id].items():
        # Use ✅ or ⬜ to represent checked/unchecked states
        checkbox_symbol = "✅" if state else "⬜"
        markup.add(
            InlineKeyboardButton(f"{checkbox_symbol} {option}", callback_data=option)
        )

    markup.add(InlineKeyboardButton("Submit", callback_data="submit"))
    return markup


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    """
    Callback query handler.
    Callback of the checkbox list
    """
    chat_id = call.message.chat.id

    # If the user clicks "Submit", finalize their selection
    if call.data == "submit":
        amigos_qr = [
            AmigoQR(amigos_dict[option])
            for option, state in checkbox_states[chat_id].items() if state
        ]
        path = f"{GIT_ROOT}/images/test.png"
        generate_agg_qr(amigos_qr, path)
        with open(path, "rb") as photo:
            bot.send_photo(chat_id=chat_id, photo=photo, caption="Voila")

        #selected_options = [option for option, state in checkbox_states[chat_id].items() if state]
        #bot.send_message(chat_id, f"You selected: {', '.join(selected_options) or 'Nothing!'}")
        return

    # Toggle the state of the selected option
    if call.data in checkbox_states[chat_id]:
        checkbox_states[chat_id][call.data] = not checkbox_states[chat_id][call.data]
        # Update the message with the new state
        bot.edit_message_text(
            "Selecciona pasajeros:",
            chat_id=chat_id,
            message_id=call.message.message_id,
            reply_markup=generate_checkbox_markup(chat_id)
        )

# Run the bot
bot.polling()
