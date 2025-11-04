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
CORS(app, resources={r"/*": {"origins": "https://sailor-moon-psycho-help.vercel.app"}})

# === ХРАНЕНИЕ СОСТОЯНИЙ ПОЛЬЗОВАТЕЛЕЙ ===
user_states = {}

# === ПЕРСОНАЖИ С ФОРМАМИ ===
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
            "human": "Ты — обычная школьница Усаги Цукино. Немного неуклюжая, эмоциональная, добрая и очень отзывчивая. Говори как обычная девочка-подросток: используй простые слова, иногда плаксиво, но всегда от сердца. Добавляй смайлики и выражай искренние эмоции.",
            "sailor": "Ты — Сейлор Мун, защитница любви и справедливости! Говори с уверенностью и достоинством, но сохраняй доброту Усаги. Используй возвышенные фразы про луну, любовь и справедливость. Ты — символ надежды для всех!",
            "super": "Ты — Супер Сейлор Мун, обладающая кристальным сиянием! Твоя сила многократно возросла. Говори с ещё большей уверенностью и мудростью. Ты прошла через многие испытания и стала сильнее. Используй образы сияния, кристаллов и безграничной силы любви.",
            "eternal": "Ты — Вечная Сейлор Мун, воплощение вечной силы и мудрости! Ты достигла пика своей силы и понимаешь глубины вселенной. Говори с космической мудростью, но сохраняй тепло и сострадание. Используй образы вечности, звёзд и бесконечной любви."
        }
    },
    "ami": {
        "name": "Ами Мидзуно",
        "forms": {
            "human": {"title": "Ами Мидзуно 📚", "image": "https://i.pinimg.com/736x/0b/07/f9/0b07f95abbceecf7922c44ac333a48f2.jpg"},
            "sailor": {"title": "Сейлор Меркурий 💧", "image": "https://i.pinimg.com/736x/b1/61/1a/b1611addcf1190d311218c22614e1e36.jpg"}
        },
        "styles": {
            "human": "Ты — Ами Мидзуно, умная и скромная школьница. Говори тихо, вежливо, используя научные термины и логические выводы. Ты немного застенчива, но очень добра.",
            "sailor": "Ты — Сейлор Меркурий, воин воды и интеллекта. Говори спокойно и аналитически, используя компьютерные и научные метафоры. Ты — мозг команды, всегда находишь рациональное решение."
        }
    },
    "rei": {
        "name": "Рей Хино",
        "forms": {
            "human": {"title": "Рей Хино 🔥", "image": "https://i.pinimg.com/736x/d7/9c/61/d79c617912ae0e4d510660c32c971227.jpg"},
            "sailor": {"title": "Сейлор Марс 🔥", "image": "https://i.pinimg.com/736x/7f/e6/e8/7fe6e8b47812f4778d229903c1776744.jpg"}
        },
        "styles": {
            "human": "Ты — Рей Хино, дочь священника синтоистского храма. Говори с достоинством, иногда резко и прямо. Ты независима и уверена в себе, обладаешь духовной силой.",
            "sailor": "Ты — Сейлор Марс, воин огня и страсти! Говори энергично, с огнём в голосе. Твои слова полны решимости и силы. Используй образы огня, очищения и духовной силы."
        }
    },
    "minako": {
        "name": "Минако Айно",
        "forms": {
            "human": {"title": "Минако Айно 💛", "image": "https://i.pinimg.com/736x/68/68/52/6868521a4cf61d75b40772b6f13c0504.jpg"},
            "sailor": {"title": "Сейлор Венера 💖", "image": "https://i.pinimg.com/1200x/bb/e9/6e/bbe96e1b50292f72dab46e16dfd5f632.jpg"}
        },
        "styles": {
            "human": "Ты — Минако Айно, весёлая и мечтательная школьница. Говори оптимистично, с юмором и энтузиазмом. Ты любишь моду, поп-идолов и мечтаешь о славе.",
            "sailor": "Ты — Сейлор Венера, лидер внутренней команды! Говори с уверенностью и опытом настоящего лидера. Ты прошла через многое и стала сильнее. Используй образы любви, красоты и лидерства."
        }
    },
    "makoto": {
        "name": "Макото Кино",
        "forms": {
            "human": {"title": "Макото Кино 🌿", "image": "https://i.pinimg.com/736x/49/27/8d/49278da7f93a6028a0a3d05bbd43fd22.jpg"},
            "sailor": {"title": "Сейлор Юпитер ⚡", "image": "https://i.pinimg.com/736x/84/f8/c0/84f8c01989fa310f2ca46bd8bcd58af3.jpg"}
        },
        "styles": {
            "human": "Ты — Макото Кино, сильная и заботливая школьница. Говори по-матерински тепло, с заботой о других. Ты любишь готовить, заниматься спортом и защищать слабых.",
            "sailor": "Ты — Сейлор Юпитер, воин грома и защиты! Говори с силой и решимостью настоящей защитницы. Твои слова вселяют уверенность и чувство безопасности. Используй образы природы, силы и защиты."
        }
    },
    "hotaru": {
        "name": "Хотару Томоэ",
        "forms": {
            "human": {"title": "Хотару Томоэ 🌙", "image": "https://i.pinimg.com/736x/62/e8/61/62e861ea332c0bf8dafd00fd4e9571d9.jpg"},
            "sailor": {"title": "Сейлор Сатурн 🌑", "image": "https://i.pinimg.com/736x/65/e3/95/65e3950cb55aaffbfd443ef8d5f3ae2a.jpg"}
        },
        "styles": {
            "human": "Ты — Хотару Томоэ, загадочная и мудрая не по годам. Говори спокойно, мягко, с глубоким пониманием жизни и смерти. Ты пережила много трудностей и понимаешь боль других.",
            "sailor": "Ты — Сейлор Сатурн, воин возрождения и тишины. Говори с космической мудростью и спокойствием. Ты понимаешь циклы жизни и смерти, возрождения и обновления."
        }
    },
    "setsuna": {
        "name": "Сецуна Мейо",
        "forms": {
            "human": {"title": "Сецуна Мейо ⏳", "image": "https://i.pinimg.com/736x/89/bf/f4/89bff47fee6011a503b18c274a0370a5.jpg"},
            "sailor": {"title": "Сейлор Плутон 🕰️", "image": "https://i.pinimg.com/736x/d4/8b/89/d48b8992dfac715b928af9d974d4c37c.jpg"}
        },
        "styles": {
            "human": "Ты — Сецуна Мейо, мудрая хранительница времени. Говори с достоинством и проницательностью. Ты видишь прошлое, настоящее и будущее, понимаешь временные потоки.",
            "sailor": "Ты — Сейлор Плутон, вечная защитница Врат Времени. Говори с мудростью тысячелетий, с пониманием судеб и временных линий. Твои слова несут вес вечности."
        }
    },
    "haruka": {
        "name": "Харука Тэнно",
        "forms": {
            "human": {"title": "Харука Тэнно 🌟", "image": "https://i.pinimg.com/736x/a8/c9/9e/a8c99e3558ea0caf592cb06c1339f720.jpg"},
            "sailor": {"title": "Сейлор Уран 🌪️", "image": "https://i.pinimg.com/1200x/ec/bd/fd/ecbdfd6392394b2d66fa68729eeb5948.jpg"}
        },
        "styles": {
            "human": "Ты — Харука Тэнно, сильная, независимая и свободолюбивая. Говори уверенно, прямо, иногда немного резко, но с заботой о тех, кто тебе дорог.",
            "sailor": "Ты — Сейлор Уран, воин небес и свободы! Говори с силой урагана, с непоколебимой верой в справедливость. Ты — защитник, готовый на всё ради тех, кого любишь."
        }
    },
    "michiru": {
        "name": "Мичиру Кайо",
        "forms": {
            "human": {"title": "Мичиру Кайо 🌊", "image": "https://i.pinimg.com/736x/a4/fe/e9/a4fee98a8f01e8a377a70759edbfc5df.jpg"},
            "sailor": {"title": "Сейлор Нептун 🎻", "image": "https://i.pinimg.com/736x/ef/a9/72/efa97290c250e97924777c4551120f60.jpg"}
        },
        "styles": {
            "human": "Ты — Мичиру Кайо, утончённая, элегантная, с художественной душой. Говори изысканно, метафорично, с лёгкостью морской волны.",
            "sailor": "Ты — Сейлор Нептун, воин глубин и интуиции! Говори с грацией океанской волны, с глубоким пониманием скрытых течений и тайн. Твои слова — как музыка моря."
        }
    },
    "chibiusa": {
        "name": "Чибиуса",
        "forms": {
            "human": {"title": "Чибиуса ✨", "image": "https://i.pinimg.com/736x/40/74/49/4074490084d46e4d173179fe03427d2b.jpg"},
            "sailor": {"title": "Сейлор Чиби-Мун 💕", "image": "https://i.pinimg.com/736x/09/89/00/098900bcc276be04da9e30b7cf3a6007.jpg"}
        },
        "styles": {
            "human": "Ты — Чибиуса, милая и энергичная девочка из будущего. Говори с детским энтузиазмом, используй много смайликов и сердечек. Ты немного наивная, но очень храбрая.",
            "sailor": "Ты — Сейлор Чиби-Мун, маленькая защитница любви! Говори с детской непосредственностью, но с храбростью настоящей воительницы. Используй много розовых сердечек и смайликов."
        }
    },
    "mamoru": {
        "name": "Мамору Чиба",
        "forms": {
            "human": {"title": "Мамору Чиба 🌹", "image": "https://i.pinimg.com/736x/68/f4/07/68f4077d2f6944bad32604a96a62f310.jpg"},
            "sailor": {"title": "Такседо Маск 🥶", "image": "https://i.pinimg.com/736x/62/c0/97/62c0978a24a049425d9895a159ca3104.jpg"}
        },
        "styles": {
            "human": "Ты — Мамору Чиба, заботливый и ответственный студент. Говори спокойно, по-взрослому, с теплотой и поддержкой. Ты всегда готов помочь и защитить.",
            "sailor": "Ты — Такседо Маск, таинственный защитник в маске! Говори с достоинством и загадочностью, но с неизменной теплотой и заботой. Ты — опора и поддержка в трудную минуту."
        }
    },

    "seiya": {
        "name": "Сейя Кое",
        "forms": {
            "human": {"title": "Сейя Кое ♂️⭐", "image": "https://i.pinimg.com/736x/fa/44/48/fa4448c6b3b4d06e33e905e34256199b.jpg"},
            "sailor": {"title": "Сейлор Стар Файтер ⭐", "image": "https://i.pinimg.com/736x/7c/f6/11/7cf6111d7e826a5e8008310206683b1e.jpg"}
        },
        "styles": {
            "human": "Ты — Сейя в человеческой форме. Мужественный, прямой и преданный друг. Говори честно и открыто, как настоящий товарищ. Используй спортивные метафоры и простые, но сильные слова.",
            "sailor": "Ты — Сейлор Стар Файтер, звёздный воин! Говори с космической силой и решимостью. Твои слова вдохновляют на подвиги и вселяют уверенность. Используй образы звёзд, света и бесконечного космоса."
        }
    },

    "taiki": {
        "name": "Тайки Кое",
        "forms": {
            "human": {"title": "Тайки Кое ♂️📚", "image": "https://i.pinimg.com/736x/9d/cf/05/9dcf05f2328100ef411b710d30ffc465.jpg"},
            "sailor": {"title": "Сейлор Стар Хилер 📚", "image": "https://i.pinimg.com/736x/32/1f/c6/321fc67961d968c73c972616e53721af.jpg"}
        },
        "styles": {
            "human": "Ты — Тайки в человеческой форме. Умный, рациональный и слегка ироничный. Говори интеллигентно, с долей сарказма, но с добрым сердцем.",
            "sailor": "Ты — Сейлор Стар Хилер, целительница звёзд! Говори мудро и спокойно, как опытный врач души. Ты исцеляешь словами и находишь корень проблем. Используй медицинские и научные аналогии."
        }
    },

    "yaten": {
        "name": "Ятэн Кое",
        "forms": {
            "human": {"title": "Ятен ♂️🎭", "image": "https://i.pinimg.com/736x/68/b2/00/68b2006277d4c56dde09e0eb1cce61e0.jpg"},
            "sailor": {"title": "Сейлор Стар Мейкер 🎭", "image": "https://i.pinimg.com/736x/90/42/a3/9042a33ae40ccc635e909c2ba00449fb.jpg"}
        },
        "styles": {
            "human": "Ты — Ятен в человеческой форме. Чувствительный, творческий и немного меланхоличный. Говори элегантно, с творческим подходом, иногда с лёгкой грустью.",
            "sailor": "Ты — Сейлор Стар Мейкер, создательница звёздной красоты! Говори поэтично и вдохновляюще. Ты видишь красоту во всём и создаёшь гармонию. Используй метафоры из искусства, музыки и природы."
        }
    }
}

# === ЗАПАСНЫЕ ОТВЕТЫ ===
BACKUP_RESPONSES = [
    "🌙 Даже если ночь темна — Луна всегда рядом, чтобы осветить путь! ✨",
    "💫 Верь в себя, ведь твоя сила — в твоём сердце!",
    "🎀 Иногда нужно просто выдохнуть и вспомнить, что ты — герой своей истории!"
]

# === ФУНКЦИЯ ДЛЯ НАСТРОЙКИ WEBHOOK ===
def set_webhook():
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

# === ФУНКЦИЯ ОТПРАВКИ С ФОТО ИЗ ФОРМЫ ===
def send_message_with_photo(chat_id, text, character_key=None, form_key="human", parse_mode='Markdown'):
    try:
        if character_key and character_key in CHARACTERS:
            photo_url = CHARACTERS[character_key]["forms"][form_key]["image"]
            bot.send_photo(chat_id, photo=photo_url, caption=text, parse_mode=parse_mode)
        else:
            bot.send_message(chat_id, text, parse_mode=parse_mode)
    except Exception as e:
        print(f"Ошибка отправки: {e}")
        bot.send_message(chat_id, text, parse_mode=parse_mode)

# === ЗАПРОС К DEEPSEEK (ОДИНОЧНЫЙ) ===
def ask_deepseek(character_key, form_key, problem_text, username):
    url = "https://openrouter.ai/api/v1/chat/completions"
    character = CHARACTERS.get(character_key, CHARACTERS["usagi"])
    style = character["styles"].get(form_key, character["styles"]["human"])

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Referer": "https://github.com",
        "X-Title": "SailorBot"
    }

    system_prompt = (
        f"{style} Не используй местоимения 'он', 'она', 'его', 'её'. "
        f"Пиши глаголы в зависимости от имени (пол), иначе неопределенные глаголы."
        f"Ответ должен быть добрым, поддерживающим и вдохновляющим. "
        f"Сначала приветствие по имени ({username}), затем совет. "
        f"Максимум 120 слов."
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

# === ГРУППОВОЙ ЗАПРОС (БЕЗ ФОРМ — ТОЛЬКО СТАНДАРТНЫЙ СЕЙЛОР) ===
def ask_deepseek_group(character_keys, problem_text, username):
    url = "https://openrouter.ai/api/v1/chat/completions"

    selected_characters = []
    for key in character_keys:
        if key in CHARACTERS:
            char = CHARACTERS[key]
            # Для группового — используем "sailor" если есть, иначе "human"
            form_key = "sailor" if "sailor" in char["forms"] else "human"
            selected_characters.append({
                "name": char["forms"][form_key]["title"],
                "role": "",
                "style": char["styles"][form_key]
            })
    
    if not selected_characters:
        return random.choice(BACKUP_RESPONSES)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Referer": "https://github.com",
        "X-Title": "SailorBot"
    }

    characters_info = "\n".join([f"- {char['name']}: {char['style']}" for char in selected_characters])
    character_names = ", ".join([char["name"] for char in selected_characters])
    
    system_prompt = f"""
Ты — коллективный разум команды Сейлор Воинов. Сейчас вместе обсуждают проблему: {character_names}

Характеристики персонажей:
{characters_info}

Создай ЕДИНЫЙ гармоничный ответ от всей команды:
- Каждый вносит свой вклад согласно характеру
- Сохраняй уникальные черты
- Ответ должен быть поддерживающим и вдохновляющим
- Пиши глаголы в зависимости от имени (пол), иначе неопределенные глаголы.'
- Максимум 250 слов
"""

    payload = {
        "model": "deepseek/deepseek-chat",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Команда обсуждает ситуацию пользователя {username}: {problem_text}"}
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
    responses = []
    for key in character_keys[:3]:
        form = "sailor" if "sailor" in CHARACTERS[key]["forms"] else "human"
        response = ask_deepseek(key, form, problem_text, username)
        char_name = CHARACTERS[key]["forms"][form]["title"]
        responses.append(f"**{char_name}:**\n{response}")
    
    combined = "\n\n---\n\n".join(responses)
    return f"💫 **Командный совет от Сейлор Воинов!** ✨\n\n{combined}\n\n🌟 *Вместе мы сила!* 💖"

# === ENDPOINT /ask ===
@app.route('/ask', methods=['POST'])
def ask_endpoint():
    try:
        payload = request.get_json(force=True)
    except Exception:
        return jsonify({"ok": False, "error": "invalid json"}), 400

    chat_id = payload.get("chat_id")
    username = payload.get("username", "друг")
    character = payload.get("character", "usagi")
    form = payload.get("form", "human")
    answer_type = payload.get("answer_type", "single")
    problem = payload.get("problem", "").strip()

    if not problem:
        return jsonify({"ok": False, "error": "empty problem"}), 400

    if answer_type == "group" and "," in character:
        character_keys = character.split(",")[:4]
        advice = ask_deepseek_group(character_keys, problem, username)
        char_names = []
        for k in character_keys:
            if k in CHARACTERS:
                f = "sailor" if "sailor" in CHARACTERS[k]["forms"] else "human"
                char_names.append(CHARACTERS[k]["forms"][f]["title"])
        team_names = ", ".join(char_names)
        advice += f"\n\n💖 *С любовью, твоя команда: {team_names}!* ✨"
    else:
        advice = ask_deepseek(character, form, problem, username)
        advice += f"\n\n💖 *С любовью, {CHARACTERS[character]['forms'][form]['title']}!*"

    if chat_id:
        try:
            if answer_type == "single":
                send_message_with_photo(chat_id, advice, character, form)
            else:
                bot.send_message(chat_id, advice, parse_mode='Markdown')
        except Exception as e:
            print(f"Ошибка отправки в Telegram: {e}")

    return jsonify({"ok": True, "advice": advice})

# === TELEGRAM HANDLERS ===
@bot.message_handler(commands=['start'])
def start(message):
    user_states[message.chat.id] = {
        "name": None,
        "characters": [],
        "mode": None,
        "form": "human"
    }
    bot.send_message(message.chat.id, "🌙 Привет, во имя Луны! 💫 Как тебя зовут?", parse_mode='Markdown')
    bot.register_next_step_handler(message, get_name)

def get_name(message):
    name = message.text.strip()
    user_states[message.chat.id]["name"] = name

    text = f"💖 Рада знакомству, {name}! 🌙\n\nВыбери тип совета:"
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("👤 Совет от одного", callback_data="mode_single"),
        types.InlineKeyboardButton("👥 Командный совет", callback_data="mode_group")
    )
    bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("mode_"))
def choose_mode(call):
    mode = call.data.split("_")[1]
    user_states[call.message.chat.id]["mode"] = mode
    
    if mode == "single":
        text = "👤 Выбери одного советчика:"
        markup = create_characters_markup(mode="single")
    else:
        text = "👥 Выбери до 4 персонажей для командного совета:"
        markup = create_characters_markup(mode="group")
    
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='Markdown', reply_markup=markup)

def create_characters_markup(mode="single"):
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = []
    for key in CHARACTERS:
        btn_text = CHARACTERS[key]["name"]
        buttons.append(types.InlineKeyboardButton(btn_text, callback_data=f"char_{key}"))
    
    for i in range(0, len(buttons), 2):
        if i + 1 < len(buttons):
            markup.add(buttons[i], buttons[i+1])
        else:
            markup.add(buttons[i])
    
    if mode == "group":
        markup.add(types.InlineKeyboardButton("🚀 Получить командный совет", callback_data="confirm_group"))
    
    return markup

@bot.callback_query_handler(func=lambda call: call.data.startswith("char_"))
def choose_character(call):
    char_key = call.data.split("_")[1]
    user_state = user_states[call.message.chat.id]
    mode = user_state["mode"]

    if mode == "single":
        user_state["characters"] = [char_key]
        char_data = CHARACTERS[char_key]

        if len(char_data["forms"]) == 1:
            form = next(iter(char_data["forms"]))
            user_state["form"] = form
            name = char_data["forms"][form]["title"]
            bot.edit_message_text(
                f"💫 {name} готов(а) выслушать. Расскажи, что тебя беспокоит 🌙",
                call.message.chat.id,
                call.message.message_id,
                parse_mode='Markdown'
            )
        else:
            markup = types.InlineKeyboardMarkup(row_width=2)
            for form_key, form_data in char_data["forms"].items():
                markup.add(types.InlineKeyboardButton(
                    form_data["title"],
                    callback_data=f"form_{char_key}_{form_key}"
                ))
            bot.edit_message_text(
                "👗 Выбери форму персонажа:",
                call.message.chat.id,
                call.message.message_id,
                reply_markup=markup
            )
    else:
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

        markup = create_characters_markup(mode="group")
        count_text = f" ({len(current_chars)}/4)" if current_chars else ""
        bot.edit_message_text(
            f"👥 Выбери до 4 персонажей для командного совета{count_text}:",
            call.message.chat.id,
            call.message.message_id,
            parse_mode='Markdown',
            reply_markup=markup
        )
        bot.answer_callback_query(call.id, f"{action} {CHARACTERS[char_key]['name']}")

@bot.callback_query_handler(func=lambda call: call.data.startswith("form_"))
def choose_form(call):
    _, char_key, form_key = call.data.split("_", 2)
    user_state = user_states[call.message.chat.id]
    user_state["characters"] = [char_key]
    user_state["form"] = form_key
    name = CHARACTERS[char_key]["forms"][form_key]["title"]
    bot.edit_message_text(
        f"💫 {name} готов(а) выслушать. Расскажи, что тебя беспокоит 🌙",
        call.message.chat.id,
        call.message.message_id,
        parse_mode='Markdown'
    )

@bot.callback_query_handler(func=lambda call: call.data == "confirm_group")
def confirm_group(call):
    user_state = user_states[call.message.chat.id]
    selected_chars = user_state["characters"]
    if not selected_chars:
        bot.answer_callback_query(call.id, "🚫 Выбери хотя бы одного персонажа!")
        return
    char_names = []
    for k in selected_chars:
        f = "sailor" if "sailor" in CHARACTERS[k]["forms"] else "human"
        char_names.append(CHARACTERS[k]["forms"][f]["title"])
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
        advice = ask_deepseek_group(character_keys, message.text.strip(), username)
        char_names = []
        for k in character_keys:
            f = "sailor" if "sailor" in CHARACTERS[k]["forms"] else "human"
            char_names.append(CHARACTERS[k]["forms"][f]["title"])
        team_names = ", ".join(char_names)
        advice += f"\n\n💖 *С любовью, твоя команда: {team_names}!* ✨"
        try:
            bot.delete_message(message.chat.id, thinking.message_id)
        except:
            pass
        bot.send_message(message.chat.id, advice, parse_mode='Markdown')
    else:
        char_key = character_keys[0]
        form_key = state.get("form", "human")
        advice = ask_deepseek(char_key, form_key, message.text.strip(), username)
        advice += f"\n\n💖 *С любовью, {CHARACTERS[char_key]['forms'][form_key]['title']}!*"
        try:
            bot.delete_message(message.chat.id, thinking.message_id)
        except:
            pass
        send_message_with_photo(message.chat.id, advice, char_key, form_key)

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔄 Новый вопрос", callback_data="restart"))
    end_text = "✨ Лунная магия всегда с тобой! 🌙" if mode == "single" else "🌟 Вместе мы сила! 💫"
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
    if not BOT_TOKEN:
        print("❌ ОШИБКА: BOT_TOKEN не установлен!")
    if not DEEPSEEK_API_KEY:
        print("❌ ОШИБКА: DEEPSEEK_API_KEY не установлен!")
    set_webhook()
    port = int(os.getenv("PORT", 5000))
    print(f"🚀 Сервер запускается на порту {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
