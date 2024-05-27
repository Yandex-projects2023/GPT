import g4f
import telebot
from telebot import types

bot = telebot.TeleBot("7174350795:AAFcP25wD6eiZfxdeOg2_2fyl5gB1TPn14k")

select_chat = "GPT-3.5"
context = []


def ask_gpt(promt: list, model: str) -> str:
    response = g4f.ChatCompletion.create(
        model=model,
        provider=g4f.Provider.Aichatos,
        messages=promt,
    )
    return response


@bot.message_handler(commands=["start"])
def main(message):
    markup = types.ReplyKeyboardMarkup()

    btn1 = types.KeyboardButton("/GPT-4")
    btn2 = types.KeyboardButton("/GPT-3.5")

    markup.row(btn1, btn2)

    bot.send_message(message.chat.id, "Привет! Выбери нейросеть которой хочешь воспользоватся.", reply_markup=markup)


@bot.message_handler(commands=["GPT-4", "GPT-3.5"])
def select(message):
    if message.text == "/GPT-4":
        bot.send_message(message.chat.id, "Внимание! Из-за проблем с подключением к этой модели, она временно заблокирована для использования.")
    elif message.text == "/GPT-3.5":
        select_chat = "GPT-3.5"
        bot.send_message(message.chat.id, "Модель применена.")
        bot.send_message(message.chat.id, "Задавайте вопросы.")


@bot.message_handler()
def ask(message):
    context.append({"role": "user", "content": message.text})
    answer = ask_gpt(promt=context, model=select_chat)
    bot.send_message(message.chat.id, answer)
    context.append({"role": "assistant", "content": answer})


bot.polling(none_stop=True)
