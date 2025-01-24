from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from .main_menu import show_main_menu

def get_audio_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎙️ Clonar Voz", callback_data="audio_clone"),
         InlineKeyboardButton("📝 Texto a Voz", callback_data="audio_tts")],
        [InlineKeyboardButton("🔙 Volver", callback_data="main_menu")]
    ])

async def handle_audio_selection(update, context):
    query = update.callback_query
    await query.answer()
    
    if query.data == "audio_clone":
        await query.edit_message_text("🎤 Envía un audio de referencia (formato WAV)")
        context.user_data["state"] = "awaiting_audio"
    elif query.data == "audio_tts":
        await query.edit_message_text("✍️ Escribe el texto para convertir a voz:")
        context.user_data["state"] = "awaiting_tts"
    elif query.data == "main_menu":
        await query.edit_message_text("🏠 Aquí tienes el menú principal")
        show_main_menu()
        context.user_data["state"] = "main_menu"