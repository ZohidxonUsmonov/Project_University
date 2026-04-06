import os
import yt_dlp
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Your Bot Token
TOKEN = "8742752243:AAHTKPdf4fv-i48baNfOspH8Hcm0M-CMMyg"

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Hi! Send me a link from Instagram, TikTok, or YouTube, "
        "and I will download the video for you! 📥"
    )

def download_video(url):
    """Downloads video using yt-dlp and returns the filename."""
    # Options for yt-dlp
    ydl_opts = {
        'format': 'best[ext=mp4]/best', # Get best mp4 quality
        'outtmpl': 'downloads/%(id)s.%(ext)s', # Save in 'downloads' folder
        'max_filesize': 50 * 1024 * 1024, # Limit to 50MB (Telegram free limit)
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        return filename

def handle_message(update: Update, context: CallbackContext):
    url = update.message.text

    # Simple URL validation
    if not any(domain in url for domain in ["instagram.com", "tiktok.com", "youtube.com", "youtu.be"]):
        update.message.reply_text("Please send a valid Instagram, TikTok, or YouTube link. ❌")
        return

    status_msg = update.message.reply_text("Processing your request... Please wait. ⏳")

    try:
        # Create downloads folder if not exists
        if not os.path.exists("downloads"):
            os.makedirs("downloads")

        # Download
        video_path = download_video(url)

        # Send to user
        with open(video_path, 'rb') as video:
            update.message.reply_video(video=video, caption="Done! ✅")

        # Clean up: delete file after sending
        os.remove(video_path)
        status_msg.delete()

    except Exception as e:
        print(f"Error: {e}")
        update.message.reply_text("Sorry, I couldn't download that video. It might be private or too large. 😕")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    print("Bot is running...")
    updater.start_polling()
    updater.idle()

if __name__== "__main__":
    main()
