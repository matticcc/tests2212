import os
import requests
from pyrogram import Client, filters

# Fetch sensitive information from environment variables
API_TOKEN = os.environ.get('8485756680:AAGVFEWAoJVibhhxykidh_uo-70kZ5naLLE')
API_ID = os.environ.get('21258990')
API_HASH = os.environ.get('90bc74918c15b3d707b2cb8e7af2cf04')

# Define the binlist API URL (using Binlist as an example)
BINLIST_API_URL = "https://lookup.binlist.net/"

# Create the Pyrogram bot client
app = Client("bin_checker_bot", api_id=API_ID, api_hash=API_HASH, bot_token=API_TOKEN)

# Function to get bank details from BIN
def get_bin_info(bin_number):
    response = requests.get(BINLIST_API_URL + bin_number)
    if response.status_code == 200:
        data = response.json()
        bank_info = {
            'bank': data.get('bank', {}).get('name', 'Unknown'),
            'country': data.get('country', {}).get('name', 'Unknown'),
            'type': data.get('type', 'Unknown'),
            'brand': data.get('brand', 'Unknown'),
        }
        return bank_info
    else:
        return None

@app.on_message(filters.command('start'))
async def start(client, message):
    await message.reply("Welcome! Send me a BIN number and I'll tell you which bank and country it belongs to.")

@app.on_message(filters.text)
async def bin_lookup(client, message):
    # Get the bin number from the message
    bin_number = message.text.strip()

    # Ensure the user sent a valid BIN
    if not bin_number.isdigit() or len(bin_number) < 6:
        await message.reply("Please send a valid BIN number (6 digits or more).")
        return
    
    # Fetch bank info
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
        reply_text = "Sorry, I couldn't find any information for this BIN."

    # Send the result back to the user
    await message.reply(reply_text)

if __name__ == "__main__":
    app.run()
