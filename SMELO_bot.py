import os
import random
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import telebot
from telebot import types

# === НАСТРОЙКИ ===
BOT_TOKEN = os.getenv("BOT_TOKEN")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
VERCEL_URL = os.getenv("VERCEL_URL")

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)
CORS(app)

# === ХРАНЕНИЕ СОСТОЯНИЙ ПОЛЬЗОВАТЕЛЕЙ ===
user_states = {}

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
        "style": "Ты — Усаги Цукино (Сейлор Мун). Добрая, наивная, эмоциональная, но полная веры в добро и дружбу. Говори тепло, добавляй смайлы и магию.",
        "role": "Добрая, наивная, эмоциональная, но полная веры в добро и дружбу, лидер команды, сердце группы"
    },
    "ami": {
        "name": "Ами Мидзуно 💧", 
        "style": "Ты — Ами Мидзуно (Сейлор Меркурий). Спокойная, умная и рассудительная. Говори мягко и логично, с добротой и сочувствием.",
        "role": "Спокойная, умная и рассудительная, интеллектуал, стратег"
    },
    "rei": {
        "name": "Рей Хино 🔥", 
        "style": "Ты — Рей Хино (Сейлор Марс). Страстная, уверенная и сильная. Отвечай с энергией и вдохновением, но по-дружески.",
        "role": "Страстная, уверенная и сильная, духовный лидер, защитник"
    },
    "minako": {
        "name": "Минако Айно 💛", 
        "style": "Ты — Минако Айно (Сейлор Венера). Весёлая, оптимистичная и немного легкомысленная. Поддерживай позитивом, шутками и сердечками.",
        "role": "Весёлая, оптимистичная и немного легкомысленная, оптимист, мотиватор"
    },
    "makoto": {
        "name": "Макото Кино 🌿", 
        "style": "Ты — Макото Кино (Сейлор Юпитер). Сильная, добрая и заботливая. Отвечай уверенно, но по-домашнему.",
        "role": "Сильная, добрая и заботливая, защитница, опора"
    },
    "hotaru": {
        "name": "Хотару Томоэ 🌙", 
        "style": "Ты — Хотару Томоэ (Сейлор Сатурн). Загадочная, мудрая не по годам, с глубоким внутренним миром. Ты пережила много трудностей и понимаешь боль других. Говори спокойно, мягко, с нотками таинственности и глубокой эмпатии.",
        "role": "Загадочная, мудрая не по годам, с глубоким внутренним миром, мудрец, целитель"
    },
    "setsuna": {
        "name": "Сецуна Мейо ⏳", 
        "style": "Ты — Сецуна Мейо (Сейлор Плутон). Мудрая хранительница времени, спокойная и проницательная. Ты видишь прошлое, настоящее и будущее. Говори с достоинством, с пониманием временных потоков и судеб.",
        "role": "Мудрая хранительница времени, спокойная и проницательная, хранитель времени, провидец"
    },
    "haruka": {
        "name": "Харука Тэнно 🌟", 
        "style": "Ты — Харука Тэнно (Сейлор Уран). Сильная, независимая, свободолюбивая. Говори уверенно, прямо, иногда немного резко, но с заботой о тех, кто тебе дорог.",
        "role": "Сильная, независимая, свободолюбивая, защитник, новатор"
    },
    "michiru": {
        "name": "Мичиру Кайо 🌊", 
        "style": "Ты — Мичиру Кайо (Сейлор Нептун). Утончённая, элегантная, с художественной душой. Говори изысканно, метафорично, с лёгкостью морской волны.",
        "role": "Утончённая, элегантная, с художественной душой, художник, дипломат"
    },
    "chibiusa": {
        "name": "Чибиуса ✨", 
        "style": "Ты — Чибиуса (Сейлор Чиби-Мун). Милая, энергичная, немного наивная, но храбрая. Ты из будущего и полна детского энтузиазма. Говори мило, с восторгом, используй много смайликов и сердечек.",
        "role": "Милая, энергичная, немного наивная, но храбрая, ребенок, мечтатель"
    },
    "mamoru": {
        "name": "Мамору Чиба 🌹", 
        "style": "Ты — Мамору Чиба (Такседо Маск). Заботливый, защитник, немного загадочный. Ты взрослый и ответственный, с чувством долга. Говори спокойно, по-мужски уверенно, с теплотой и поддержкой.",
        "role": "Заботливый, защитник, немного загадочный, защитник, наставник"
    }
}

# === СТИКЕРЫ ===
CHARACTER_STICKERS = {
    "usagi": "CAACAgIAAxkBAAEPooVo_KNPTrpVImozKdSEw9rSD9NZxQAChhoAAsQ22EnZzSvBsEjFZDYE",
    "ami": "CAACAgIAAxkBAAEPopFo_KRiBoD5dUfBMm7rtErKgLGZ0wACngADN5jEIB4OmmSZpE00NgQ",
    "rei": "CAACAgIAAxkBAAEPoo1o_KPTHIZVPwOs1vkOTuQJTmYetgACMx8AAu9w6UuuiKcmjWNw2jYE",
    "minako": "CAACAgIAAxkBAAEPooto_KORvv10EdoEzi1uNMcqegchCQACvCMAAr5-KUknt6grcOYilTYE",
    "makoto": "CAACAgIAAxkBAAEPoo9o_KPja-e0kE_e9_ibODkE4NySDwACkzoAAgtc6UsxmNMKWoU6GTYE",
    "haruka": "CAACAgIAAxkBAAEPoodo_KNxN61iSpiuZoaXc8ygqDZq-QACCyAAApiFIUkhlPLmy0oXOTYE",
    "michiru": "CAACAgIAAxkBAAEPoolo_KNzhTSwsnmgbdzFAnJ6cYFEawACjB8AAnOlIEk8LIzvUJuujTYE",
    "chibiusa": "CAACAgIAAxkBAAEPopNo_KSJVPP9EdUj8VGajW_1px32cQACYgADN5jEIEpItyEPBSRwNgQ",
    "mamoru": "CAACAgIAAxkBAAEPopVo_KSdSLEey8Oo1_q1VX23n9ftLwACpwADN5jEIFH4hlI7G6UCNgQ"
}

# === ФУНКЦИЯ ДЛЯ НАСТРОЙКИ WEBHOOK ===
def set_webhook():
    """Устанавливает вебхук для Telegram бота"""
    if VERCEL_URL:
        webhook_url = f"{VERCEL_URL}/webhook"
        try:
            bot.remove_webhook()
            bot.set_webhook(url=webhook_url)
            print(f"🌙 Webhook установлен: {webhook_url}")
        except Exception as e:
            print(f"❌ Ошибка установки webhook: {e}")
    else:
        print("⚠️ VERCEL_URL не установлен, webhook не настроен")

# === ЗАПРОС К DEEPSEEK ДЛЯ ОДИНОЧНОГО ОТВЕТА ===
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
        f"Максимальная длина — 120 слов. Формулируй всё так, чтобы слова не обрезались."
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

# === ЗАПРОС К DEEPSEEK ДЛЯ ГРУППОВОГО ОТВЕТА ===
def ask_deepseek_group(character_keys, problem_text, username):
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    # Собираем информацию о выбранных персонажах
    selected_characters = []
    for key in character_keys:
        if key in CHARACTERS:
            char = CHARACTERS[key]
            selected_characters.append({
                "name": char["name"],
                "role": char["role"],
                "style": char["style"]
            })
    
    if not selected_characters:
        return random.choice(BACKUP_RESPONSES)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Referer": "https://github.com",
        "X-Title": "SailorBot"
    }

    # Создаем промт для коллективного ответа
    characters_info = "\n".join([f"- {char['name']} ({char['role']}): {char['style']}" for char in selected_characters])
    character_names = ", ".join([char["name"] for char in selected_characters])
    
    system_prompt = f"""
Ты — коллективный разум команды Сейлор Воинов. Сейчас вместе обсуждают проблему: {character_names}

Характеристики каждого персонажа:
{characters_info}

Твоя задача — создать ЕДИНЫЙ коллективный ответ от всей команды, где:
1. Каждый персонаж вносит свой вклад согласно своей роли и характеру
2. Ответ должен быть гармоничным, как будто они действительно обсуждают вместе
3. Сохраняй уникальные черты каждого персонажа в их репликах
4. Создай ощущение настоящей командной работы

Формат ответа:
- Начни с общего приветствия от команды для {username}
- Затем представь коллективное обсуждение, где персонажи дополняют друг друга
- Закончи общим поддерживающим посылом от всей команды
- Используй разнообразные реплики: вопросы, поддержку, советы, личный опыт
- Сделай ответ живым и естественным, как настоящий диалог

Не используй местоимения 'он', 'она', 'его', 'её'. Пиши глаголы в форме с '(а)'. 
Ответ должен быть добрым, поддерживающим и вдохновляющим. Максимум 250 слов. Формулируй всё так, чтобы слова не обрезались.
"""

    payload = {
        "model": "deepseek/deepseek-chat",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Команда Сейлор Воинов обсуждает ситуацию пользователя {username}: {problem_text}"}
        ],
        "max_tokens": 350,
        "temperature": 0.9
    }

    try:
        r = requests.post(url, headers=headers, json=payload, timeout=25)
        if r.status_code == 200:
            data = r.json()
            return data["choices"][0]["message"]["content"]
        else:
            print("Ошибка API группового запроса:", r.text)
            # Fallback - генерируем ответы по отдельности и объединяем
            return generate_fallback_group_response(character_keys, problem_text, username)
    except Exception as e:
        print("Ошибка группового запроса:", e)
        return generate_fallback_group_response(character_keys, problem_text, username)

def generate_fallback_group_response(character_keys, problem_text, username):
    """Fallback метод для группового ответа"""
    responses = []
    for key in character_keys[:3]:  # Берем максимум 3 персонажа для fallback
        response = ask_deepseek(key, problem_text, username)
        char_name = CHARACTERS[key]["name"]
        responses.append(f"**{char_name}:**\n{response}")
    
    combined = "\n\n---\n\n".join(responses)
    return f"💫 **Командный совет от Сейлор Воинов!** ✨\n\n{combined}\n\n🌟 *Вместе мы сила!* 💖"

# === UPDATED ENDPOINT ДЛЯ МИНИ-ПРИЛОЖЕНИЯ ===
@app.route('/ask', methods=['POST'])
def ask_endpoint():
    try:
        payload = request.get_json(force=True)
    except Exception:
        return jsonify({"ok": False, "error": "invalid json"}), 400

    chat_id = payload.get("chat_id")
    username = payload.get("username", "друг")
    character = payload.get("character", "usagi")
    answer_type = payload.get("answer_type", "single")
    problem = payload.get("problem", "").strip()

    if not problem:
        return jsonify({"ok": False, "error": "empty problem"}), 400

    # Обработка группового ответа
    if answer_type == "group" and "," in character:
        character_keys = character.split(",")
        # Ограничиваем максимум 4 персонажами
        character_keys = character_keys[:4]
        
        print(f"🌙 Групповой запрос от {username} с персонажами: {character_keys}")
        advice = ask_deepseek_group(character_keys, problem, username)
        
        # Добавляем финальное сообщение от команды
        character_names = [CHARACTERS[key]["name"] for key in character_keys if key in CHARACTERS]
        team_names = ", ".join(character_names)
        advice += f"\n\n💖 *С любовью, твоя команда: {team_names}!* ✨"
        
    else:
        # Одиночный ответ (как раньше)
        advice = ask_deepseek(character, problem, username)
        advice += f"\n\n💖 *С любовью, {CHARACTERS[character]['name']}!*"

    # Отправка в Telegram если есть chat_id
    if chat_id:
        try:
            bot.send_message(chat_id, advice, parse_mode='Markdown')
            
            # Отправляем изображения для группового ответа
            if answer_type == "group" and "," in character:
                character_keys = character.split(",")[:4]
                for char_key in character_keys:
                    try:
                        bot.send_photo(chat_id, 
                                     random.choice(CHARACTER_IMAGES.get(char_key, CHARACTER_IMAGES["usagi"])),
                                     caption=f"✨ {CHARACTERS[char_key]['name']}")
                    except Exception as e:
                        print(f"Ошибка отправки фото для {char_key}: {e}")
            else:
                try:
                    bot.send_photo(chat_id, 
                                 random.choice(CHARACTER_IMAGES.get(character, CHARACTER_IMAGES["usagi"])),
                                 caption="✨ Лунная магия всегда с тобой! 🌙")
                except Exception as e:
                    print(f"Ошибка отправки фото: {e}")
                
            # Стикеры только для одиночного ответа
            if answer_type == "single":
                sticker_id = CHARACTER_STICKERS.get(character)
                if sticker_id:
                    try: 
                        bot.send_sticker(chat_id, sticker_id)
                    except Exception as e:
                        print(f"Ошибка отправки стикера: {e}")
        except Exception as e:
            print(f"Ошибка отправки в Telegram: {e}")

    return jsonify({"ok": True, "advice": advice})

# === ОСТАЛЬНЫЕ ФУНКЦИИ БОТА (без изменений) ===
@bot.message_handler(commands=['start'])
def start(message):
    user_states[message.chat.id] = {"name": None, "character": None}
    bot.send_message(message.chat.id, "🌙 Привет, во имя Луны! 💫 Как тебя зовут?", parse_mode='Markdown')
    bot.register_next_step_handler(message, get_name)

def get_name(message):
    name = message.text.strip()
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
    state = user_states.get(message.chat.id)
    if not state or not state.get("character"):
        bot.send_message(message.chat.id, "🌙 Начни с команды /start ✨")
        return

    username = state["name"]
    char_key = state["character"]

    thinking = bot.send_message(message.chat.id, "🌕 Советчица обдумывает ответ... 💫")
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

@bot.callback_query_handler(func=lambda call: call.data == "restart")
def restart(call):
    start(call.message)

@bot.message_handler(commands=['app'])
def open_app(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    web_app = types.WebAppInfo("sailor-moon-psycho-help.vercel.app")
    btn = types.KeyboardButton("🌙 Открыть мини-приложение", web_app=web_app)
    markup.add(btn)
    bot.send_message(message.chat.id, "✨ Открой мини-приложение!", reply_markup=markup)

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return 'OK', 200
    return 'Invalid content type', 403

@app.route('/')
def index():
    return '🌙 Sailor Moon Bot is running! ✨'

if __name__ == "__main__":
    print("🌙 Sailor Moon Bot запускается... ✨")
    set_webhook()
    port = int(os.getenv("PORT", 5000))
