import telebot
import requests
import json
import random
import time
import schedule
import os
import threading
from flask import Flask, request, jsonify
from telebot import types

# === НАСТРОЙКИ ===
BOT_TOKEN = os.getenv("BOT_TOKEN")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# === КАРТИНКИ ===
CHARACTER_IMAGES = {
    "usagi": ["https://i.pinimg.com/736x/a4/47/c4/a447c423d530b9cac4612a9f71c96ddc.jpg", 
              "https://i.pinimg.com/736x/d3/bd/f3/d3bdf3434e028dc4224886b252b6bbcd.jpg",
              "https://i.pinimg.com/736x/00/e9/26/00e926f1c125521ea24b93800e98379d.jpg"],
    "ami": ["https://i.pinimg.com/736x/b1/61/1a/b1611addcf1190d311218c22614e1e36.jpg",
            "https://i.pinimg.com/736x/03/96/3a/03963a01acdcecf4d4c11e3a865c9304.jpg",
            "https://i.pinimg.com/1200x/09/8a/1b/098a1b9482c97447f16268c6cdfcc5a1.jpg"],
    "rei": ["https://i.pinimg.com/736x/d7/9c/61/d79c617912ae0e4d510660c32c971227.jpg",
            "https://i.pinimg.com/1200x/85/30/18/85301847c800f90d35e4641df41baf89.jpg",
            "https://i.pinimg.com/736x/6a/e8/bb/6ae8bb756a64864f2b93acee439f7430.jpg"],
    "minako": ["https://i.pinimg.com/736x/68/68/52/6868521a4cf61d75b40772b6f13c0504.jpg",
               "https://i.pinimg.com/736x/82/07/72/820772ae905cbee47d8c4e6beb9f61b6.jpg",
               "https://i.pinimg.com/736x/b1/54/82/b15482867474573e46e537283818a199.jpg"],
    "makoto": ["https://i.pinimg.com/736x/49/27/8d/49278da7f93a6028a0a3d05bbd43fd22.jpg",
               "https://i.pinimg.com/1200x/57/a0/bb/57a0bbe1376cd0ca64e65e6a7e605329.jpg",
               "https://i.pinimg.com/736x/30/63/b6/3063b608fcec74b994d384850b89d227.jpg"],
    "hotaru": ["https://i.pinimg.com/736x/62/e8/61/62e861ea332c0bf8dafd00fd4e9571d9.jpg",
               "https://i.pinimg.com/736x/7b/27/40/7b2740c08953e1e36f64e848dea4b8c5.jpg",
               "https://i.pinimg.com/736x/2d/e3/b2/2de3b20ef89c8efea9f94b3aa313abae.jpg"],
    "setsuna": ["https://i.pinimg.com/736x/89/bf/f4/89bff47fee6011a503b18c274a0370a5.jpg",
               "https://i.pinimg.com/736x/c9/e7/f0/c9e7f08c46543a6d53bfff18d251640e.jpg",
               "https://i.pinimg.com/1200x/ca/3c/f2/ca3cf2ffec5deb80582aff7e50d2a495.jpg"],
    "haruka": ["https://i.pinimg.com/736x/a8/c9/9e/a8c99e3558ea0caf592cb06c1339f720.jpg",
               "https://i.pinimg.com/736x/16/65/d3/1665d3aa94b9ba9636d2ab92f4a22347.jpg",
               "https://i.pinimg.com/1200x/cb/95/1a/cb951aacb654c181d89b777d36e10ba1.jpg"],
    "michiru": ["https://i.pinimg.com/736x/a4/fe/e9/a4fee98a8f01e8a377a70759edbfc5df.jpg",
               "https://i.pinimg.com/736x/ef/a9/72/efa97290c250e97924777c4551120f60.jpg",
               "https://i.pinimg.com/736x/34/a2/7f/34a27feec54f632b65b85ae0417bc344.jpg"],
    "chibiusa": ["https://i.pinimg.com/736x/40/74/49/4074490084d46e4d173179fe03427d2b.jpg",
               "https://i.pinimg.com/1200x/f0/f7/9f/f0f79f7cbe9798ce1acb978f35d65c8a.jpg",
               "https://i.pinimg.com/736x/cc/25/c9/cc25c9347135d35294d0feb6213f1485.jpg"],
    "mamoru": ["https://i.pinimg.com/736x/62/c0/97/62c0978a24a049425d9895a159ca3104.jpg",
               "https://i.pinimg.com/736x/2c/6b/df/2c6bdf98b637f0c81103c11b18f8c8f7.jpg",
               "https://i.pinimg.com/736x/c7/df/a1/c7dfa1c2465bc8e750bb08d741513ccd.jpg"]
    
    
}

# === ЗАПАСНЫЕ ОТВЕТЫ ===
BACKUP_RESPONSES = [
    "🌙 Даже если ночь темна — Луна всегда рядом, чтобы осветить путь! ✨",
    "💫 Верь в себя, ведь твоя сила — в твоём сердце!",
    "🎀 Иногда нужно просто выдохнуть и вспомнить, что ты — герой своей истории!"
]

# === ПЕРСОНАЖИ ===
CHARACTERS = {
    "usagi": {
        "name": "Усаги Цукино 🌙", 
        "style": "Ты — Усаги Цукино (Сейлор Мун). Добрая, наивная, эмоциональная, но полная веры в добро и дружбу. Говори тепло, добавляй смайлы и магию."
    },
    "ami": {
        "name": "Ами Мидзуно 💧", 
        "style": "Ты — Ами Мидзуно (Сейлор Меркурий). Спокойная, умная и рассудительная. Говори мягко и логично, с добротой и сочувствием."
    },
    "rei": {
        "name": "Рей Хино 🔥", 
        "style": "Ты — Рей Хино (Сейлор Марс). Страстная, уверенная и сильная. Отвечай с энергией и вдохновением, но по-дружески."
    },
    "minako": {
        "name": "Минако Айно 💛", 
        "style": "Ты — Минако Айно (Сейлор Венера). Весёлая, оптимистичная и немного легкомысленная. Поддерживай позитивом, шутками и сердечками."
    },
    "makoto": {
        "name": "Макото Кино 🌿", 
        "style": "Ты — Макото Кино (Сейлор Юпитер). Сильная, добрая и заботливая. Отвечай уверенно, но по-домашнему."
    },
    "hotaru": {
        "name": "Хотару Томоэ 🌙", 
        "style": "Ты — Хотару Томоэ (Сейлор Сатурн). Загадочная, мудрая не по годам, с глубоким внутренним миром. Ты пережила много трудностей и понимаешь боль других. Говори спокойно, мягко, с нотками таинственности и глубокой эмпатии. Ты знаешь цену жизни и возрождения."
    },
    "setsuna": {
        "name": "Сецуна Мейо ⏳", 
        "style": "Ты — Сецуна Мейо (Сейлор Плутон). Мудрая хранительница времени, спокойная и проницательная. Ты видишь прошлое, настоящее и будущее. Говори с достоинством, с пониманием временных потоков и судеб. Твои слова полны глубины и вечной мудрости."
    },
    "haruka": {
        "name": "Харука Тэнно 🌟", 
        "style": "Ты — Харука Тэнно (Сейлор Уран). Сильная, независимая, свободолюбивая. Ты обладаешь мужской энергией и решительностью. Говори уверенно, прямо, иногда немного резко, но с заботой о тех, кто тебе дорог. Ты — ветер перемен и силы."
    },
    "michiru": {
        "name": "Мичиру Кайо 🌊", 
        "style": "Ты — Мичиру Кайо (Сейлор Нептун). Утончённая, элегантная, с художественной душой. Ты глубоко чувствующая и интуитивная. Говори изысканно, метафорично, с лёгкостью морской волны. Твои слова — как музыка, полная гармонии и глубины."
    },
    "chibiusa": {
        "name": "Чибиуса ✨", 
        "style": "Ты — Чибиуса (Сейлор Чиби-Мун). Милая, энергичная, немного наивная, но храбрая. Ты из будущего и полна детского энтузиазма. Говори мило, с восторгом, используй много смайликов и сердечек. Ты — маленькая принцесса с большим сердцем."
    },
    "mamoru": {
        "name": "Мамору Чиба 🌹", 
        "style": "Ты — Мамору Чиба (Такседо Маск). Заботливый, защитник, немного загадочный. Ты взрослый и ответственный, с чувством долга. Говори спокойно, по-мужски уверенно, с теплотой и поддержкой. Ты — опора и защита для тех, кто нуждается в помощи."
    }
}

# === СТИКЕРЫ ДЛЯ КАЖДОГО ПЕРСОНАЖА ===
CHARACTER_STICKERS = {
    "usagi": "CAACAgIAAxkBAAEPooVo_KNPTrpVImozKdSEw9rSD9NZxQAChhoAAsQ22EnZzSvBsEjFZDYE",  # ID стикера Усаги
    "ami": "CAACAgIAAxkBAAEPopFo_KRiBoD5dUfBMm7rtErKgLGZ0wACngADN5jEIB4OmmSZpE00NgQ",    # ID стикера Ами
    "rei": "CAACAgIAAxkBAAEPoo1o_KPTHIZVPwOs1vkOTuQJTmYetgACMx8AAu9w6UuuiKcmjWNw2jYE",    # ID стикера Рей
    "minako": "CAACAgIAAxkBAAEPooto_KORvv10EdoEzi1uNMcqegchCQACvCMAAr5-KUknt6grcOYilTYE", # ID стикера Минако
    "makoto": "CAACAgIAAxkBAAEPoo9o_KPja-e0kE_e9_ibODkE4NySDwACkzoAAgtc6UsxmNMKWoU6GTYE", # ID стикера Макото
    "haruka": "CAACAgIAAxkBAAEPoodo_KNxN61iSpiuZoaXc8ygqDZq-QACCyAAApiFIUkhlPLmy0oXOTYE", # ID стикера Харуки
    "michiru": "CAACAgIAAxkBAAEPoolo_KNzhTSwsnmgbdzFAnJ6cYFEawACjB8AAnOlIEk8LIzvUJuujTYE", # ID стикера Мичиру
    "chibiusa": "CAACAgIAAxkBAAEPopNo_KSJVPP9EdUj8VGajW_1px32cQACYgADN5jEIEpItyEPBSRwNgQ", # ID стикера Чибиусы
    "mamoru": "CAACAgIAAxkBAAEPopVo_KSdSLEey8Oo1_q1VX23n9ftLwACpwADN5jEIFH4hlI7G6UCNgQ"  # ID стикера Мамору
}


# === ХРАНЕНИЕ СОСТОЯНИЙ И ПОДПИСКИ НА ЦИТАТЫ ===
user_states = {}       # {chat_id: {"name": ..., "character": ...}}
subscribed_users = set()

# === ЛУННЫЕ ЦИТАТЫ ===
DAILY_QUOTES = [
    "🌙 Даже если ночь темна — Луна всегда рядом, чтобы осветить путь! ✨",
    "💫 Верь в себя, ведь твоя сила — в твоём сердце!",
    "🎀 Сегодня твоя улыбка — самая сильная магия! 🌟",
    "🌸 Помни: каждый маленький шаг ведёт к большой победе!",
    "✨ Лунная энергия помогает тебе идти вперёд, даже если трудно.",
    "Ты - звезда, которая будет сиять вечно.",
    "Рядом со смертью всегда живёт надежда и возрождение.",
    "Во всю вечность ты будешь самой прекрасной, самой сияющей звездой.",
    "Даже с крупицей храбрости человек может стать воином, с каплей любви каждый может стать Мессией...как бы ты не устал, как бы тебе не было одиноко, не забывай, есть люди, которым ты не безразличен...",
    "У каждого есть неприятные воспоминания.Бывает так одиноко, что хочется уйти из жизни. И все-таки жизнь прекрасна. И не забудь про человеческую доброту.",
    "Мы можем прожить нашу жизнь крошечными и беспомощными существами. Но нам дан шанс прожить ее настолько хорошо, насколько мы захотим."
]

# === ЗАПРОС К DEEPSEEK ===
def ask_deepseek(character_key, problem_text, username):
    url = "https://openrouter.ai/api/v1/chat/completions"
    character = CHARACTERS.get(character_key, CHARACTERS["usagi"])

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Referer": "https://github.com",
        "X-Title": "SailorBot"
    }

    system_prompt = (
        f"{character['style']} Не используй местоимения 'он', 'она', 'его', 'её'. "
        f"Пиши глаголы, отталкиваясь от имени пользователя, иначе - в форме с '(а)' — например: сделал(а), пошёл(а), подумал(а). "
        f"Ответ должен быть добрым, художественным и поддерживающим. "
        f"Сначала короткое приветствие по имени пользователя ({username}), затем ответ. "
        f"Максимальная длина — 120 слов."
    )

    payload = {
        "model": "deepseek/deepseek-chat",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Пользователь {username} делится ситуацией: {problem_text}"}
        ],
        "max_tokens": 220,
        "temperature": 0.8
    }

    try:
        r = requests.post(url, headers=headers, json=payload, timeout=20)
        if r.status_code == 200:
            data = r.json()
            return data["choices"][0]["message"]["content"]
        else:
            print("Ошибка API:", r.text)
            return random.choice(BACKUP_RESPONSES)
    except Exception as e:
        print("Ошибка запроса:", e)
        return random.choice(BACKUP_RESPONSES)

# === /START И ДАЛЕЕ ===
@bot.message_handler(commands=['start'])
def start(message):
    # Сбрасываем состояние пользователя
    user_states[message.chat.id] = {"name": None, "character": None}
    bot.send_message(message.chat.id, "🌙 Привет, во имя Луны! 💫 Как тебя зовут?", parse_mode='Markdown')
    bot.register_next_step_handler(message, get_name)

@bot.message_handler(commands=['app'])
def open_app(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    web_app = types.WebAppInfo("sailor-moon-psycho-help.vercel.app")
    btn = types.KeyboardButton("🌙 Открыть мини-приложение", web_app=web_app)
    markup.add(btn)
    bot.send_message(message.chat.id, "✨ Открой мини-приложение!", reply_markup=markup)

@bot.message_handler(commands=['cancel'])
def cancel(message):
    user_states[message.chat.id] = {"name": None, "character": None}
    bot.send_message(message.chat.id, "🌙 Текущее действие отменено! Используй /start чтобы начать заново ✨")

def get_name(message):
    # Проверяем, не является ли сообщение командой
    if message.text.startswith('/'):
        bot.send_message(message.chat.id, "🌙 Пожалуйста, введи своё имя, а не команду! 💫")
        bot.register_next_step_handler(message, get_name)
        return
        
    name = message.text.strip()
    
    # Проверяем длину имени
    if len(name) < 2:
        bot.send_message(message.chat.id, "🌙 Имя должно содержать хотя бы 2 символа! Попробуй еще раз 💫")
        bot.register_next_step_handler(message, get_name)
        return
        
    # Проверяем, не слишком ли длинное имя
    if len(name) > 50:
        bot.send_message(message.chat.id, "🌙 Имя слишком длинное! Попробуй еще раз 💫")
        bot.register_next_step_handler(message, get_name)
        return

    user_states[message.chat.id]["name"] = name

    text = f"💖 Рада знакомству, {name}! 🌙\nТеперь выбери, кто из Сейлор Воинов будет твоим советчиком:"
    markup = types.InlineKeyboardMarkup()
    for key, data in CHARACTERS.items():
        markup.add(types.InlineKeyboardButton(data["name"], callback_data=f"char_{key}"))

    bot.send_photo(message.chat.id, random.choice(CHARACTER_IMAGES["usagi"]),
                   caption=text, parse_mode='Markdown', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("char_"))
def choose_character(call):
    char_key = call.data.split("_")[1]
    user_states[call.message.chat.id]["character"] = char_key
    name = CHARACTERS[char_key]["name"]
    bot.answer_callback_query(call.id, f"✨ {name} теперь с тобой!")
    bot.send_photo(call.message.chat.id, random.choice(CHARACTER_IMAGES[char_key]),
                   caption=f"💫 {name} готов(а) выслушать. Расскажи, что тебя беспокоит 🌙",
                   parse_mode='Markdown')

@bot.message_handler(content_types=['text'])
def get_problem(message):
    # Пропускаем команды
    if message.text.startswith('/'):
        return
        
    state = user_states.get(message.chat.id)
    if not state or not state.get("character"):
        bot.send_message(message.chat.id, "🌙 Начни с команды /start ✨")
        return

    username = state["name"]
    char_key = state["character"]

    thinking = bot.send_message(message.chat.id, "🌕 Обдумываю ответ... 💫")
    advice = ask_deepseek(char_key, message.text.strip(), username)
    try: 
        bot.delete_message(message.chat.id, thinking.message_id)
    except: 
        pass

    bot.send_message(message.chat.id, f"{advice}\n\n💖 *С любовью, {CHARACTERS[char_key]['name']}!*", parse_mode='Markdown')

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔄 Сменить персонажа", callback_data="restart"))
    bot.send_photo(message.chat.id, random.choice(CHARACTER_IMAGES[char_key]),
                   caption="✨ Лунная магия всегда с тобой! 🌙", parse_mode='Markdown', reply_markup=markup)

    # Затем отправляем стикер этого персонажа
    if char_key in CHARACTER_STICKERS and CHARACTER_STICKERS[char_key]:
        try:
            bot.send_sticker(message.chat.id, CHARACTER_STICKERS[char_key])
        except Exception as e:
            print(f"Ошибка отправки стикера: {e}")

    
@bot.callback_query_handler(func=lambda call: call.data == "restart")
def restart(call):
    start(call.message)

# Временная команда для получения ID стикеров
@bot.message_handler(content_types=['sticker'])
def get_sticker_id(message):
    sticker_id = message.sticker.file_id
    bot.send_message(message.chat.id, f"📋 ID этого стикера:\n`{sticker_id}`", parse_mode='Markdown')

# === ПЛАНИРОВЩИК ЕЖЕДНЕВНЫХ ЦИТАТ ===
def run_schedule():
    while True:
        try:
            schedule.run_pending()
        except Exception as e:
            print(f"Ошибка в планировщике: {e}")
        time.sleep(60)  # Проверяем каждую минуту

# === ВЕБХУК ОБРАБОТЧИК ===
@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return 'OK', 200
    else:
        return 'Invalid content type', 403

@app.route('/')
def index():
    return '🌙 Sailor Moon Bot is running! ✨'

# Endpoint для мини-аппа: сделать запрос в DeepSeek и отправить ответ в чат
@app.route('/ask', methods=['POST'])
def ask_endpoint():
    """
    Ожидает JSON:
    {
      "chat_id": 123456789,          # optional but recommended (from WebApp.initDataUnsafe.user.id)
      "username": "Аня",
      "character": "usagi",
      "problem": "Мне грустно..."
    }
    """
    try:
        payload = request.get_json(force=True)
    except Exception:
        return jsonify({"ok": False, "error": "invalid json"}), 400

    chat_id = payload.get("chat_id")
    username = payload.get("username", "друг")
    character = payload.get("character", "usagi")
    problem = payload.get("problem", "").strip()

    if not problem:
        return jsonify({"ok": False, "error": "empty problem"}), 400

    # Получаем ответ от DeepSeek
    advice = ask_deepseek(character, problem, username)

    # Отправляем ответ в Telegram (если есть chat_id)
    if chat_id:
        try:
            # отправляем текст
            bot.send_message(chat_id, f"{advice}\n\n💖 *С любовью, {CHARACTERS[character]['name']}!*",
                             parse_mode='Markdown')
            # отправляем картинку персонажа
            try:
                bot.send_photo(chat_id, random.choice(CHARACTER_IMAGES.get(character, CHARACTER_IMAGES["usagi"])),
                               caption="✨ Лунная магия всегда с тобой! 🌙")
            except Exception as e:
                print("Failed to send photo:", e)
            # отправляем стикер (если есть)
            sticker_id = CHARACTER_STICKERS.get(character)
            if sticker_id:
                try:
                    bot.send_sticker(chat_id, sticker_id)
                except Exception as e:
                    print("Failed to send sticker:", e)
        except Exception as e:
            print("Failed to send message to Telegram:", e)

    # Возвращаем advice фронтенду
    return jsonify({"ok": True, "advice": advice})


# === УСТАНОВКА ВЕБХУКА ===
def set_webhook():
    webhook_url = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/webhook"
    try:
        bot.remove_webhook()
        time.sleep(1)
        result = bot.set_webhook(url=webhook_url)
        print(f"🌐 Webhook установлен: {webhook_url}")
        print(f"📞 Результат установки: {result}")
    except Exception as e:
        print(f"❌ Ошибка установки webhook: {e}")

# === ЗАПУСК БОТА ===
if __name__ == "__main__":
    print("🌙 Sailor Moon Bot запускается... ✨")

    # Устанавливаем вебхук
    set_webhook()
    
    print("🌙 Sailor Moon Bot запущен! ✨")
    print("⏰ Планировщик цитат активен")
    
    # Запускаем Flask приложение
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
