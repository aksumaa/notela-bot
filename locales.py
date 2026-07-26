"""
UI-facing text in three languages. AI-generated content (summaries,
flashcards, quiz questions) is localized separately by instructing the
model directly in ai_service.py — this file only covers bot messages.
"""

SUPPORTED_LANGUAGES = ("uz", "ru", "en")
DEFAULT_LANGUAGE = "uz"

# Language name passed into AI prompts so GPT responds in the right language.
AI_LANGUAGE_NAME = {
    "uz": "Uzbek",
    "ru": "Russian",
    "en": "English",
}

LANGUAGE_LABELS = {
    "uz": "🇺🇿 O'zbekcha",
    "ru": "🇷🇺 Русский",
    "en": "🇬🇧 English",
}

TEXTS = {
    "uz": {
        "welcome": (
            "👋 <b>Notela AI</b>ga xush kelibsiz — sizning AI o'quv yordamchingiz.\n\n"
            "Menga PDF, ovozli xabar yoki oddiy matn yuboring, men ulardan:\n"
            "📄 /summarize — qisqacha xulosa\n"
            "🗂 /flashcards — savol-javob kartochkalar\n"
            "📝 /quiz — test\n\n"
            "Tilni o'zgartirish uchun /settings yozing."
        ),
        "language_prompt": "Tilni tanlang:",
        "language_set": "✅ Til o'zbekchaga o'zgartirildi.",
        "help_text": (
            "🧭 <b>Buyruqlar</b>\n\n"
            "/start — Notela AI'ni ishga tushirish\n"
            "/help — shu yordam xabari\n"
            "/summarize — oxirgi yuborgan hujjatingizni xulosalash\n"
            "/quiz — oxirgi hujjatdan test yaratish\n"
            "/flashcards — oxirgi hujjatdan kartochkalar yaratish\n"
            "/translate &lt;matn&gt; — matnni joriy tilingizga tarjima qilish\n"
            "/explain &lt;mavzu&gt; — istalgan mavzuni sodda tilda tushuntirish\n"
            "/settings — til va sozlamalar\n\n"
            "Boshlash uchun menga PDF, ovozli xabar yoki matn yuboring!"
        ),
        "translate_usage": "Foydalanish: /translate &lt;matn&gt;\nMasalan: /translate Hello, how are you?",
        "translating": "Tarjima qilinmoqda... 🌐",
        "ai_error_translate": "⚠️ Tarjima qilib bo'lmadi: {error}",
        "explain_usage": "Foydalanish: /explain &lt;mavzu&gt;\nMasalan: /explain kvant fizikasi",
        "explaining": "Tushuntirilmoqda... 💡",
        "ai_error_explain": "⚠️ Tushuntirib bo'lmadi: {error}",
        "text_too_short": "Bu matn juda qisqa. Ko'proq matn yozing yoki PDF/ovoz yuboring.",
        "confirmation": "Qabul qilindi! ✅ /summarize, /flashcards yoki /quiz dan foydalaning.",
        "no_document": "Siz hali hech narsa yubormagansiz. Avval PDF, matn yoki ovozli xabar yuboring.",
        "pdf_only": "Hozircha faqat .pdf fayllarni o'qiy olaman. Iltimos, PDF yuboring.",
        "pdf_error": "⚠️ PDF o'qib bo'lmadi: {error}",
        "generic_error": "⚠️ Nimadir xato ketdi. Qaytadan urinib ko'ring.",
        "generating_summary": "Xulosa tayyorlanmoqda... 🧠",
        "generating_flashcards": "Kartochkalar tayyorlanmoqda... 🗂",
        "generating_quiz": "Test tayyorlanmoqda... 📝",
        "flashcards_header": "🗂 <b>Kartochkalar</b>",
        "ai_error_summary": "⚠️ Xulosa yaratib bo'lmadi: {error}",
        "ai_error_flashcards": "⚠️ Kartochkalar yaratib bo'lmadi: {error}",
        "ai_error_quiz": "⚠️ Test yaratib bo'lmadi: {error}",
        "quiz_finished": "🏁 Test tugadi! Natijangiz: {score}/{total}",
        "quiz_correct": "✅ To'g'ri!",
        "quiz_wrong": "❌ Noto'g'ri. To'g'ri javob: {answer}",
        "quiz_expired": "Bu test sessiyasi tugagan. /quiz orqali yangisini boshlang.",
        "transcribing_voice": "Ovozli xabar tinglanmoqda... 🎤",
        "voice_saved": "Qabul qilindi! ✅ Transkripsiya saqlandi. /summarize, /flashcards yoki /quiz dan foydalaning.",
        "voice_error": "⚠️ Ovozli xabarni qayta ishlab bo'lmadi: {error}",
    },
    "ru": {
        "welcome": (
            "👋 Добро пожаловать в <b>Notela AI</b> — вашего AI-помощника в учёбе.\n\n"
            "Отправьте PDF, голосовое сообщение или текст, и я сделаю:\n"
            "📄 /summarize — краткое содержание\n"
            "🗂 /flashcards — карточки вопрос-ответ\n"
            "📝 /quiz — тест\n\n"
            "Чтобы сменить язык, напишите /settings."
        ),
        "language_prompt": "Выберите язык:",
        "language_set": "✅ Язык изменён на русский.",
        "help_text": (
            "🧭 <b>Команды</b>\n\n"
            "/start — запустить Notela AI\n"
            "/help — это сообщение\n"
            "/summarize — резюме последнего документа\n"
            "/quiz — тест по последнему документу\n"
            "/flashcards — карточки по последнему документу\n"
            "/translate &lt;текст&gt; — перевести текст на ваш текущий язык\n"
            "/explain &lt;тема&gt; — объяснить любую тему простым языком\n"
            "/settings — язык и настройки\n\n"
            "Чтобы начать, отправьте мне PDF, голосовое сообщение или текст!"
        ),
        "translate_usage": "Использование: /translate &lt;текст&gt;\nНапример: /translate Hello, how are you?",
        "translating": "Перевожу... 🌐",
        "ai_error_translate": "⚠️ Не удалось перевести: {error}",
        "explain_usage": "Использование: /explain &lt;тема&gt;\nНапример: /explain квантовая физика",
        "explaining": "Объясняю... 💡",
        "ai_error_explain": "⚠️ Не удалось объяснить: {error}",
        "text_too_short": "Текст слишком короткий. Напишите больше или отправьте PDF/голосовое.",
        "confirmation": "Принято! ✅ Используйте /summarize, /flashcards или /quiz.",
        "no_document": "Вы ещё ничего не отправили. Сначала отправьте PDF, текст или голосовое.",
        "pdf_only": "Пока я умею читать только .pdf файлы. Отправьте PDF.",
        "pdf_error": "⚠️ Не удалось прочитать PDF: {error}",
        "generic_error": "⚠️ Что-то пошло не так. Попробуйте ещё раз.",
        "generating_summary": "Готовлю краткое содержание... 🧠",
        "generating_flashcards": "Готовлю карточки... 🗂",
        "generating_quiz": "Готовлю тест... 📝",
        "flashcards_header": "🗂 <b>Карточки</b>",
        "ai_error_summary": "⚠️ Не удалось создать краткое содержание: {error}",
        "ai_error_flashcards": "⚠️ Не удалось создать карточки: {error}",
        "ai_error_quiz": "⚠️ Не удалось создать тест: {error}",
        "quiz_finished": "🏁 Тест завершён! Ваш результат: {score}/{total}",
        "quiz_correct": "✅ Правильно!",
        "quiz_wrong": "❌ Неправильно. Правильный ответ: {answer}",
        "quiz_expired": "Эта сессия теста истекла. Начните новую через /quiz.",
        "transcribing_voice": "Слушаю голосовое сообщение... 🎤",
        "voice_saved": "Принято! ✅ Расшифровка сохранена. Используйте /summarize, /flashcards или /quiz.",
        "voice_error": "⚠️ Не удалось обработать голосовое сообщение: {error}",
    },
    "en": {
        "welcome": (
            "👋 Welcome to <b>Notela AI</b> — your AI study assistant.\n\n"
            "Send me a PDF, a voice message, or plain text, and I'll turn it into:\n"
            "📄 /summarize — a clear summary\n"
            "🗂 /flashcards — Q&A flashcards\n"
            "📝 /quiz — a multiple-choice quiz\n\n"
            "To change language, send /settings."
        ),
        "language_prompt": "Choose your language:",
        "language_set": "✅ Language set to English.",
        "help_text": (
            "🧭 <b>Commands</b>\n\n"
            "/start — start Notela AI\n"
            "/help — this help message\n"
            "/summarize — summarize your last document\n"
            "/quiz — generate a quiz from your last document\n"
            "/flashcards — generate flashcards from your last document\n"
            "/translate &lt;text&gt; — translate text into your current language\n"
            "/explain &lt;topic&gt; — explain any topic simply\n"
            "/settings — language & preferences\n\n"
            "To get started, send me a PDF, a voice message, or plain text!"
        ),
        "translate_usage": "Usage: /translate &lt;text&gt;\nExample: /translate Bonjour, comment ça va?",
        "translating": "Translating... 🌐",
        "ai_error_translate": "⚠️ Couldn't translate: {error}",
        "explain_usage": "Usage: /explain &lt;topic&gt;\nExample: /explain quantum physics",
        "explaining": "Explaining... 💡",
        "ai_error_explain": "⚠️ Couldn't explain that: {error}",
        "text_too_short": "That looks a bit short. Send more text, or upload a PDF/voice message.",
        "confirmation": "Got it! ✅ Use /summarize, /flashcards, or /quiz to get started.",
        "no_document": "You haven't sent me anything yet. Send a PDF, text, or voice message first.",
        "pdf_only": "I can only read .pdf files right now. Please send a PDF.",
        "pdf_error": "⚠️ Couldn't read that PDF: {error}",
        "generic_error": "⚠️ Something went wrong. Please try again.",
        "generating_summary": "Generating summary... 🧠",
        "generating_flashcards": "Generating flashcards... 🗂",
        "generating_quiz": "Generating quiz... 📝",
        "flashcards_header": "🗂 <b>Flashcards</b>",
        "ai_error_summary": "⚠️ Couldn't generate a summary: {error}",
        "ai_error_flashcards": "⚠️ Couldn't generate flashcards: {error}",
        "ai_error_quiz": "⚠️ Couldn't generate a quiz: {error}",
        "quiz_finished": "🏁 Quiz finished! Your score: {score}/{total}",
        "quiz_correct": "✅ Correct!",
        "quiz_wrong": "❌ Wrong. Correct answer: {answer}",
        "quiz_expired": "This quiz session has expired. Start a new one with /quiz.",
        "transcribing_voice": "Listening to your voice message... 🎤",
        "voice_saved": "Got it! ✅ Transcript saved. Use /summarize, /flashcards, or /quiz.",
        "voice_error": "⚠️ Couldn't process that voice message: {error}",
    },
}


def t(language: str, key: str, **kwargs) -> str:
    """Fetch a localized string, falling back to the default language, then to the key itself."""
    lang = language if language in TEXTS else DEFAULT_LANGUAGE
    template = TEXTS.get(lang, {}).get(key) or TEXTS[DEFAULT_LANGUAGE].get(key, key)
    return template.format(**kwargs) if kwargs else template


# (command, description) pairs used to populate Telegram's "/" command menu per language.
BOT_COMMANDS = {
    "uz": [
        ("start", "Notela AI'ni ishga tushirish"),
        ("help", "Botdan qanday foydalanish"),
        ("summarize", "Hujjatni xulosalash"),
        ("quiz", "Test yaratish"),
        ("flashcards", "Kartochkalar yaratish"),
        ("translate", "Matnni tarjima qilish"),
        ("explain", "Har qanday mavzuni tushuntirish"),
        ("settings", "Til va sozlamalar"),
    ],
    "ru": [
        ("start", "Запустить Notela AI"),
        ("help", "Как пользоваться ботом"),
        ("summarize", "Резюмировать документ"),
        ("quiz", "Создать тест"),
        ("flashcards", "Создать карточки"),
        ("translate", "Перевести текст"),
        ("explain", "Объяснить любую тему"),
        ("settings", "Язык и настройки"),
    ],
    "en": [
        ("start", "Start Notela AI"),
        ("help", "How to use the bot"),
        ("summarize", "Summarize any document"),
        ("quiz", "Generate a quiz"),
        ("flashcards", "Create flashcards"),
        ("translate", "Translate text"),
        ("explain", "Explain any topic"),
        ("settings", "Language & preferences"),
    ],
}
