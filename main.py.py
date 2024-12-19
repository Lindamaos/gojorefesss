import asyncio
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Token del bot
BOT_TOKEN = '7411610720:AAEZjL4JD_JAyxlXiARFdneG5JGw4aGOAHc'
CHANNEL_ID = '-1002274444077'  # ID del canal de referencias

# ID del usuario @gusies que puede aprobar grupos
OWNER_ID = 7116662379  # Tu ID de usuario
APPROVED_GROUPS = set()  # Lista dinámica de grupos aprobados

# Función para aprobar grupos dinámicamente
async def approve_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("❌ No tienes permiso para aprobar grupos.")
        return
    group_id = update.effective_chat.id
    APPROVED_GROUPS.add(group_id)
    await update.message.reply_text(f"✅ Grupo aprobado. ID: `{group_id}`", parse_mode="Markdown")


# Función para manejar el comando /refe
async def refe_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id not in APPROVED_GROUPS:
        await update.message.reply_text("❌ Este grupo no está aprobado para usar este comando.")
        return

    user_message = update.message.reply_to_message
    if not user_message or not user_message.photo:
        await update.message.reply_text("❌ Responde a un mensaje con una foto válida.")
        return

    # Extraer el comentario (texto) del mensaje original
    comment = user_message.caption if user_message.caption else "Sin comentario"

    # Descarga la foto
    photo = user_message.photo[-1]
    file = await context.bot.get_file(photo.file_id)
    await file.download_to_drive("temp_refe.jpg")

    # Formato del mensaje
    user_reference = user_message.from_user.username or "Usuario desconocido"
    message_format = (
        "★ 𝙂𝙤𝙟𝙤 𝙥𝙧𝙤𝙮𝙚𝙘𝙩 ★\n"
        "𖦹๋࣭⭑──────────────𖦹๋࣭⭑\n"
        f"𓆰𓆪 ⁞ 𝐑𝐞𝐟𝐞𝐫𝐞𝐧𝐜𝐢𝐚 𝐝𝐞: @{user_reference}\n"
        f"𓆰𓆪 ⁞ 𝐂𝐨𝐦𝐞𝐧𝐭𝐚𝐫𝐢𝐨: {comment}\n"
        f"𓆰𓆪 ⁞ 𝐀𝐩𝐫𝐨𝐛𝐚𝐝𝐨 𝐩𝐨𝐫: [@gusies](https://t.me/gusies)\n"
        f"𓆰𓆪 ⁞ 𝐅𝐞𝐜𝐡𝐚: {update.message.date.strftime('%Y-%m-%d %H:%M:%S')}\n"
        "✶𖦹๋࣭⭑──────────────𖦹๋࣭⭑✶"
    )

    # Botones interactivos
    keyboard = [
        [InlineKeyboardButton("OWNER 👤", url="https://t.me/gusies")],
        [InlineKeyboardButton("REFERENCIAS 📁", url="https://t.me/gojoproyect")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Envía la foto al canal con formato y botones
    await context.bot.send_photo(
        chat_id=CHANNEL_ID,
        photo=open("temp_refe.jpg", 'rb'),
        caption=message_format,
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

    await update.message.reply_text("✅ ¡Referencia enviada correctamente!")


# Función principal
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("approvegroup", approve_group))
    app.add_handler(CommandHandler("refe", refe_command))
    print("El bot está activo. Presiona Ctrl+C para detenerlo.")
    app.run_polling()


# Ejecuta el bot
if __name__ == "__main__":
    main()
