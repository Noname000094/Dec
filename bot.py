import os
import logging
from pyrogram import Client, filters
from cryptography.fernet import Fernet

# Telegram API credentials
API_ID = "your_api_id"
API_HASH = "your_api_hash"
BOT_TOKEN = "your_bot_token"

# Initialize the bot
app = Client("encryption_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Generate encryption key (Save this key securely)
KEY = Fernet.generate_key()
cipher = Fernet(KEY)

logging.basicConfig(level=logging.INFO)

@app.on_message(filters.command("start"))
async def start(_, message):
    await message.reply_text(
        "🔐 Welcome to the Encryption Bot!\n\n"
        "Use /encrypt to encrypt a file.\n"
        "Use /decrypt to decrypt a file.\n"
    )

@app.on_message(filters.command("encrypt"))
async def encrypt_command(_, message):
    await message.reply_text("📂 Send the Python or PHP file you want to encrypt.")

@app.on_message(filters.command("decrypt"))
async def decrypt_command(_, message):
    await message.reply_text("📂 Send the encrypted file (.enc) to decrypt.")

@app.on_message(filters.document)
async def handle_document(_, message):
    file_extension = message.document.file_name.split(".")[-1]

    if file_extension not in ["py", "php", "enc"]:
        await message.reply_text("❌ Unsupported file type. Send a .py or .php file.")
        return

    file_path = await message.download()
    
    if file_extension == "enc":
        decrypted_path = file_path.replace(".enc", "")
        with open(file_path, "rb") as enc_file:
            encrypted_data = enc_file.read()
        decrypted_data = cipher.decrypt(encrypted_data)
        with open(decrypted_path, "wb") as dec_file:
            dec_file.write(decrypted_data)
        
        await message.reply_document(decrypted_path, caption="✅ Decryption complete!")
        os.remove(file_path)
        os.remove(decrypted_path)

    else:
        encrypted_path = f"{file_path}.enc"
        with open(file_path, "rb") as original_file:
            original_data = original_file.read()
        encrypted_data = cipher.encrypt(original_data)
        with open(encrypted_path, "wb") as enc_file:
            enc_file.write(encrypted_data)

        await message.reply_document(encrypted_path, caption="🔒 Encryption complete!")
        os.remove(file_path)
        os.remove(encrypted_path)

if __name__ == "__main__":
    app.run()
    