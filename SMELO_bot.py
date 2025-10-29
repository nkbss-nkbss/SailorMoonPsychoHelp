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
    "usagi": "https://i.pinimg.com/736x/a4/47/c4/a447c423d530b9cac4612a9f71c96ddc.jpg", 
    "ami": "https://i.pinimg.com/736x/b1/61/1a/b1611addcf1190d311218c22614e1e36.jpg",
    "rei": "https://i.pinimg.com/736x/d7/9c/61/d79c617912ae0e4d510660c32c971227.jpg",
    "minako": "https://i.pinimg.com/736x/68/68/52/6868521a4cf61d75b40772b6f13c0504.jpg",
    "makoto": "https://i.pinimg.com/736x/49/27/8d/49278da7f93a6028a0a3d05bbd43fd22.jpg",
    "hotaru": "https://i.pinimg.com/736x/62/e8/61/62e861ea332c0bf8dafd00fd4e9571d9.jpg",
    "setsuna": "https://i.pinimg.com/736x/89/bf/f4/89bff47fee6011a503b18c274a0370a5.jpg",
    "haruka": "https://i.pinimg.com/736x/a8/c9/9e/a8c99e3558ea0caf592cb06c1339f720.jpg",
    "michiru": "https://i.pinimg.com/736x/a4/fe/e9/a4fee98a8f01e8a377a70759edbfc5df.jpg",
    "chibiusa": "https://i.pinimg.com/736x/40/74/49/4074490084d46e4d173179fe03427d2b.jpg",
    "mamoru": "https://i.pinimg.com/736x/62/c0/97/62c0978a24a049425d9895a159ca3104.jpg"
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
        "role": "лидер команды"
    },
    "ami": {
        "name": "Ами Мидзуно 💧", 
        "style": "Ты — Ами Мидзуно (Сейлор Меркурий). Спокойная, умная и рассудительная. Говори мягко и логично, с добротой и сочувствием.",
        "role": "интеллектуал"
    },
    "rei": {
        "name": "Рей Хино 🔥", 
        "style": "Ты — Рей Хино (Сейлор Марс). Страстная, уверенная и сильная. Отвечай с энергией и вдохновением, но по-дружески.",
        "role": "духовный лидер"
    },
    "minako": {
        "name": "Минако Айно 💛", 
        "style": "Ты — Минако Айно (Сейлор Венера). Весёлая, оптимистичная и немного легкомысленная. Поддерживай позитивом, шутками и сердечками.",
        "role": "оптимист"
    },
    "makoto": {
        "name": "Макото Кино 🌿", 
        "style": "Ты — Макото Кино (Сейлор Юпитер). Сильная, добрая и заботливая. Отвечай уверенно, но по-домашнему.",
        "role": "защитница"
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

# === ФУНКЦИЯ ДЛЯ ОТПРАВКИ СООБЩЕНИЯ С КАРТИНКОЙ ===
def send_message_with_photo(chat_id, text, character_key=None, parse_mode='Markdown'):
    """Отправляет сообщение с картинкой персонажа"""
    try:
        if character_key and character_key in CHARACTER_IMAGES:
            # Отправляем фото с подписью
            photo_url = CHARACTER_IMAGES[character_key]
            bot.send_photo(
                chat_id, 
                photo=photo_url, 
                caption=text,
                parse_mode=parse_mode
            )
        else:
            # Если нет картинки, отправляем просто текст
            bot.send_message(chat_id, text, parse_mode=parse_mode)
    except Exception as e:
        print(f"Ошибка отправки сообщения с фото: {e}")
        # Fallback - отправляем просто текст
        bot.send_message(chat_id, text, parse_mode=parse_mode)

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
        f"Формулируй всё так, чтобы слова не обрезались, а мысли были законченными. Максимальная длина — 120 слов."
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
- Используй разнообразные реплики: вопросы, поддержку, советы, личный опыт
- Сделай ответ живым и естественным, как настоящий диалог

Не используй местоимения 'он', 'она', 'его', 'её'. Пиши глаголы в форме с '(а)'. 
Ответ должен быть добрым, поддерживающим и вдохновляющим. Максимум 250 слов.
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
            return generate_fallback_group_response(character_keys, problem_text, username)
    except Exception as e:
        print("Ошибка группового запроса:", e)
        return generate_fallback_group_response(character_keys, problem_text, username)

def generate_fallback_group_response(character_keys, problem_text, username):
    """Fallback метод для группового ответа"""
    responses = []
    for key in character_keys[:3]:
        response = ask_deepseek(key, problem_text, username)
        char_name = CHARACTERS[key]["name"]
        responses.append(f"**{char_name}:**\n{response}")
    
    combined = "\n\n---\n\n".join(responses)
    return f"💫 **Командный совет от Сейлор Воинов!** ✨\n\n{combined}\n\n🌟 *Вместе мы сила!* 💖"

# === ENDPOINT ДЛЯ МИНИ-ПРИЛОЖЕНИЯ ===
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
        character_keys = character_keys[:4]
        
        print(f"🌙 Групповой запрос от {username} с персонажами: {character_keys}")
        advice = ask_deepseek_group(character_keys, problem, username)
        
        character_names = [CHARACTERS[key]["name"] for key in character_keys if key in CHARACTERS]
        team_names = ", ".join(character_names)
        advice += f"\n\n💖 *С любовью, твоя команда: {team_names}!* ✨"
        
    else:
        # Одиночный ответ
        advice = ask_deepseek(character, problem, username)
        advice += f"\n\n💖 *С любовью, {CHARACTERS[character]['name']}!*"

    # Отправка в Telegram если есть chat_id
    if chat_id:
        try:
            # ИСПРАВЛЕНИЕ: используем новую функцию с картинкой
            if answer_type == "single":
                send_message_with_photo(chat_id, advice, character)
            else:
                # Для группового ответа отправляем без конкретной картинки
                bot.send_message(chat_id, advice, parse_mode='Markdown')
        except Exception as e:
            print(f"Ошибка отправки в Telegram: {e}")

    return jsonify({"ok": True, "advice": advice})

# === TELEGRAM BOT HANDLERS С МУЛЬТИВЫБОРОМ ===
@bot.message_handler(commands=['start'])
def start(message):
    user_states[message.chat.id] = {
        "name": None, 
        "characters": [],  # теперь храним список выбранных персонажей
        "mode": None  # 'single' или 'group'
    }
    bot.send_message(message.chat.id, "🌙 Привет, во имя Луны! 💫 Как тебя зовут?", parse_mode='Markdown')
    bot.register_next_step_handler(message, get_name)

def get_name(message):
    name = message.text.strip()
    user_states[message.chat.id]["name"] = name

    text = f"💖 Рада знакомству, {name}! 🌙\n\nВыбери тип совета:"
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    btn_single = types.InlineKeyboardButton("👤 Совет от одного", callback_data="mode_single")
    btn_group = types.InlineKeyboardButton("👥 Командный совет", callback_data="mode_group")
    
    markup.add(btn_single, btn_group)
    
    bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("mode_"))
def choose_mode(call):
    mode = call.data.split("_")[1]  # 'single' или 'group'
    user_states[call.message.chat.id]["mode"] = mode
    
    if mode == "single":
        text = "👤 Выбери одного советчика:"
        markup = create_characters_markup(mode="single")
    else:
        text = "👥 Выбери до 4 персонажей для командного совета (отмечай галочками):"
        markup = create_characters_markup(mode="group")
    
    bot.edit_message_text(
        text, 
        call.message.chat.id, 
        call.message.message_id,
        parse_mode='Markdown',
        reply_markup=markup
    )

def create_characters_markup(mode="single"):
    """Создает клавиатуру для выбора персонажей"""
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    buttons = []
    for key, data in CHARACTERS.items():
        emoji = "" if mode == "group" else ""
        btn_text = f"{emoji}{data['name']}"
        callback_data = f"char_{key}"
        buttons.append(types.InlineKeyboardButton(btn_text, callback_data=callback_data))
    
    # Добавляем кнопки построчно
    for i in range(0, len(buttons), 2):
        if i + 1 < len(buttons):
            markup.add(buttons[i], buttons[i+1])
        else:
            markup.add(buttons[i])
    
    # Кнопка подтверждения для группового режима
    if mode == "group":
        markup.add(types.InlineKeyboardButton("🚀 Получить командный совет", callback_data="confirm_group"))
    
    return markup

@bot.callback_query_handler(func=lambda call: call.data.startswith("char_"))
def choose_character(call):
    char_key = call.data.split("_")[1]
    user_state = user_states[call.message.chat.id]
    mode = user_state["mode"]
    
    if mode == "single":
        # Одиночный выбор - сразу устанавливаем персонажа
        user_state["characters"] = [char_key]
        name = CHARACTERS[char_key]["name"]
        bot.answer_callback_query(call.id, f"✨ {name} теперь с тобой!")
        
        bot.edit_message_text(
            f"💫 {name} готов(а) выслушать. Расскажи, что тебя беспокоит 🌙",
            call.message.chat.id,
            call.message.message_id,
            parse_mode='Markdown'
        )
        
    else:
        # Групповой выбор - добавляем/убираем из списка
        current_chars = user_state["characters"]
        
        if char_key in current_chars:
            current_chars.remove(char_key)
            action = "❌"
        else:
            if len(current_chars) < 4:
                current_chars.append(char_key)
                action = "✅"
            else:
                bot.answer_callback_query(call.id, "🚫 Можно выбрать до 4 персонажей!")
                return
        
        user_state["characters"] = current_chars
        
        # Обновляем клавиатуру
        markup = create_characters_markup(mode="group")
        count_text = f" ({len(current_chars)}/4)" if current_chars else ""
        
        bot.edit_message_text(
            f"👥 Выбери до 4 персонажей для командного совета{count_text}:",
            call.message.chat.id,
            call.message.message_id,
            parse_mode='Markdown',
            reply_markup=markup
        )
        
        char_name = CHARACTERS[char_key]["name"]
        bot.answer_callback_query(call.id, f"{action} {char_name}")

@bot.callback_query_handler(func=lambda call: call.data == "confirm_group")
def confirm_group(call):
    user_state = user_states[call.message.chat.id]
    selected_chars = user_state["characters"]
    
    if not selected_chars:
        bot.answer_callback_query(call.id, "🚫 Выбери хотя бы одного персонажа!")
        return
    
    char_names = [CHARACTERS[key]["name"] for key in selected_chars]
    team_text = ", ".join(char_names)
    
    bot.edit_message_text(
        f"👥 **Команда собрана!** ✨\n\n{team_text} готовы выслушать тебя!\n\nРасскажи, что тебя беспокоит 🌙",
        call.message.chat.id,
        call.message.message_id,
        parse_mode='Markdown'
    )

@bot.message_handler(content_types=['text'])
def get_problem(message):
    state = user_states.get(message.chat.id)
    if not state or not state.get("characters"):
        bot.send_message(message.chat.id, "🌙 Начни с команды /start ✨")
        return

    username = state["name"]
    character_keys = state["characters"]
    mode = state.get("mode", "single")

    thinking_text = "🌕 Советчица обдумывает ответ... 💫"
    if mode == "group":
        thinking_text = "🌕 Команда обсуждает твой вопрос... 💫"
    
    thinking = bot.send_message(message.chat.id, thinking_text)

    if mode == "group" and len(character_keys) > 1:
        # Групповой ответ
        advice = ask_deepseek_group(character_keys, message.text.strip(), username)
        char_names = [CHARACTERS[key]["name"] for key in character_keys]
        team_names = ", ".join(char_names)
        advice += f"\n\n💖 *С любовью, твоя команда: {team_names}!* ✨"
        
        # Для группового ответа отправляем без конкретной картинки
        try: 
            bot.delete_message(message.chat.id, thinking.message_id)
        except: 
            pass
        bot.send_message(message.chat.id, advice, parse_mode='Markdown')
        
    else:
        # Одиночный ответ
        char_key = character_keys[0]
        advice = ask_deepseek(char_key, message.text.strip(), username)
        advice += f"\n\n💖 *С любовью, {CHARACTERS[char_key]['name']}!*"

        try: 
            bot.delete_message(message.chat.id, thinking.message_id)
        except: 
            pass
        
        # ИСПРАВЛЕНИЕ: используем новую функцию с картинкой для одиночного ответа
        send_message_with_photo(message.chat.id, advice, char_key)

    # Предлагаем начать заново
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔄 Новый вопрос", callback_data="restart"))
    
    end_text = "✨ Лунная магия всегда с тобой! 🌙"
    if mode == "group":
        end_text = "🌟 Вместе мы сила! 💫"
        
    bot.send_message(message.chat.id, end_text, parse_mode='Markdown', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "restart")
def restart(call):
    start(call.message)

@bot.message_handler(commands=['app'])
def open_app(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    web_app = types.WebAppInfo("https://sailor-moon-psycho-help.vercel.app")
    btn = types.KeyboardButton("🌙 Открыть мини-приложение", web_app=web_app)
    markup.add(btn)
    bot.send_message(message.chat.id, "✨ Открой мини-приложение с расширенными функциями!", reply_markup=markup)

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

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "sailor-moon-bot"})

if __name__ == "__main__":
    print("🌙 Sailor Moon Bot запускается... ✨")
    
    # Проверяем обязательные переменные
    if not BOT_TOKEN:
        print("❌ ОШИБКА: BOT_TOKEN не установлен!")
    if not DEEPSEEK_API_KEY:
        print("❌ ОШИБКА: DEEPSEEK_API_KEY не установлен!")
    
    set_webhook()
    port = int(os.getenv("PORT", 5000))
    
    print(f"🚀 Сервер запускается на порту {port}")
    print(f"🌐 Webhook URL: {VERCEL_URL}/webhook" if VERCEL_URL else "⚠️ Webhook не настроен")
    
    app.run(host='0.0.0.0', port=port, debug=False)
