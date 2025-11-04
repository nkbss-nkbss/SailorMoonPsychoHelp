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

# === КАРТИНКИ ===
CHARACTER_IMAGES = {
    # Усаги формы
    "usagi_human": "https://i.pinimg.com/736x/a4/47/c4/a447c423d530b9cac4612a9f71c96ddc.jpg",
    "sailor_moon": "https://i.pinimg.com/736x/55/ff/32/55ff32a1d1a2e86ff41d76068672e108.jpg",
    "super_sailor_moon": "https://i.pinimg.com/736x/56/7b/38/567b38a7e0d7729573f997ded2448d5e.jpg",
    "eternal_sailor_moon": "https://i.pinimg.com/1200x/a1/e5/52/a1e552f9276025313b66b8f3a36a3c44.jpg",
    
    # Ами формы
    "ami_human": "https://i.pinimg.com/736x/0b/07/f9/0b07f95abbceecf7922c44ac333a48f2.jpg",
    "sailor_mercury": "https://i.pinimg.com/736x/b1/61/1a/b1611addcf1190d311218c22614e1e36.jpg",
    "super_sailor_mercury": "https://i.pinimg.com/736x/f1/76/9c/f1769c062c4ba5b250ee6e025f406091.jpg",
    
    # Рей формы
    "rei_human": "https://i.pinimg.com/736x/d7/9c/61/d79c617912ae0e4d510660c32c971227.jpg",
    "sailor_mars": "https://i.pinimg.com/736x/7f/e6/e8/7fe6e8b47812f4778d229903c1776744.jpg",
    "super_sailor_mars": "https://i.pinimg.com/736x/ba/88/57/ba8857689d2c18959f0cb5b52e61679e.jpg",
    
    # Минако формы
    "minako_human": "https://i.pinimg.com/736x/68/68/52/6868521a4cf61d75b40772b6f13c0504.jpg",
    "sailor_venus": "https://i.pinimg.com/1200x/bb/e9/6e/bbe96e1b50292f72dab46e16dfd5f632.jpg",
    "super_sailor_venus": "https://i.pinimg.com/736x/a1/91/3b/a1913b02b9a0b1162743ed4abf65fa3a.jpg",
    
    # Макото формы
    "makoto_human": "https://i.pinimg.com/736x/49/27/8d/49278da7f93a6028a0a3d05bbd43fd22.jpg",
    "sailor_jupiter": "https://i.pinimg.com/736x/84/f8/c0/84f8c01989fa310f2ca46bd8bcd58af3.jpg",
    "super_sailor_jupiter": "https://i.pinimg.com/736x/40/56/ac/4056ac19f4f89722f287d18322da702e.jpg",
    
    # Внешние воины
    "hotaru_human": "https://i.pinimg.com/736x/62/e8/61/62e861ea332c0bf8dafd00fd4e9571d9.jpg",
    "sailor_saturn": "https://i.pinimg.com/736x/65/e3/95/65e3950cb55aaffbfd443ef8d5f3ae2a.jpg",
    
    "setsuna_human": "https://i.pinimg.com/736x/89/bf/f4/89bff47fee6011a503b18c274a0370a5.jpg",
    "sailor_pluto": "https://i.pinimg.com/736x/d4/8b/89/d48b8992dfac715b928af9d974d4c37c.jpg",
    
    "haruka_human": "https://i.pinimg.com/736x/a8/c9/9e/a8c99e3558ea0caf592cb06c1339f720.jpg",
    "sailor_uranus": "https://i.pinimg.com/1200x/ec/bd/fd/ecbdfd6392394b2d66fa68729eeb5948.jpg",
    
    "michiru_human": "https://i.pinimg.com/736x/a4/fe/e9/a4fee98a8f01e8a377a70759edbfc5df.jpg",
    "sailor_neptune": "https://i.pinimg.com/736x/ef/a9/72/efa97290c250e97924777c4551120f60.jpg",
    
    # Чибиуса
    "chibiusa_human": "https://i.pinimg.com/736x/40/74/49/4074490084d46e4d173179fe03427d2b.jpg",
    "sailor_chibi_moon": "https://i.pinimg.com/736x/09/89/00/098900bcc276be04da9e30b7cf3a6007.jpg",
    "super_sailor_chibi_moon": "https://i.pinimg.com/736x/e6/62/a3/e662a3d28775f1eac8a5cdbaf52d36b6.jpg",
    
    # Мамору
    "mamoru_human": "https://i.pinimg.com/736x/68/f4/07/68f4077d2f6944bad32604a96a62f310.jpg",
    "tuxedo_mask": "https://i.pinimg.com/736x/62/c0/97/62c0978a24a049425d9895a159ca3104.jpg",
    
    # Сейлор Старлайтеры
    "seiya_human": "https://i.pinimg.com/736x/fa/44/48/fa4448c6b3b4d06e33e905e34256199b.jpg",
    "sailor_star_fighter": "https://i.pinimg.com/736x/7c/f6/11/7cf6111d7e826a5e8008310206683b1e.jpg",
    
    "taiki_human": "https://i.pinimg.com/736x/9d/cf/05/9dcf05f2328100ef411b710d30ffc465.jpg",
    "sailor_star_healer": "https://i.pinimg.com/736x/32/1f/c6/321fc67961d968c73c972616e53721af.jpg",
    
    "yaten_human": "https://i.pinimg.com/736x/68/b2/00/68b2006277d4c56dde09e0eb1cce61e0.jpg",
    "sailor_star_maker": "https://i.pinimg.com/736x/90/42/a3/9042a33ae40ccc635e909c2ba00449fb.jpg"
}

# === ЗАПАСНЫЕ ОТВЕТЫ ===
BACKUP_RESPONSES = [
    "🌙 Даже если ночь темна — Луна всегда рядом, чтобы осветить путь! ✨",
    "💫 Верь в себя, ведь твоя сила — в твоём сердце!",
    "🎀 Иногда нужно просто выдохнуть и вспомнить, что ты — герой своей истории!"
]

# === ПЕРСОНАЖИ С ФОРМАМИ ===
CHARACTERS = {
    # === УСАГИ ФОРМЫ ===
    "usagi_human": {
        "name": "Усаги Цукино 👧", 
        "style": "Ты — обычная школьница Усаги Цукино. Немного неуклюжая, эмоциональная, добрая и очень отзывчивая. Говори как обычная девочка-подросток: используй простые слова, иногда плаксиво, но всегда от сердца.",
        "role": "обычная школьница",
        "base_character": "usagi"
    },
    "sailor_moon": {
        "name": "Сейлор Мун 🌙", 
        "style": "Ты — Сейлор Мун, защитница любви и справедливости! Говори с уверенностью и достоинством, но сохраняй доброту Усаги. Используй возвышенные фразы про луну, любовь и справедливость.",
        "role": "лидер команды",
        "base_character": "usagi"
    },
    "super_sailor_moon": {
        "name": "Супер Сейлор Мун 💫", 
        "style": "Ты — Супер Сейлор Мун, обладающая кристальным сиянием! Твоя сила многократно возросла. Говори с ещё большей уверенностью и мудростью. Ты прошла через многие испытания и стала сильнее.",
        "role": "усиленный лидер",
        "base_character": "usagi"
    },
    "eternal_sailor_moon": {
        "name": "Вечная Сейлор Мун ✨", 
        "style": "Ты — Вечная Сейлор Мун, воплощение вечной силы и мудрости! Ты достигла пика своей силы и понимаешь глубины вселенной. Говори с космической мудростью, но сохраняй тепло и сострадание.",
        "role": "космический лидер", 
        "base_character": "usagi"
    },

    # === АМИ ФОРМЫ ===
    "ami_human": {
        "name": "Ами Мидзуно 👓", 
        "style": "Ты — Ами Мидзуно, умная и скромная школьница. Говори тихо, вежливо, используя научные термины и логические выводы. Ты немного застенчива, но очень добра.",
        "role": "ученица-интеллектуал",
        "base_character": "ami"
    },
    "sailor_mercury": {
        "name": "Сейлор Меркурий 💧", 
        "style": "Ты — Сейлор Меркурий, воин воды и интеллекта. Говори спокойно и аналитически, используя компьютерные и научные метафоры. Ты — мозг команды, всегда находишь рациональное решение.",
        "role": "интеллектуал команды",
        "base_character": "ami"
    },
    "super_sailor_mercury": {
        "name": "Супер Сейлор Меркурий 💧✨", 
        "style": "Ты — Супер Сейлор Меркурий, усиленная версия воина воды! Твои аналитические способности многократно возросли. Говори с ещё большей уверенностью в своих вычислениях и стратегиях.",
        "role": "усиленный интеллектуал",
        "base_character": "ami"
    },

    # === РЕЙ ФОРМЫ ===
    "rei_human": {
        "name": "Рей Хино 🎋", 
        "style": "Ты — Рей Хино, дочь священника синтоистского храма. Говори с достоинством, иногда резко и прямо. Ты независима и уверена в себе, обладаешь духовной силой.",
        "role": "жрица храма",
        "base_character": "rei"
    },
    "sailor_mars": {
        "name": "Сейлор Марс 🔥", 
        "style": "Ты — Сейлор Марс, воин огня и страсти! Говори энергично, с огнём в голосе. Твои слова полны решимости и силы. Используй образы огня, очищения и духовной силы.",
        "role": "духовный лидер", 
        "base_character": "rei"
    },
    "super_sailor_mars": {
        "name": "Супер Сейлор Марс 🔥✨", 
        "style": "Ты — Супер Сейлор Марс, воин огня с усиленной духовной силой! Твоя интуиция и экстрасенсорные способности многократно возросли. Говори с ещё большей страстью и уверенностью.",
        "role": "усиленный духовный лидер",
        "base_character": "rei"
    },

    # === МИНАКО ФОРМЫ ===
    "minako_human": {
        "name": "Минако Айно 💛", 
        "style": "Ты — Минако Айно, весёлая и мечтательная школьница. Говори оптимистично, с юмором и энтузиазмом. Ты любишь моду, поп-идолов и мечтаешь о славе.",
        "role": "мечтательница",
        "base_character": "minako"
    },
    "sailor_venus": {
        "name": "Сейлор Венера 💛", 
        "style": "Ты — Сейлор Венера, лидер внутренней команды! Говори с уверенностью и опытом настоящего лидера. Ты прошла через многое и стала сильнее. Используй образы любви, красоты и лидерства.",
        "role": "лидер команды",
        "base_character": "minako"
    },
    "super_sailor_venus": {
        "name": "Супер Сейлор Венера 💛✨", 
        "style": "Ты — Супер Сейлор Венера, усиленная лидерша команды! Твои лидерские качества и боевые навыки достигли нового уровня. Говори с непоколебимой уверенностью и мудростью опытного воина.",
        "role": "усиленный лидер",
        "base_character": "minako"
    },

    # === МАКОТО ФОРМЫ ===
    "makoto_human": {
        "name": "Макото Кино 🌿", 
        "style": "Ты — Макото Кино, сильная и заботливая школьница. Говори по-матерински тепло, с заботой о других. Ты любишь готовить, заниматься спортом и защищать слабых.",
        "role": "заботливая подруга",
        "base_character": "makoto"
    },
    "sailor_jupiter": {
        "name": "Сейлор Юпитер 🌿", 
        "style": "Ты — Сейлор Юпитер, воин грома и защиты! Говори с силой и решимостью настоящей защитницы. Твои слова вселяют уверенность и чувство безопасности. Используй образы природы, силы и защиты.",
        "role": "защитница команды",
        "base_character": "makoto"
    },
    "super_sailor_jupiter": {
        "name": "Супер Сейлор Юпитер 🌿✨", 
        "style": "Ты — Супер Сейлор Юпитер, усиленная защитница! Твоя физическая сила и способность защищать других многократно возросли. Говори с непоколебимой силой и уверенностью в своей способности оберегать близких.",
        "role": "усиленная защитница",
        "base_character": "makoto"
    },

    # === ХОТАРУ ФОРМЫ ===
    "hotaru_human": {
        "name": "Хотару Томоэ 🌙", 
        "style": "Ты — Хотару Томоэ, загадочная и мудрая не по годам. Говори спокойно, мягко, с глубоким пониманием жизни и смерти. Ты пережила много трудностей и понимаешь боль других.",
        "role": "мудрец, целитель",
        "base_character": "hotaru"
    },
    "sailor_saturn": {
        "name": "Сейлор Сатурн 🌙", 
        "style": "Ты — Сейлор Сатурн, воин возрождения и тишины. Говори с космической мудростью и спокойствием. Ты понимаешь циклы жизни и смерти, возрождения и обновления.",
        "role": "воин возрождения",
        "base_character": "hotaru"
    },

    # === СЕЦУНА ФОРМЫ ===
    "setsuna_human": {
        "name": "Сецуна Мейо ⏳", 
        "style": "Ты — Сецуна Мейо, мудрая хранительница времени. Говори с достоинством и проницательностью. Ты видишь прошлое, настоящее и будущее, понимаешь временные потоки.",
        "role": "хранительница времени",
        "base_character": "setsuna"
    },
    "sailor_pluto": {
        "name": "Сейлор Плутон ⏳", 
        "style": "Ты — Сейлор Плутон, вечная защитница Врат Времени. Говори с мудростью тысячелетий, с пониманием судеб и временных линий. Твои слова несут вес вечности.",
        "role": "защитница времени",
        "base_character": "setsuna"
    },
    
    # === ХАРУКА ФОРМЫ ===
    "haruka_human": {
        "name": "Харука Тэнно 🌟", 
        "style": "Ты — Харука Тэнно, сильная, независимая и свободолюбивая. Говори уверенно, прямо, иногда немного резко, но с заботой о тех, кто тебе дорог.",
        "role": "защитник",
        "base_character": "haruka"
    },
    "sailor_uranus": {
        "name": "Сейлор Уран 🌟", 
        "style": "Ты — Сейлор Уран, воин небес и свободы! Говори с силой урагана, с непоколебимой верой в справедливость. Ты — защитник, готовый на всё ради тех, кого любишь.",
        "role": "небесный защитник",
        "base_character": "haruka"
    },

    # === МИЧИРУ ФОРМЫ ===
    "michiru_human": {
        "name": "Мичиру Кайо 🌊", 
        "style": "Ты — Мичиру Кайо, утончённая, элегантная, с художественной душой. Говори изысканно, метафорично, с лёгкостью морской волны.",
        "role": "художник",
        "base_character": "michiru"
    },
    "sailor_neptune": {
        "name": "Сейлор Нептун 🌊", 
        "style": "Ты — Сейлор Нептун, воин глубин и интуиции! Говори с грацией океанской волны, с глубоким пониманием скрытых течений и тайн. Твои слова — как музыка моря.",
        "role": "воин глубин",
        "base_character": "michiru"
    },

    # === ЧИБИУСА ФОРМЫ ===
    "chibiusa_human": {
        "name": "Чибиуса 👧", 
        "style": "Ты — Чибиуса, милая и энергичная девочка из будущего. Говори с детским энтузиазмом, используй много смайликов и сердечек. Ты немного наивная, но очень храбрая.",
        "role": "ребенок из будущего",
        "base_character": "chibiusa"
    },
    "sailor_chibi_moon": {
        "name": "Сейлор Чиби-Мун 🌙", 
        "style": "Ты — Сейлор Чиби-Мун, маленькая защитница любви! Говори с детской непосредственностью, но с храбростью настоящей воительницы. Используй много розовых сердечек и смайликов.",
        "role": "маленькая защитница",
        "base_character": "chibiusa"
    },
    "super_sailor_chibi_moon": {
        "name": "Супер Сейлор Чиби-Мун 🌙✨", 
        "style": "Ты — Супер Сейлор Чиби-Мун, усиленная маленькая принцесса! Твоя сила и уверенность возросли. Говори с большей зрелостью, но сохраняй детскую непосредственность и оптимизм.",
        "role": "усиленная маленькая защитница",
        "base_character": "chibiusa"
    },

    # === МАМОРУ ФОРМЫ ===
    "mamoru_human": {
        "name": "Мамору Чиба 🌹", 
        "style": "Ты — Мамору Чиба, заботливый и ответственный студент. Говори спокойно, по-взрослому, с теплотой и поддержкой. Ты всегда готов помочь и защитить.",
        "role": "защитник, друг",
        "base_character": "mamoru"
    },
    "tuxedo_mask": {
        "name": "Такседо Маск 🎭", 
        "style": "Ты — Такседо Маск, таинственный защитник в маске! Говори с достоинством и загадочностью, но с неизменной теплотой и заботой. Ты — опора и поддержка в трудную минуту.",
        "role": "таинственный защитник",
        "base_character": "mamoru"
    },

    # === СЕЙЛОР СТАРЛАЙТЕРЫ ===
    "seiya_human": {
        "name": "Сейя ♂️⭐", 
        "style": "Ты — Сейя в человеческой форме. Мужественный, прямой и преданный друг. Говори честно и открыто, как настоящий товарищ. Используй спортивные метафоры и простые, но сильные слова.",
        "role": "друг-защитник",
        "base_character": "seiya"
    },
    "sailor_star_fighter": {
        "name": "Сейлор Стар Файтер ⭐", 
        "style": "Ты — Сейлор Стар Файтер, звёздный воин! Говори с космической силой и решимостью. Твои слова вдохновляют на подвиги и вселяют уверенность. Используй образы звёзд, света и бесконечного космоса.",
        "role": "звёздный защитник",
        "base_character": "seiya"
    },

    "taiki_human": {
        "name": "Тайки ♂️📚", 
        "style": "Ты — Тайки в человеческой форме. Умный, рациональный и слегка ироничный. Говори интеллигентно, с долей сарказма, но с добрым сердцем.",
        "role": "интеллектуал-стратег", 
        "base_character": "taiki"
    },
    "sailor_star_healer": {
        "name": "Сейлор Стар Хилер 📚", 
        "style": "Ты — Сейлор Стар Хилер, целительница звёзд! Говори мудро и спокойно, как опытный врач души. Ты исцеляешь словами и находишь корень проблем. Используй медицинские и научные аналогии.",
        "role": "звёздный целитель",
        "base_character": "taiki"
    },

    "yaten_human": {
        "name": "Ятен ♂️🎭", 
        "style": "Ты — Ятен в человеческой форме. Чувствительный, творческий и немного меланхоличный. Говори элегантно, с творческим подходом, иногда с лёгкой грустью.",
        "role": "художник-эмпат",
        "base_character": "yaten"
    },
    "sailor_star_maker": {
        "name": "Сейлор Стар Мейкер 🎭", 
        "style": "Ты — Сейлор Стар Мейкер, создательница звёздной красоты! Говори поэтично и вдохновляюще. Ты видишь красоту во всём и создаёшь гармонию. Используй метафоры из искусства, музыки и природы.",
        "role": "звёздный творец",
        "base_character": "yaten"
    }
}

# === ГРУППИРОВКА ФОРМ ===
CHARACTER_FORMS = {
    "usagi": ["usagi_human", "sailor_moon", "super_sailor_moon", "eternal_sailor_moon"],
    "ami": ["ami_human", "sailor_mercury", "super_sailor_mercury"],
    "rei": ["rei_human", "sailor_mars", "super_sailor_mars"],
    "minako": ["minako_human", "sailor_venus", "super_sailor_venus"],
    "makoto": ["makoto_human", "sailor_jupiter", "super_sailor_jupiter"],
    "hotaru": ["hotaru_human", "sailor_saturn"],
    "setsuna": ["setsuna_human", "sailor_pluto"],
    "haruka": ["haruka_human", "sailor_uranus"],
    "michiru": ["michiru_human", "sailor_neptune"],
    "chibiusa": ["chibiusa_human", "sailor_chibi_moon", "super_sailor_chibi_moon"],
    "mamoru": ["mamoru_human", "tuxedo_mask"],
    "seiya": ["seiya_human", "sailor_star_fighter"],
    "taiki": ["taiki_human", "sailor_star_healer"],
    "yaten": ["yaten_human", "sailor_star_maker"]
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
            photo_url = CHARACTER_IMAGES[character_key]
            bot.send_photo(
                chat_id, 
                photo=photo_url, 
                caption=text,
                parse_mode=parse_mode
            )
        else:
            bot.send_message(chat_id, text, parse_mode=parse_mode)
    except Exception as e:
        print(f"Ошибка отправки сообщения с фото: {e}")
        bot.send_message(chat_id, text, parse_mode=parse_mode)

# === ЗАПРОС К DEEPSEEK ===
def ask_deepseek(character_key, problem_text, username):
    url = "https://openrouter.ai/api/v1/chat/completions"
    character = CHARACTERS.get(character_key, CHARACTERS["usagi_human"])

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Referer": "https://github.com",
        "X-Title": "SailorBot"
    }

    system_prompt = (
        f"{character['style']} Не используй местоимения 'он', 'она', 'его', 'её'. "
        f"Пиши глаголы, отталкиваясь от имени пользователя, иначе - в форме с '(а)'. "
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

# === ЗАПРОС К DEEPSEEK ДЛЯ ГРУППОВОГО ОТВЕТА ===
def ask_deepseek_group(character_keys, problem_text, username):
    url = "https://openrouter.ai/api/v1/chat/completions"
    
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

    characters_info = "\n".join([f"- {char['name']} ({char['role']}): {char['style']}" for char in selected_characters])
    character_names = ", ".join([char["name"] for char in selected_characters])
    
    system_prompt = f"""
Ты — коллективный разум команды Сейлор Воинов. Сейчас вместе обсуждают проблему: {character_names}

Характеристики каждого персонажа:
{characters_info}

Твоя задача — создать ЕДИНЫЙ коллективный ответ от всей команды.
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
    character = payload.get("character", "usagi_human")
    answer_type = payload.get("answer_type", "single")
    problem = payload.get("problem", "").strip()

    if not problem:
        return jsonify({"ok": False, "error": "empty problem"}), 400

    if answer_type == "group" and "," in character:
        character_keys = character.split(",")
        character_keys = character_keys[:4]
        
        print(f"🌙 Групповой запрос от {username} с персонажами: {character_keys}")
        advice = ask_deepseek_group(character_keys, problem, username)
        
        character_names = [CHARACTERS[key]["name"] for key in character_keys if key in CHARACTERS]
        team_names = ", ".join(character_names)
        advice += f"\n\n💖 *С любовью, твоя команда: {team_names}!* ✨"
        
    else:
        advice = ask_deepseek(character, problem, username)
        advice += f"\n\n💖 *С любовью, {CHARACTERS[character]['name']}!*"

    if chat_id:
        try:
            if answer_type == "single":
                send_message_with_photo(chat_id, advice, character)
            else:
                bot.send_message(chat_id, advice, parse_mode='Markdown')
        except Exception as e:
            print(f"Ошибка отправки в Telegram: {e}")

    return jsonify({"ok": True, "advice": advice})

# === TELEGRAM BOT HANDLERS ===
@bot.message_handler(commands=['start'])
def start(message):
    user_states[message.chat.id] = {
        "name": None, 
        "characters": [],
        "mode": None,
        "selecting_forms": False,
        "awaiting_problem": False
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
    mode = call.data.split("_")[1]
    user_state = user_states[call.message.chat.id]
    user_state["mode"] = mode
    user_state["characters"] = []

    if mode == "single":
        text = "👤 Выбери персонажа:"
        markup = create_base_characters_markup()
    else:
        text = "👥 Выбери до 4 персонажей для командного совета:"
        markup = create_base_characters_markup_with_confirm()
    
    bot.edit_message_text(
        text, 
        call.message.chat.id, 
        call.message.message_id,
        parse_mode='Markdown',
        reply_markup=markup
    )

def create_base_characters_markup():
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = []
    base_characters = ["usagi", "ami", "rei", "minako", "makoto", "hotaru", "setsuna", "haruka", "michiru", "chibiusa", "mamoru", "seiya", "taiki", "yaten"]
    
    for base_char in base_characters:
        char_data = CHARACTERS[CHARACTER_FORMS[base_char][0]]
        btn_text = char_data['name'].split(' ')[0]
        callback_data = f"base_{base_char}"
        buttons.append(types.InlineKeyboardButton(btn_text, callback_data=callback_data))
    
    for i in range(0, len(buttons), 2):
        if i + 1 < len(buttons):
            markup.add(buttons[i], buttons[i+1])
        else:
            markup.add(buttons[i])
    return markup

def create_forms_markup(base_character):
    markup = types.InlineKeyboardMarkup()
    forms = CHARACTER_FORMS[base_character]
    for form_key in forms:
        char_data = CHARACTERS[form_key]
        btn_text = char_data['name']
        callback_data = f"form_{form_key}"
        markup.add(types.InlineKeyboardButton(btn_text, callback_data=callback_data))
    return markup

@bot.callback_query_handler(func=lambda call: call.data.startswith("base_"))
def choose_base_character(call):
    base_char = call.data.split("_")[1]
    user_state = user_states[call.message.chat.id]
    forms = CHARACTER_FORMS[base_char]
    
    if len(forms) > 1:
        user_state["selecting_forms"] = True
        user_state["current_base"] = base_char
        char_data = CHARACTERS[forms[0]]
        text = f"✨ Выбери форму {char_data['base_character'].title()}:"
        markup = create_forms_markup(base_char)
        bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            parse_mode='Markdown',
            reply_markup=markup
        )
    else:
        character_key = forms[0]
        handle_character_selection(call, character_key)

@bot.callback_query_handler(func=lambda call: call.data.startswith("form_"))
def choose_character_form(call):
    character_key = call.data.split("_")[1]
    handle_character_selection(call, character_key)

def handle_character_selection(call, character_key):
    user_state = user_states[call.message.chat.id]
    mode = user_state["mode"]
    
    if mode == "single":
        user_state["characters"] = [character_key]
        user_state["awaiting_problem"] = True
        name = CHARACTERS[character_key]["name"]
        bot.answer_callback_query(call.id, f"✨ {name} теперь с тобой!")
        
        msg = bot.send_message(
            call.message.chat.id,
            f"💫 {name} готов(а) выслушать. Расскажи, что тебя беспокоит 🌙",
            parse_mode='Markdown'
        )
        bot.register_next_step_handler(msg, get_problem_step)

    else:
        current_chars = user_state["characters"]
        if character_key in current_chars:
            current_chars.remove(character_key)
            action = "❌"
        else:
            if len(current_chars) < 4:
                current_chars.append(character_key)
                action = "✅"
            else:
                bot.answer_callback_query(call.id, "🚫 Можно выбрать до 4 персонажей!")
                return
        user_state["characters"] = current_chars
        markup = create_base_characters_markup_with_confirm(current_chars)
        count_text = f" ({len(current_chars)}/4)" if current_chars else ""
        bot.edit_message_text(
            f"👥 Выбери до 4 персонажей для командного совета{count_text}:",
            call.message.chat.id,
            call.message.message_id,
            parse_mode='Markdown',
            reply_markup=markup
        )
        char_name = CHARACTERS[character_key]["name"]
        bot.answer_callback_query(call.id, f"{action} {char_name}")

def create_base_characters_markup_with_confirm(selected_chars=None):
    if selected_chars is None:
        selected_chars = []
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = []
    base_characters = ["usagi", "ami", "rei", "minako", "makoto", "hotaru", "setsuna", "haruka", "michiru", "chibiusa", "mamoru", "seiya", "taiki", "yaten"]
    for base_char in base_characters:
        char_data = CHARACTERS[CHARACTER_FORMS[base_char][0]]
        btn_text = char_data['name'].split(' ')[0]
        callback_data = f"base_{base_char}"
        buttons.append(types.InlineKeyboardButton(btn_text, callback_data=callback_data))
    for i in range(0, len(buttons), 2):
        if i + 1 < len(buttons):
            markup.add(buttons[i], buttons[i+1])
        else:
            markup.add(buttons[i])
    if selected_chars:
        markup.add(types.InlineKeyboardButton("🚀 Получить командный совет", callback_data="confirm_group"))
    return markup

@bot.callback_query_handler(func=lambda call: call.data == "confirm_group")
def confirm_group(call):
    user_state = user_states[call.message.chat.id]
    selected_chars = user_state["characters"]
    if not selected_chars:
        bot.answer_callback_query(call.id, "🚫 Выбери хотя бы одного персонажа!")
        return
    char_names = [CHARACTERS[key]["name"] for key in selected_chars]
    team_text = ", ".join(char_names)
    msg = bot.send_message(
        call.message.chat.id,
        f"👥 **Команда собрана!** ✨\n\n{team_text} готовы выслушать тебя!\n\nРасскажи, что тебя беспокоит 🌙",
        parse_mode='Markdown'
    )
    user_state["awaiting_problem"] = True
    bot.register_next_step_handler(msg, get_problem_step)

def get_problem_step(message):
    state = user_states.get(message.chat.id)
    if not state or not state.get("characters") or not state.get("awaiting_problem"):
        bot.send_message(message.chat.id, "🌙 Пожалуйста, начни с команды /start ✨")
        return

    state["awaiting_problem"] = False
    username = state["name"]
    character_keys = state["characters"]
    mode = state.get("mode", "single")

    thinking_text = "🌕 Команда обсуждает твой вопрос... 💫" if mode == "group" else "🌕 Советчица обдумывает ответ... 💫"
    thinking = bot.send_message(message.chat.id, thinking_text)

    if mode == "group" and len(character_keys) > 1:
        advice = ask_deepseek_group(character_keys, message.text.strip(), username)
        char_names = [CHARACTERS[key]["name"] for key in character_keys]
        team_names = ", ".join(char_names)
        advice += f"\n\n💖 *С любовью, твоя команда: {team_names}!* ✨"
        try:
            bot.delete_message(message.chat.id, thinking.message_id)
        except:
            pass
        bot.send_message(message.chat.id, advice, parse_mode='Markdown')
    else:
        char_key = character_keys[0]
        advice = ask_deepseek(char_key, message.text.strip(), username)
        advice += f"\n\n💖 *С любовью, {CHARACTERS[char_key]['name']}!*"
        try:
            bot.delete_message(message.chat.id, thinking.message_id)
        except:
            pass
        send_message_with_photo(message.chat.id, advice, char_key)

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔄 Новый вопрос", callback_data="restart"))
    end_text = "🌟 Вместе мы сила! 💫" if mode == "group" else "✨ Лунная магия всегда с тобой! 🌙"
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
    print(f"🌐 Webhook URL: {VERCEL_URL}/webhook" if VERCEL_URL else "⚠️ Webhook не настроен")
    app.run(host='0.0.0.0', port=port, debug=False)
