import os
from datetime import date, datetime
import asyncio

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from main import download_and_merge_sec_filings


DEFAULT_START = "2023-01-01"


def ensure_defaults(user_data: dict) -> None:
    user_data.setdefault("start_date", DEFAULT_START)
    user_data.setdefault("end_date", date.today().isoformat())
    user_data.setdefault("verbose", False)


async def ini(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    ensure_defaults(context.user_data)
    if not context.args:
        await update.message.reply_text("Uso: /ini YYYY-MM-DD")
        return
    try:
        datetime.strptime(context.args[0], "%Y-%m-%d")
    except ValueError:
        await update.message.reply_text("Fecha inválida, usa YYYY-MM-DD.")
        return
    context.user_data["start_date"] = context.args[0]
    await update.message.reply_text(f"Fecha inicial establecida en {context.args[0]}.")


async def fin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    ensure_defaults(context.user_data)
    if not context.args:
        await update.message.reply_text("Uso: /fin YYYY-MM-DD")
        return
    try:
        datetime.strptime(context.args[0], "%Y-%m-%d")
    except ValueError:
        await update.message.reply_text("Fecha inválida, usa YYYY-MM-DD.")
        return
    context.user_data["end_date"] = context.args[0]
    await update.message.reply_text(f"Fecha final establecida en {context.args[0]}.")


async def ticker(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    ensure_defaults(context.user_data)
    if not context.args:
        await update.message.reply_text("Uso: /ticker TICKER")
        return
    ticker_value = context.args[0].upper()
    context.user_data["ticker"] = ticker_value
    await update.message.reply_text(f"Ticker establecido en {ticker_value}.")


async def v(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    ensure_defaults(context.user_data)
    context.user_data["verbose"] = not context.user_data.get("verbose", False)
    mode = "verbose" if context.user_data["verbose"] else "normal"
    await update.message.reply_text(f"Modo {mode} activado.")


async def get_docs(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    ensure_defaults(context.user_data)
    ticker_value = context.user_data.get("ticker")
    if not ticker_value:
        await update.message.reply_text("Debes establecer un ticker con /ticker <TICKER>")
        return
    start = context.user_data["start_date"]
    end = context.user_data["end_date"]
    verbose = context.user_data.get("verbose", False)

    def send_verbose(text: str) -> None:
        loop = asyncio.get_running_loop()
        loop.create_task(update.message.reply_text(text))

    pdf_path = download_and_merge_sec_filings(
        ticker_value,
        start,
        end,
        verbose_callback=send_verbose if verbose else None,
    )
    with open(pdf_path, "rb") as pdf_file:
        await update.message.reply_document(pdf_file)


def main() -> None:
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("ini", ini))
    application.add_handler(CommandHandler("fin", fin))
    application.add_handler(CommandHandler("ticker", ticker))
    application.add_handler(CommandHandler("get", get_docs))
    application.add_handler(CommandHandler("v", v))

    application.run_polling()


if __name__ == "__main__":
    main()
