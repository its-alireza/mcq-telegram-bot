import telebot
from telebot import types
from api import generate_mcq
import logging
from datetime import datetime
from dotenv import load_dotenv
import os

# load environment variables from .env file
load_dotenv()

# API key and Telegram token
api_key = os.getenv("API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# log setup
logging.basicConfig(filename='user_activity.log', level=logging.INFO, format='%(asctime)s - %(message)s')

user_data = {}

# Log user action
def log_activity(user_id, action, details=""):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logging.info(f"User ID: {user_id} | Action: {action} | Timestamp: {timestamp} | {details}")

# /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user = message.from_user
    log_activity(user.username or user.id, "start", f"User {user.first_name} started the bot.")
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    generate_button = types.KeyboardButton("Generate MCQ")
    markup.add(generate_button)
    bot.reply_to(message, f"👋 Hello {user.first_name}!\n\n👉 Use the 'Generate MCQ' button to send me a text for generating a multiple-choice question.", reply_markup=markup)


# 'Generate MCQ' button
@bot.message_handler(func=lambda message: message.text.lower() == "generate mcq")
def request_text_for_mcq(message):
    user_id = message.from_user.id
    log_activity(user_id, "generate_mcq_clicked", "User clicked 'Generate MCQ'.")
    
    bot.reply_to(message, "📝 Please send me a text for generating a multiple choice question.")
    bot.register_next_step_handler(message, generate_mcq_command)

# if user didnt use the button
@bot.message_handler(func=lambda message: not message.text.lower() == "generate mcq")
def remind_use_button(message):
    bot.reply_to(message, "⚠️ Please press 'Generate MCQ' button to type your text for generating a question.")

# make mcq
def generate_mcq_command(message):
    user_id = message.from_user.id
    user_input = message.text.strip()

    # ignore 'Generate MCQ' as input text
    if user_input == "Generate MCQ":
        bot.reply_to(message, "⚠️ Please send the text first to generate a question.")
        bot.register_next_step_handler(message, generate_mcq_command)
        return

    if not user_input:
        bot.reply_to(message, "❗You didn't provide any text. Please try again.")
        return

    log_activity(user_id, "generate_mcq_input", f"User sent text: {user_input}")

    # generate mcq
    try:
        response = generate_mcq(user_input, api_key)
        question = response["question"]
        options = response["options"]
        correct_answer = response["correct_answer"]

        # Save question data
        user_data[user_id] = {"correct_answer": correct_answer, "question": question, "options": options, "answered": False}

        # Send question with options in inlinekeyboard
        markup = types.InlineKeyboardMarkup(row_width=1)
        buttons = [types.InlineKeyboardButton(f"{key}: {value}", callback_data=f"{key}_{user_id}") for key, value in options.items()]
        markup.add(*buttons)

        log_activity(user_id, "mcq_generated", f"Generated question: {question} with options: {options}")
        bot.send_message(message.chat.id, question, reply_markup=markup)

    except ValueError as e:
        log_activity(user_id, "error", f"Error generating MCQ: {str(e)}")
        bot.reply_to(message, "Error generating the MCQ. Please try again.")


# user answer
@bot.callback_query_handler(func=lambda call: True)
def handle_answer(call):
    user_id = call.from_user.id
    selected_answer, user_id_from_callback = call.data.split("_")

    if int(user_id_from_callback) != user_id:
        bot.answer_callback_query(call.id, "This button is not for you.")
        return
    
    if user_id in user_data and not user_data[user_id]["answered"]:
        correct_answer = user_data[user_id]["correct_answer"]
        result_text = "✅ Correct" if selected_answer == correct_answer else f"❌ Incorrect\n\nThe right answer was {correct_answer}."

        user_data[user_id]["answered"] = True
        log_activity(user_id, "answer_submitted", f"User selected answer: {selected_answer}. Result: {result_text}")

        bot.send_message(call.message.chat.id, result_text)
        bot.answer_callback_query(call.id, "Your answer has been recorded.")
    else:
        bot.answer_callback_query(call.id, "⚠️ You already answered this question, or something went wrong.")

if __name__ == '__main__':
    bot.polling(none_stop=True)