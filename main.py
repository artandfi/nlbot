import os
from telegram import Update, ForceReply
from telegram.ext import Application, ContextTypes, CommandHandler, Updater, MessageHandler, filters
from preprocessing import preprocess
from sentiment import get_sentiment_score


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "creds.json"
help_text = "Type in some text, and I'll sentiment-analyze it for you."


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(f"Hi {user.mention_html()}! {help_text}")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text(help_text)


async def respond(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Respond with a sentiment score of user-provided text."""
    user_input = update.message.text
    user_input = preprocess(user_input)
    sentiment_score = get_sentiment_score(user_input)
    status = (
        "NEGATIVE | 🔴" if sentiment_score <= -0.25 else
        "NEUTRAL | 🟡" if sentiment_score <= 0.25 else
        "POSITIVE | 🟢"
    )

    await update.message.reply_text(f"Score: {sentiment_score} | {status}")


def main() -> None:
    """Start the bot."""
    with open("bot_token.txt") as f:
        bot_token = f.read()

    # Create the Application and pass it your bot's token.
    application = Application.builder().token(bot_token).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))

    # on non-command i.e message - make a response
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, respond))

    # Run the bot until its owner presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
