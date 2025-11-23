import os
import random
import requests
import telebot
from flask import Flask, request, jsonify
from flask_cors import CORS
from telebot import types

# === НАСТРОЙКИ ===
BOT_TOKEN = os.getenv("BOT_TOKEN")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
VERCEL_URL = os.getenv("VERCEL_URL")
PORT = int(os.getenv("PORT", 5000))

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# 🛠 ИСПРАВЛЕНИЕ: Разрешаем запросы с любого источника (звездочка *)
CORS(app, resources={r"/*": {"origins": "*"}})

# === ХРАНЕНИЕ СОСТОЯНИЙ ===
user_states = {}

# === ДАННЫЕ ПЕРСОНАЖЕЙ (Полный список из твоего файла) ===
CHARACTERS = {
    "usagi": {
        "name": "Усаги Цукино",
        "forms": {
            "human": {"title": "Усаги Цукино 👧", "image": "https://i.pinimg.com/736x/a4/47/c4/a447c423d530b9cac4612a9f71c96ddc.jpg"},
            "sailor": {"title": "Сейлор Мун 🌙", "image": "https://i.pinimg.com/736x/55/ff/32/55ff32a1d1a2e86ff41d76068672e108.jpg"},
            "super": {"title": "Супер Сейлор Мун 💫", "image": "https://i.pinimg.com/736x/56/7b/38/567b38a7e0d7729573f997ded2448d5e.jpg"},
            "eternal": {"title": "Вечная Сейлор Мун ✨", "image": "https://i.pinimg.com/1200x/a1/e5/52/a1e552f9276025313b66b8f3a36a3c44.jpg"}
        },
        "styles": {
            "human": "Ты — обычная школьница Усаги Цукино. Немного неуклюжая, эмоциональная, добрая. Говори как девочка-подросток, используй простые слова, смайлики. Не используй сложные термины.",
            "sailor": "Ты — Сейлор Мун, защитница любви и справедливости! Говори с уверенностью и достоинством, но сохраняй доброту. Используй возвышенные фразы про луну.",
            "super": "Ты — Супер Сейлор Мун. Твоя сила возросла. Говори с ещё большей уверенностью и мудростью. Используй образы сияния и кристаллов.",
            "eternal": "Ты — Вечная Сейлор Мун. Ты достигла пика силы. Говори с космической мудростью, сохраняя тепло. Используй образы вечности и звёзд."
        }
    },
    "ami": {
        "name": "Ами Мидзуно",
        "forms": {
            "human": {"title": "Ами Мидзуно 📚", "image": "https://i.pinimg.com/736x/0b/07/f9/0b07f95abbceecf7922c44ac333a48f2.jpg"},
            "sailor": {"title": "Сейлор Меркурий 💧", "image": "https://i.pinimg.com/736x/b1/61/1a/b1611addcf1190d311218c22614e1e36.jpg"}
        },
        "styles": {
            "human": "Ты — Ами Мидзуно. Говори тихо, вежливо, логично. Используй научные термины, но оставайся доброй.",
            "sailor": "Ты — Сейлор Меркурий. Говори спокойно и аналитически. Ты — мозг команды. Используй компьютерные метафоры."
        }
    },
    "rei": {
        "name": "Рей Хино",
        "forms": {
            "human": {"title": "Рей Хино 🔥", "image": "https://i.pinimg.com/736x/d7/9c/61/d79c617912ae0e4d510660c32c971227.jpg"},
            "sailor": {"title": "Сейлор Марс 🔥", "image": "https://i.pinimg.com/736x/7f/e6/e8/7fe6e8b47812f4778d229903c1776744.jpg"}
        },
        "styles": {
            "human": "Ты — Рей Хино. Говори с достоинством, иногда резко и прямо, но справедливо. Ты жрица храма.",
            "sailor": "Ты — Сейлор Марс. Говори энергично, с огнём в голосе. Твои слова полны решимости. Используй образы огня."
        }
    },
    "minako": {
        "name": "Минако Айно",
        "forms": {
            "human": {"title": "Минако Айно 💛", "image": "https://i.pinimg.com/736x/68/68/52/6868521a4cf61d75b40772b6f13c0504.jpg"},
            "sailor": {"title": "Сейлор Венера 💖", "image": "https://i.pinimg.com/1200x/bb/e9/6e/bbe96e1b50292f72dab46e16dfd5f632.jpg"}
        },
        "styles": {
            "human": "Ты — Минако Айно. Говори оптимистично, с юмором, шути. Ты мечтаешь стать идолом.",
            "sailor": "Ты — Сейлор Венера, лидер внутренней команды. Говори с уверенностью лидера, используй образы любви и красоты."
        }
    },
    "makoto": {
        "name": "Макото Кино",
        "forms": {
            "human": {"title": "Макото Кино 🌿", "image": "https://i.pinimg.com/736x/49/27/8d/49278da7f93a6028a0a3d05bbd43fd22.jpg"},
            "sailor": {"title": "Сейлор Юпитер ⚡", "image": "https://i.pinimg.com/736x/84/f8/c0/84f8c01989fa310f2ca46bd8bcd58af3.jpg"}
        },
        "styles": {
            "human": "Ты — Макото Кино. Говори по-матерински тепло, заботливо. Ты любишь готовить и защищать слабых.",
            "sailor": "Ты — Сейлор Юпитер. Говори с силой и решимостью. Твои слова вселяют чувство безопасности. Используй образы грома."
        }
    },
    "hotaru": {
        "name": "Хотару Томоэ",
        "forms": {
            "human": {"title": "Хотару Томоэ 🌙", "image": "https://i.pinimg.com/736x/62/e8/61/62e861ea332c0bf8dafd00fd4e9571d9.jpg"},
            "sailor": {"title": "Сейлор Сатурн 🌑", "image": "https://i.pinimg.com/736x/65/e3/95/65e3950cb55aaffbfd443ef8d5f3ae2a.jpg"}
        },
        "styles": {
            "human": "Ты — Хотару Томоэ. Говори спокойно, мягко, немного загадочно. Ты мудра не по годам.",
            "sailor": "Ты — Сейлор Сатурн. Говори с космической мудростью, спокойно и фаталистично. Ты понимаешь циклы жизни и смерти."
        }
    },
    "setsuna": {
        "name": "Сецуна Мейо",
        "forms": {
            "human": {"title": "Сецуна Мейо ⏳", "image": "https://i.pinimg.com/736x/89/bf/f4/89bff47fee6011a503b18c274a0370a5.jpg"},
            "sailor": {"title": "Сейлор Плутон 🕰️", "image": "https://i.pinimg.com/736x/d4/8b/89/d48b8992dfac715b928af9d974d4c37c.jpg"}
        },
        "styles": {
            "human": "Ты — Сецуна Мейо. Говори с достоинством взрослой женщины, проницательно.",
            "sailor": "Ты — Сейлор Плутон, страж Времени. Говори с мудростью тысячелетий, строго но справедливо."
        }
    },
    "haruka": {
        "name": "Харука Тэнно",
        "forms": {
            "human": {"title": "Харука Тэнно 🌟", "image": "https://i.pinimg.com/736x/a8/c9/9e/a8c99e3558ea0caf592cb06c1339f720.jpg"},
            "sailor": {"title": "Сейлор Уран 🌪️", "image": "https://i.pinimg.com/1200x/ec/bd/fd/ecbdfd6392394b2d66fa68729eeb5948.jpg"}
        },
        "styles": {
            "human": "Ты — Харука Тэнно. Говори уверенно, немного дерзко, флиртующе, но искренне.",
            "sailor": "Ты — Сейлор Уран. Говори с силой ветра, решительно. Ты готова на всё ради миссии."
        }
    },
    "michiru": {
        "name": "Мичиру Кайо",
        "forms": {
            "human": {"title": "Мичиру Кайо 🌊", "image": "https://i.pinimg.com/736x/a4/fe/e9/a4fee98a8f01e8a377a70759edbfc5df.jpg"},
            "sailor": {"title": "Сейлор Нептун 🎻", "image": "https://i.pinimg.com/736x/ef/a9/72/efa97290c250e97924777c4551120f60.jpg"}
        },
        "styles": {
            "human": "Ты — Мичиру Кайо. Говори изысканно, элегантно, метафорично. Ты леди.",
            "sailor": "Ты — Сейлор Нептун. Говори с грацией океана, глубоко и интуитивно."
        }
    },
    "chibiusa": {
        "name": "Чибиуса",
        "forms": {
            "human": {"title": "Чибиуса ✨", "image": "https://i.pinimg.com/736x/40/74/49/4074490084d46e4d173179fe03427d2b.jpg"},
            "sailor": {"title": "Сейлор Чиби-Мун 💕", "image": "https://i.pinimg.com/736x/09/89/00/098900bcc276be04da9e30b7cf3a6007.jpg"}
        },
        "styles": {
            "human": "Ты — Чибиуса. Говори как капризная, но добрая девочка. Используй много смайликов.",
            "sailor": "Ты — Сейлор Чиби-Мун. Говори с детской отвагой. Ты хочешь быть как мама (Усаги)."
        }
    },
    "mamoru": {
        "name": "Мамору Чиба",
        "forms": {
            "human": {"title": "Мамору Чиба 🌹", "image": "https://i.pinimg.com/736x/68/f4/07/68f4077d2f6944bad32604a96a62f310.jpg"},
            "sailor": {"title": "Такседо Маск 🥶", "image": "https://i.pinimg.com/736x/62/c0/97/62c0978a24a049425d9895a159ca3104.jpg"}
        },
        "styles": {
            "human": "Ты — Мамору Чиба. Говори спокойно, по-взрослому, интеллигентно и с поддержкой.",
            "sailor": "Ты — Такседо Маск. Говори загадочно, короткими и емкими фразами. Ты — опора."
        }
    },
    "seiya": {
        "name": "Сейя Кое",
        "forms": {
            "human": {"title": "Сейя Кое ♂️⭐", "image": "https://i.pinimg.com/736x/fa/44/48/fa4448c6b3b4d06e33e905e34256199b.jpg"},
            "sailor": {"title": "Сейлор Стар Файтер ⭐", "image": "https://i.pinimg.com/736x/7c/f6/11/7cf6111d7e826a5e8008310206683b1e.jpg"}
        },
        "styles": {
            "human": "Ты — Сейя. Говори как "свой парень", дерзко, весело, с драйвом.",
            "sailor": "Ты — Сейлор Стар Файтер. Говори с космической серьезностью, ты ищешь свою принцессу."
        }
    },
    "taiki": {
        "name": "Тайки Кое",
        "forms": {
            "human": {"title": "Тайки Кое ♂️📚", "image": "https://i.pinimg.com/736x/9d/cf/05/9dcf05f2328100ef411b710d30ffc465.jpg"},
            "sailor": {"title": "Сейлор Стар Хилер 📚", "image": "https://i.pinimg.com/736x/32/1f/c6/321fc67961d968c73c972616e53721af.jpg"}
        },
        "styles": {
            "human": "Ты — Тайки. Говори очень умно, иногда занудно и с иронией. Ты интеллектуал.",
            "sailor": "Ты — Сейлор Стар Хилер. Говори как мудрый целитель, холодно но профессионально."
        }
    },
    "yaten": {
        "name": "Ятэн Кое",
        "forms": {
            "human": {"title": "Ятен ♂️🎭", "image": "https://i.pinimg.com/736x/68/b2/00/68b2006277d4c56dde09e0eb1cce61e0.jpg"},
            "sailor": {"title": "Сейлор Стар Мейкер 🎭", "image": "https://i.pinimg.com/736x/90/42/a3/9042a33ae40ccc635e909c2ba00449fb.jpg"}
        },
        "styles": {
            "human": "Ты — Ятен. Говори цинично, устало от фанатов, но с творческой ноткой.",
            "sailor": "Ты — Сейлор Стар Мейкер. Говори поэтично, создавая образы."
        }
    }
}

BACKUP_RESPONSES = [
    "🌙 Лунная призма, дай мне силу! Сейчас помехи в эфире, но знай: всё будет хорошо! ✨",
    "💫 Звёзды говорят, что ты справишься, даже если я сейчас не могу подобрать слов.",
    "🎀 Главное — верь в себя! Я с тобой!"
]

# === УСТАНОВКА WEBHOOK ===
def set_webhook():
    if VERCEL_URL:
        webhook_url = f"{VERCEL_URL}/webhook"
        try:
            bot.remove_webhook()
            bot.set_webhook(url=webhook_url)
            print(f"🌙 Webhook установлен: {webhook_url}")
        except Exception as e:
            print(f"❌ Ошибка установки webhook: {e}")

# === DEEPSEEK SINGLE ===
def ask_deepseek(character_key, form_key, problem_text, username):
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    char_data = CHARACTERS.get(character_key, CHARACTERS["usagi"])
    if form_key not in char_data["forms"]:
        form_key = list(char_data["forms"].keys())[0]

    style = char_data["styles"].get(form_key, char_data["styles"].get("human", ""))

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "HTTP-Referer": "https://telegram.org",
        "X-Title": "SailorMoonBot"
    }

    # Промпт улучшен: запрет 3 лица, Markdown
    system_prompt = (
        f"Ты отыгрываешь роль: {style}\n"
        f"Твоя задача: дать психологический совет пользователю {username}.\n"
        f"ПРАВИЛА:\n"
        f"1. Обращайся на 'ты'.\n"
        f"2. НИКОГДА не говори о себе в 3-м лице (не пиши '{char_data['name']} думает', пиши 'Я думаю').\n"
        f"3. Используй Markdown для выделения (**жирный**, *курсив*).\n"
        f"4. Ответ добрый, до 150 слов."
    )

    payload = {
        "model": "deepseek/deepseek-chat",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"{username} говорит: {problem_text}"}
        ],
        "max_tokens": 300,
        "temperature": 0.8
    }

    try:
        r = requests.post(url, headers=headers, json=payload, timeout=20)
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"]
        print(f"API Error: {r.text}")
        return random.choice(BACKUP_RESPONSES)
    except Exception as e:
        print(f"Req Error: {e}")
        return random.choice(BACKUP_RESPONSES)

# === DEEPSEEK GROUP ===
def ask_deepseek_group(character_keys, problem_text, username):
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    chars_info = []
    for key in character_keys:
        if key in CHARACTERS:
            form = "sailor" if "sailor" in CHARACTERS[key]["forms"] else "human"
            name = CHARACTERS[key]["forms"][form]["title"]
            style = CHARACTERS[key]["styles"].get(form, "")
            chars_info.append(f"- {name}: {style}")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "HTTP-Referer": "https://telegram.org",
        "X-Title": "SailorMoonBot"
    }

    system_prompt = (
        f"Ты симулируешь диалог команды Сейлор Воинов.\n"
        f"Персонажи: {', '.join([c.split(':')[0] for c in chars_info])}\n"
        f"Стили: {' '.join(chars_info)}\n"
        f"Задача: Поддержать {username}, у которого проблема: {problem_text}\n"
        f"Формат ответа:\n"
        f"**Имя**: Реплика\n\n"
        f"**Имя**: Реплика\n"
        f"В конце общее пожелание. Используй Markdown."
    )

    payload = {
        "model": "deepseek/deepseek-chat",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "Девочки, помогите советом!"}
        ],
        "max_tokens": 500,
        "temperature": 0.9
    }

    try:
        r = requests.post(url, headers=headers, json=payload, timeout=25)
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"]
        return random.choice(BACKUP_RESPONSES)
    except:
        return random.choice(BACKUP_RESPONSES)

# === API ENDPOINT ДЛЯ WEBAPP ===
@app.route('/ask', methods=['POST'])
def ask_endpoint():
    try:
        data = request.json
        username = data.get("username", "друг")
        problem = data.get("problem", "")
        answer_type = data.get("answer_type", "single")
        
        if not problem:
            return jsonify({"ok": False, "error": "Нет описания проблемы"}), 400

        advice = ""
        if answer_type == 'group':
            keys = data.get("character", "usagi").split(',')
            advice = ask_deepseek_group(keys, problem, username)
        else:
            char = data.get("character", "usagi")
            form = data.get("form", "human")
            advice = ask_deepseek(char, form, problem, username)

        return jsonify({"ok": True, "advice": advice})
    except Exception as e:
        print(f"Endpoint Error: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500

# === TELEGRAM BOT HANDLERS ===
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🌙 Открыть Приложение", web_app=types.WebAppInfo("https://sailor-moon-psycho-help.vercel.app")))
    bot.send_message(message.chat.id, "Нажми кнопку ниже, чтобы поговорить с Сейлор Мун! 👇", reply_markup=markup)

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return 'OK', 200
    return 'Error', 403

@app.route('/')
def index():
    return 'Moon Bot Active 🌙'

if __name__ == "__main__":
    set_webhook()
    app.run(host='0.0.0.0', port=PORT)
