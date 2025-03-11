import telebot
import requests
import random


TELEGRAM_TOKEN = "7575961175:AAELh7cjOf7_FEs4GciXLw5NfzypaCjCbd4"
TMDB_API_KEY = "7c29207bbc86bed58d03d015f91cb670"

BASE_URL = "https://api.themoviedb.org/3"

bot = telebot.TeleBot(TELEGRAM_TOKEN)


def get_random_movie():
    page = random.randint(1, 500) 
    url = f"{BASE_URL}/discover/movie?api_key={TMDB_API_KEY}&language=ru-RU&page={page}"

    response = requests.get(url)
    if response.status_code == 200:
        movies = response.json().get("results", [])
        if movies:
            movie = random.choice(movies)
            return {
                "title": movie["title"],
                "overview": movie["overview"],
                "poster": f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie["poster_path"] else None
            }
    return None

# 🔹 /start и /help команды
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Напиши 'дай кино' или отправь /movie, и я пришлю случайный фильм! 🎬")

# 🔹 Команда /movie
@bot.message_handler(commands=['movie'])
def send_movie(message):
    movie = get_random_movie()
    if movie:
        text = f"🎬 *{movie['title']}*\n📖 {movie['overview']}"
        if movie["poster"]:
            bot.send_photo(message.chat.id, movie["poster"], caption=text, parse_mode="Markdown")
        else:
            bot.send_message(message.chat.id, text, parse_mode="Markdown")
    else:
        bot.reply_to(message, "Не удалось найти фильм 😢")

# 🔹 Если пользователь пишет "дай кино"
@bot.message_handler(func=lambda message: message.text.lower() == "дай кино")
def handle_text(message):
    send_movie(message)

# 🚀 Запуск бота
print("Бот запущен...")
bot.polling(none_stop=True)
