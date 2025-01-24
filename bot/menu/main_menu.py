from telegram import ReplyKeyboardMarkup, KeyboardButton

def get_main_menu():
    return ReplyKeyboardMarkup([
        [KeyboardButton("🎵 Generar Audio"), KeyboardButton("📷 Generar Imagen")],
        [KeyboardButton("❓ Ayuda"), KeyboardButton("⚙️ Configuración")]
    ], resize_keyboard=True)

async def show_main_menu(update, context):
    await update.message.reply_text(
        "🏠 **Menú Principal**",
        reply_markup=get_main_menu(),
        parse_mode="Markdown"
    )