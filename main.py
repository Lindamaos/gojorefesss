import asyncio
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackContext

# Token del bot
BOT_TOKEN = '7411610720:AAEZjL4JD_JAyxlXiARFdneG5JGw4aGOAHc'
CHANNEL_ID = '-1002274444077'  # ID del canal de referencias
OWNER_ID = 7116662379  # Tu ID de usuario
APPROVED_GROUPS = {-1002436988879}  # Incluye el grupo aprobado automáticamente

def approve_group(update, context: CallbackContext):
    if update.effective_user.id != OWNER_ID:
        update.message.reply_text("❌ No tienes permiso para aprobar grupos.")
        return
    group_id = update.effective_chat.id
    APPROVED_GROUPS.add(group_id)
    update.message.reply_text(f"✅ Grupo aprobado. ID: {group_id}", parse_mode="Markdown")

def refe_command(update, context: CallbackContext):
    if update.effective_chat.id not in APPROVED_GROUPS:
        update.message.reply_text("❌ Este grupo no está aprobado para usar este comando.")
        return

    user_message = update.message.reply_to_message
    if not user_message or not user_message.photo:
        update.message.reply_text("❌ Responde a un mensaje con una foto válida.")
        return

    comment = user_message.caption if user_message.caption else "Sin comentario"
    user_reference = user_message.from_user.username or "Usuario desconocido"
    message_format = (
        f"★ 𝙂𝙤𝙟𝙤 𝙥𝙧𝙤𝙮𝙚𝙘𝙩 ★\n"
        f"Referencia de: @{user_reference}\nComentario: {comment}\nAprobado por: [@gusies](https://t.me/gusies)"
    )
    keyboard = [[InlineKeyboardButton("OWNER 👤", url="https://t.me/gusies")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(message_format, reply_markup=reply_markup)

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("approvegroup", approve_group))
    dp.add_handler(CommandHandler("refe", refe_command))

    print("El bot está activo. Presiona Ctrl+C para detenerlo.")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

