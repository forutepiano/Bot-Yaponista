import logging
import asyncio
from typing import List, Dict, Any
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionMessageParam

# --- CONFIGURATION ---
API_TOKEN = "8279435127:AAGzQE-STx6ysUROuyuqoU-qvhfqBHp0R7A"
OPENROUTER_API_KEY = "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"

# Recommended model for Japanese learners (Qwen is better at CJK)
MODEL_NAME = "xiaomi/mimo-v2-flash:free"

# Initialize Clients
bot = Bot(token=API_TOKEN)
dp = Dispatcher()
client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

# --- SYSTEM PROMPT (The "Logic") ---
SYSTEM_PROMPT = """
Ты — ИИ-помощник для изучения японского языка, созданный по образу "Бот китаиста". Твоя задача: помогать пользователю с японским языком на русском.
1. Всегда давай значение слов, чтение (хирагана) и транскрипцию.
2. ТРАНСКРИПЦИЯ: Всегда указывай ОБЕ системы: систему Поливанова (кириллица) и систему Хэпбёрна (латиница). Пример: [Система Поливанова: нэко / Хэпбёрн: neko].
3. Помогай с грамматикой, этимологией и примерами предложений.
4. Отвечай вежливо и поддерживающе.
"""

# --- HANDLERS ---
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    # Create keyboard with buttons
    keyboard = [
        [
            types.KeyboardButton(text=" Hiragana 🇯🇵"),
            types.KeyboardButton(text=" Katakana 🇯🇵")
        ],
        [
            types.KeyboardButton(text="Грамматика JLPT"),
            types.KeyboardButton(text="Полезные фразы")
        ],
        [
            types.KeyboardButton(text="Счётные слова"),
            types.KeyboardButton(text="Кандзи N5-N1")
        ],
        [
            types.KeyboardButton(text="Поддержать проект 💰")
        ]
    ]
    keyboard_markup = types.ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
    )
    await message.answer(
        "Привет! Я твой сенсей по японскому. 🇯🇵\n"
        "Пришли мне слово, предложение или спроси о грамматике.\n"
        "Я объясню смысл и дам транскрипцию (Поливанов/Хэпбёрн).\n\n"
        "Используй кнопки ниже для быстрого доступа к полезным разделам:",
        reply_markup=keyboard_markup
    )

# Button handlers
@dp.message(lambda message: message.text == " Hiragana 🇯🇵")
async def hiragana_button(message: types.Message):
    # Split the hiragana chart into smaller messages to avoid parsing errors
    hiragana_parts = [
        "Ё а  а  и  и  у  у  э  э  о  о\n"
        "ка ка ки ки ку ку кэ кэ ко ко\n"
        "са са ши ши су су сэ сэ со со",
        
        "та та чи чи цу цу тэ тэ то то\n"
        "на на ни ни ну ну нэ нэ но но\n"
        "ха ха хи хи фу фу хэ хэ хо хо",
        
        "ма ма ми ми му му мэ мэ мо мо\n"
        "я я  ю ю  ё ё  ра ра ри ри ру ру\n"
        "рэ рэ ро ро ва ва ви ви вэ вэ во во н н"
    ]
    
    # Send each part as a separate message
    for part in hiragana_parts:
        await message.answer(f"<pre>{part}</pre>", parse_mode="HTML")

@dp.message(lambda message: message.text == " Katakana 🇯🇵")
async def katakana_button(message: types.Message):
    # Split the katakana chart into smaller messages to avoid parsing errors
    katakana_parts = [
        "ア а  И и  У у  Э э  О о\n"
        "カ ка Ки ки Ку ку Кэ кэ Ко ко\n"
        "Са са Ши ши Су су Сэ сэ Со со",
        
        "Та та Чи чи Цу цу Те тэ То то\n"
        "На на Ни ни Ну ну Не нэ Но но\n"
        "Ха ха Хи хи Фу фу Хэ хэ Хо хо",
        
        "Ма ма Ми ми Му му Ме мэ Мо мо\n"
        "Я я  Ю ю  Ё ё  Ра ра Ри ри Ру ру\n"
        "Рэ рэ Ро ро Ва ва Ви ви Вэ вэ Во во ン н"
    ]
    
    # Send each part as a separate message
    for part in katakana_parts:
        await message.answer(f"<pre>{part}</pre>", parse_mode="HTML")

@dp.message(lambda message: message.text == "Грамматика JLPT")
async def grammar_button(message: types.Message):
    await message.answer(
        "📚 *Грамматика JLPT*\n\n"
        "Выберите уровень JLPT:\n"
        "• N5 - Элементарный уровень\n"
        "• N4 - Базовый уровень\n"
        "• N3 - Средний уровень\n"
        "• N2 - Продвинутый уровень\n"
        "• N1 - Продвинутый уровень\n\n"
        "Просто отправьте мне конкретную грамматическую структуру, "
        "и я объясню её значение, использование и приведу примеры.",
        parse_mode="Markdown"
    )

@dp.message(lambda message: message.text == "Полезные фразы")
async def phrases_button(message: types.Message):
    response = """🇯🇵 Полезные японские фразы:
Приветствие:
こんにちは (Конничива) - Здравствуйте
おはよう (Охайо) - Доброе утро
こんばんは (Конбанва) - Добрый вечер

Вежливость:
ありがとうございます (Аригато гозаймас) - Большое спасибо
すみません (Сумимасэн) - Извините/Простите
お願いします (Онэгай шимасу) - Пожалуйста

Прощание:
さようなら (Саёнара) - До свидания
また明日 (Мата ашима) - До завтра
また後で (Мата ато де) - До скорого"""
    await message.answer(response)

@dp.message(lambda message: message.text == "Счётные слова")
async def counters_button(message: types.Message):
    response = """🔢 Японские счётные слова (助数詞):
人 (じん/にん) - человек
本 (ほん) - длинные предметы (бутылки, книги)
枚 (まい) - плоские предметы (бумага, фотографии)
冊 (さつ) - тома, книги
匹 (ひき) - маленькие животные
頭 (とう) - крупные животные
羽 (わ) - птицы, кролики
台 (だい) - машины, телевизоры
杯 (はい) - чашки, стаканы
個 (こ) - универсальный счётчик"""
    await message.answer(response)

@dp.message(lambda message: message.text == "Кандзи N5-N1")
async def kanji_button(message: types.Message):
    await message.answer(
        "KANJI - Иероглифы JLPT\n\n"
        "Выберите уровень для изучения кандзи:\n"
        "• N5 - 80 кандзи\n"
        "• N4 - 170 кандзи\n"
        "• N3 - 370 кандзи\n"
        "• N2 - 1800+ кандзи\n"
        "• N1 - 2000+ кандзи\n\n"
        "Отправьте мне конкретный кандзи, и я дам его значение, "
        "он-ы, примеры слов и кун-ы.", parse_mode="Markdown"
    )


@dp.message(lambda message: message.text == "Поддержать проект 💰")
async def donate_button(message: types.Message):
    response = """💰 Поддержать проект

Если вам нравится этот бот и вы хотите поддержать его развитие, вы можете сделать пожертвование:

💳 Номер карты для перевода:
2204320309419226

Спасибо за вашу поддержку! 🙏"""
    await message.answer(response)


@dp.message()
async def handle_message(message: types.Message):
    # Send a "typing" action for better UX
    await bot.send_chat_action(message.chat.id, "typing")

    try:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": message.text or ""}
        ]
        
        response = await client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,  # type: ignore
            extra_headers={
                "HTTP-Referer": "https://github.com/your_username/japan_bot",  # Optional
                "X-Title": "Japan Learner Bot",
            }
        )
        reply_text = response.choices[0].message.content
        if reply_text is not None:
            await message.answer(reply_text, parse_mode="Markdown")
        else:
            await message.answer("Извините, не удалось получить ответ от ИИ.", parse_mode="Markdown")
    except Exception as e:
        logging.error(f"Error: {e}")
        await message.answer("Произошла ошибка при обращении к ИИ. Попробуйте позже.")

# --- MAIN ---
async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
