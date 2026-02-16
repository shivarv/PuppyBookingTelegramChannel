# 🐕 Cane Corso Puppy Sales Telegram Bot

A complete Telegram bot solution for selling Cane Corso puppies online. Perfect for kennels, breeders, and dog businesses who want to engage with customers through Telegram and social media platforms like YouTube.

## ✨ Features

- 🐾 **Puppy Catalog** - Display available puppies with details (age, gender, color, price)
- 📸 **Photo Support** - Show puppy photos in chat
- 💰 **Pricing Info** - Transparent pricing and payment options
- 📝 **Inquiry Forms** - Customers can submit contact information
- 🔔 **Admin Notifications** - Get instant Telegram notifications for new inquiries
- ❓ **FAQ Section** - Answer common customer questions automatically
- 📞 **Contact Info** - Share your phone, email, and location
- ℹ️ **About Section** - Tell customers about your breeding program
- 💾 **Data Storage** - All data stored in easy-to-edit JSON files

## 🚀 Quick Start

1. **Create your bot** with @BotFather on Telegram
2. **Install dependencies**: `pip install -r requirements.txt`
3. **Configure** your bot token and admin ID
4. **Edit** `puppies_data.json` with your actual puppies
5. **Run**: `python3 cane_corso_bot.py`

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed instructions!

## 📱 Perfect for YouTube Marketing

Share your bot link in:
- Video descriptions
- Pinned comments  
- Video cards/end screens
- Community posts

Your Telegram bot link will be: `https://t.me/YourBotUsername`

## 📁 Files Included

- `cane_corso_bot.py` - Main bot code
- `requirements.txt` - Python dependencies
- `puppies_data.json` - Your puppy listings (edit this!)
- `SETUP_GUIDE.md` - Complete setup instructions
- `start_bot.sh` - Linux/Mac startup script
- `start_bot.bat` - Windows startup script

## 🎯 How It Works

1. Customer clicks your bot link from YouTube
2. Bot shows them a menu with options
3. Customer browses available puppies
4. Customer submits inquiry with contact details
5. You receive notification on Telegram
6. You follow up with the customer directly

## 🔧 Customization

The bot is fully customizable:
- Add/remove puppies in `puppies_data.json`
- Edit pricing, FAQ, and contact info
- Add photos (URLs or Telegram file IDs)
- Modify messages and buttons in the code
- Add payment integration (Telegram Payments)

## 📊 Data Management

All data is stored in simple JSON files:
- `puppies_data.json` - Your puppy inventory
- `inquiries.json` - Customer inquiry history

Easy to edit, backup, and manage!

## 🛡️ Security

- Never share your bot TOKEN publicly
- Store TOKEN in environment variables
- Keep inquiry data private (contains customer info)
- Regular backups recommended

## 💡 Tips for Success

1. ✅ Use high-quality puppy photos
2. ✅ Keep pricing transparent and up-to-date
3. ✅ Respond to inquiries within 24 hours
4. ✅ Update puppy availability regularly
5. ✅ Share bot link across all social media
6. ✅ Monitor `inquiries.json` for leads

## 🌐 Hosting Options

Run the bot on:
- Your computer (simple, but needs to stay on)
- Cloud platform (Render, Railway, PythonAnywhere)
- VPS/Server (DigitalOcean, AWS, etc.)
- Raspberry Pi (low-cost 24/7 solution)

## 📞 Support

This bot uses:
- Python 3.8+
- python-telegram-bot library
- JSON for data storage

Check the code comments for detailed explanations of each function.

## ⚖️ Legal Compliance

Ensure you comply with:
- Local dog breeding regulations
- Business licensing requirements
- Consumer protection laws
- Data privacy regulations (customer info)
- Telegram Terms of Service

## 🐾 About Cane Corso

This bot is specifically designed for Cane Corso breeders but can easily be adapted for any dog breed by editing the text and puppy data.

---

**Ready to start?** Check out [SETUP_GUIDE.md](SETUP_GUIDE.md) for step-by-step instructions!

**Questions?** Review the code - it's well-commented and easy to understand!

Happy breeding! 🐕❤️
