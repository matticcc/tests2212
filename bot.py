import os
import requests
from pyrogram.enums import ParseMode
from pyrogram import Client, filters
from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent

# -----------------------------
# Configuration (replace these with your values)
API_TOKEN = "8485756680:AAGVFEWAoJVibhhxykidh_uo-70kZ5naLLE"
API_ID = 21258990  # Replace with your API ID (integer)
API_HASH = "90bc74918c15b3d707b2cb8e7af2cf04"
# -----------------------------

BINLIST_API_URL = "https://lookup.binlist.net/"

# Pyrogram bot client
app = Client("bin_checker_bot", api_id=API_ID, api_hash=API_HASH, bot_token=API_TOKEN)

# Function to get BIN info from API
def get_bin_info(bin_number):
    try:
        headers = {
            "Accept-Version": "3",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Accept": "application/json",
            "Connection": "keep-alive"
        }
        response = requests.get(BINLIST_API_URL + bin_number, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {
                'bank': data.get('bank', {}).get('name', 'Unknown'),
                'country': data.get('country', {}).get('name', 'Unknown'),
                'type': data.get('type', 'Unknown'),
                'brand': data.get('brand', 'Unknown'),
            }
        else:
            print(f"BIN API Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Exception in get_bin_info(): {e}")
    return None

# /start command
@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("Welcome! Send me a BIN number (6+ digits) and I’ll tell you which bank and country it belongs to.\n\n"
                        "Or use me inline by typing `@YourBotUsername <BIN>` in any chat.",
                        quote=True)

# Handle regular messages (non-command text)
@app.on_message(filters.text & ~filters.command(["start"]))
async def bin_lookup(client, message):
    bin_number = message.text.strip()
    if not bin_number.isdigit() or len(bin_number) < 6:
        await message.reply("❌ Please send a valid BIN number (6 digits or more).", quote=True)
        return

    bank_info = get_bin_info(bin_number)
    if bank_info:
        reply_text = (
            f"**BIN Information:**\n"
            f"**Bank:** {bank_info['bank']}\n"
            f"**Country:** {bank_info['country']}\n"
            f"**Type:** {bank_info['type']}\n"
            f"**Brand:** {bank_info['brand']}"
        )
    else:
        reply_text = "❌ Sorry, I couldn't find any information for this BIN."

    await message.reply(reply_text, quote=True)

# Inline mode handler
@app.on_inline_query()
async def inline_handler(client, inline_query):
    query = inline_query.query.strip()
    print(f"[INLINE QUERY] User: {inline_query.from_user.id}, Query: '{query}'")

    if not query.isdigit() or len(query) < 6:
        await inline_query.answer([], cache_time=1)
        return

    bank_info = get_bin_info(query)

    if bank_info:
        result_text = (
            f"**BIN Information:**\n"
            f"**Bank:** {bank_info['bank']}\n"
            f"**Country:** {bank_info['country']}\n"
            f"**Type:** {bank_info['type']}\n"
            f"**Brand:** {bank_info['brand']}"
        )
    else:
        result_text = "❌ Sorry, I couldn't find any information for this BIN."

    await inline_query.answer(
        results=[
            InlineQueryResultArticle(
                title=f"BIN Info: {query}",
                description=f"Bank: {bank_info['bank'] if bank_info else 'Not found'}",
                input_message_content=InputTextMessageContent(
                    result_text,
                    parse_mode=ParseMode.MARKDOWN
                )
            )
        ],
        cache_time=1
    )

# Start the bot
if __name__ == "__main__":
    app.run()
