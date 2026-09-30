 import os

 from telegram import (
     Update,
     InlineKeyboardButton,
     InlineKeyboardMarkup,
 )
 from telegram.ext import (
     Application,
     CommandHandler,
     CallbackQueryHandler,
     MessageHandler,
     ContextTypes,
     filters,
 )

 TOKEN = os.getenv("BOT_TOKEN")


 # =========================
 # MAIN MENU
 # =========================

 def main_menu():
     keyboard = [
         [
             InlineKeyboardButton(
                 "🇮🇳 Malayalam Movies",
                 callback_data="malayalam"
             )
         ],
         [
             InlineKeyboardButton(
                 "🎬 Malayalam Dubbed Movies",
                 callback_data="dubbed"
             )
         ],
         [
             InlineKeyboardButton(
                 "🆕 Latest Malayalam Movies",
                 callback_data="latest"
             )
         ],
         [
             InlineKeyboardButton(
                 "🎞️ Request for a movie",
                 callback_data="request"
             )
         ],
     ]

     return InlineKeyboardMarkup(keyboard)


 # =========================
 # YEAR MENU
 # =========================

 def year_menu(back="main"):
     keyboard = [
         [
             InlineKeyboardButton("2026", callback_data=f"year_2026_{back}"),
             InlineKeyboardButton("2025", callback_data=f"year_2025_{back}"),
         ],
         [
             InlineKeyboardButton("2024", callback_data=f"year_2024_{back}"),
             InlineKeyboardButton("2023", callback_data=f"year_2023_{back}"),
         ],
         [
             InlineKeyboardButton("2022", callback_data=f"year_2022_{back}"),
             InlineKeyboardButton("2021", callback_data=f"year_2021_{back}"),
         ],
         [
             InlineKeyboardButton("🔙 Go Back", callback_data="main")
         ],
     ]

     return InlineKeyboardMarkup(keyboard)


 # =========================
 # START
 # =========================

 async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
     await update.message.reply_text(
         "🎬 *NOVA MOVIES BOT*\n\n"
         "Welcome! 👋\n"
         "Choose an option below:",
         reply_markup=main_menu(),
         parse_mode="Markdown",
     )


 # =========================
 # BUTTON HANDLER
 # =========================

 async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
     query = update.callback_query
     await query.answer()

     data = query.data

     # Main menu
     if data == "main":
         await query.edit_message_text(
             "🎬 *NOVA MOVIES BOT*\n\nChoose an option:",
             reply_markup=main_menu(),
             parse_mode="Markdown",
         )
         return

     # Malayalam movies
     if data == "malayalam":
         await query.edit_message_text(
             "🇮🇳 *Malayalam Movies*\n\n"
             "Select a year:",
             reply_markup=year_menu("malayalam"),
             parse_mode="Markdown",
         )
         return

     # Dubbed movies
     if data == "dubbed":
         await query.edit_message_text(
             "🎬 *Malayalam Dubbed Movies*\n\n"
             "Select a year:",
             reply_markup=year_menu("dubbed"),
             parse_mode="Markdown",
         )
         return

     # Latest movies
     if data == "latest":
         await query.edit_message_text(
             "🆕 *Latest Malayalam Movies*\n\n"
             "Select a year:",
             reply_markup=year_menu("latest"),
             parse_mode="Markdown",
         )
         return

     # Movie request
     if data == "request":
         await query.edit_message_text(
             "🎞️ *Movie Request*\n\n"
             "Please send me the movie name you want.\n\n"
             "Example:\n"
             "`Aavesham`",
             parse_mode="Markdown",
         )
         return

     # Year selection
     if data.startswith("year_"):
         parts = data.split("_")

         year = parts[1]
         category = parts[2]

         await query.edit_message_text(
             f"🎬 *{year} Movies*\n\n"
             "Movie list will be added here.\n\n"
             "🔗 Only official/legal viewing links should be used.",
             reply_markup=InlineKeyboardMarkup([
                 [
                     InlineKeyboardButton(
                         "🔙 Go Back",
                         callback_data=category
                     )
                 ],
                 [
                     InlineKeyboardButton(
                         "🏠 Main Menu",
                         callback_data="main"
                     )
                 ],
             ]),
             parse_mode="Markdown",
         )
         return


 # =========================
 # MOVIE REQUEST MESSAGE
 # =========================

 async def movie_request(
     update: Update,
     context: ContextTypes.DEFAULT_TYPE
 ):
     text = update.message.text

     await update.message.reply_text(
         f"🎞️ Movie request received!\n\n"
         f"🎬 Movie: {text}\n\n"
         "We will check for an official/legal viewing option."
     )


 # =========================
 # RUN BOT
 # =========================

 def main():
     if not TOKEN:
         print("ERROR: BOT_TOKEN is not set.")
         return

     app = Application.builder().token(TOKEN).build()

     app.add_handler(CommandHandler("start", start))
     app.add_handler(CallbackQueryHandler(buttons))
     app.add_handler(
         MessageHandler(
             filters.TEXT & ~filters.COMMAND,
             movie_request
         )
     )

     print("NOVA BOT started successfully!")

     app.run_polling()


 if __name__ == "__main__":
     main()