from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    filters,
    CallbackQueryHandler,
    CommandHandler
)
from .menu.main_menu import show_main_menu, get_main_menu
from .menu.audio_menu import get_audio_menu, handle_audio_selection
from utils.security import validate_user
import os
import logging

from ai_services.tts_local import xtts_engine

logging.basicConfig(level=logging.INFO)
# logging.basicConfig(level=logging.CRITICAL)
logging.getLogger("httpx").setLevel(logging.CRITICAL)

# Inicializar estados del usuario
def init_user_state(context):
    if "state" not in context.user_data:
        context.user_data["state"] = "main_menu"

async def handle_all_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Validar usuario
    if not validate_user(update.message.from_user.id):
        await update.message.reply_text("❌ No autorizado")
        return

    init_user_state(context)
    current_state = context.user_data["state"]

    # Procesar AUDIO
    if update.message.voice or update.message.audio:
        if current_state == "awaiting_audio":
            await handle_voice_message(update, context)
        else:
            await update.message.reply_text("⚠️ Usa el comando /clonar_voz primero")
        return

    # Procesar TEXTO
    if update.message.text:
        text = update.message.text
        if text == "/start":
            await show_main_menu(update, context)
        elif text == "🎵 Generar Audio":
            await update.message.reply_text(
                "🔊 Elige una opción:", 
                reply_markup=get_audio_menu()
            )
        elif current_state == "awaiting_tts":
            await process_tts(update, text, context)
        elif current_state == "awaiting_cloning_text":
            try:
                # Obtener texto del usuario
                texto_a_clonar = update.message.text
                
                # Obtener ruta del audio guardado
                input_path = context.user_data['input_path']
                
                # Limpiar estado
                del context.user_data['input_path']
                
                # Procesar audio
                output_path = await xtts_engine.process_audio(texto_a_clonar, input_path)
                
                # Enviar respuesta
                await update.message.reply_text("✅ Voz clonada exitosamente!")
                await update.message.reply_voice(voice=open(output_path, "rb"))
                
                # Limpieza de archivos temporales (opcional)
                input_path.unlink(missing_ok=True)
                output_path.unlink(missing_ok=True)
                
            except Exception as e:
                await update.message.reply_text("❌ Error al generar el audio clonado: ", e)
            finally:
                context.user_data["state"] = "main_menu"
                await show_main_menu(update, context)
        else:
            await update.message.reply_text(
                "ℹ️ Usa los botones del menú:",
                reply_markup=get_main_menu()
            )
        return

    # Otros tipos de mensaje
    await update.message.reply_text("⚠️ Formato no soportado")

async def process_tts(update: Update, text: str, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🔊 Generando audio: {text}")
    context.user_data["state"] = "main_menu"
    # Aquí iría la generación real del audio
    await update.message.reply_voice(voice=open("audio.mp3", "rb"))  # Ejemplo
    await show_main_menu(update, context)

async def handle_voice_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Obtener el archivo de audio
        file = await (update.message.voice or update.message.audio).get_file()
        
        # Guardar audio recibido
        input_path = await xtts_engine.save_incoming_audio(file)

        # Guardar la ruta del audio en el contexto
        context.user_data['input_path'] = input_path
        
        # Pedir texto al usuario
        await update.message.reply_text("🎤 Audio recibido. Por favor, escribe el texto que quieres que clone:")

         # Establecer estado de espera
        context.user_data["state"] = "awaiting_cloning_text"
        
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")
    

def setup_bot():
    app = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()
    
    # Handlers esenciales
    app.add_handler(CommandHandler("start", show_main_menu))
    app.add_handler(CallbackQueryHandler(handle_audio_selection))
    app.add_handler(MessageHandler(filters.ALL, handle_all_messages))
    
    return app