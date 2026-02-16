# Cane Corso Puppy Sales Telegram Bot - Setup Guide

## Features
✅ View available puppies with details
✅ Pricing information
✅ FAQ section
✅ Customer inquiry form
✅ Contact information
✅ About your breeding program
✅ Admin notifications for new inquiries
✅ Data stored in JSON files

## Setup Instructions

### Step 1: Create Your Telegram Bot

1. Open Telegram and search for **@BotFather**
2. Start a chat and send `/newbot`
3. Choose a name for your bot (e.g., "Cane Corso Puppies")
4. Choose a username ending in "bot" (e.g., "YourKennelCaneCorsBot")
5. BotFather will give you a **TOKEN** - save this!

### Step 2: Get Your Admin User ID (to receive inquiries)

1. Search for **@userinfobot** on Telegram
2. Start a chat - it will show your User ID
3. Copy this number

### Step 3: Install Python Requirements

```bash
# Make sure you have Python 3.8+ installed
python3 --version

# Install dependencies
pip install -r requirements.txt
```

### Step 4: Configure the Bot

1. Open `cane_corso_bot.py` in a text editor
2. Find line 32: `ADMIN_ID = None`
3. Replace with your User ID: `ADMIN_ID = 123456789`  (your actual ID)

### Step 5: Set Your Bot Token

**Option A - Environment Variable (Recommended):**
```bash
# Linux/Mac
export TELEGRAM_BOT_TOKEN="your_token_here"

# Windows Command Prompt
set TELEGRAM_BOT_TOKEN=your_token_here

# Windows PowerShell
$env:TELEGRAM_BOT_TOKEN="your_token_here"
```

**Option B - Directly in code:**
Edit `cane_corso_bot.py` line 337:
```python
TOKEN = "YOUR_BOT_TOKEN_HERE"  # Replace the os.getenv line
```

### Step 6: Customize Your Puppy Data

The bot automatically creates `puppies_data.json` on first run with sample data.

Edit this file to add your actual puppies:

```json
{
  "puppies": [
    {
      "id": 1,
      "name": "Bruno",
      "age": "8 weeks",
      "gender": "Male",
      "color": "Black Brindle",
      "price": "$2,500",
      "available": true,
      "description": "Healthy, vaccinated, champion bloodline",
      "photo_url": null
    }
  ],
  "about": "Your kennel description here...",
  "contact_info": {
    "phone": "+1-XXX-XXX-XXXX",
    "email": "your@email.com",
    "location": "Your City, State"
  }
}
```

### Step 7: Run the Bot

```bash
python3 cane_corso_bot.py
```

You should see: "Bot is starting..."

### Step 8: Test Your Bot

1. Open Telegram
2. Search for your bot username
3. Click Start
4. Test all the features!

## Adding Photos to Puppies

### Method 1: Using Photo URLs
If you have photos hosted online (Instagram, Google Drive public link, etc.):
```json
"photo_url": "https://example.com/puppy.jpg"
```

### Method 2: Using Telegram File IDs (Recommended)
1. Send a photo to your bot
2. The bot will log the file_id
3. Use that file_id in your JSON:
```json
"photo_url": "AgACAgIAAxkBAAI..."
```

## For Your YouTube Link

Create a short link to your bot:
```
https://t.me/YourBotUsername
```

Or create a direct start link:
```
https://t.me/YourBotUsername?start=youtube
```

Put this in your YouTube:
- Video description
- Pinned comment
- Cards/End screen (as a link)

## Running 24/7

### Option 1: Your Computer
Keep the terminal/command prompt running

### Option 2: Free Cloud Hosting
- **Render.com** (Free tier available)
- **Railway.app** (Free trial)
- **PythonAnywhere** (Free tier)
- **Heroku** (Paid)

### Option 3: Raspberry Pi
Run it on a Raspberry Pi at home

## Files Created by Bot

- `puppies_data.json` - Your puppy listings and info
- `inquiries.json` - Customer inquiries (you'll receive these via Telegram too)

## Customization Ideas

1. **Add more puppies:** Edit `puppies_data.json`
2. **Change pricing:** Update the pricing section in the code
3. **Modify FAQ:** Edit the `show_faq` function
4. **Add payment integration:** You can add Telegram Payments
5. **Add photo galleries:** Store multiple photos per puppy
6. **Add video support:** Include video links

## Troubleshooting

**Bot doesn't start:**
- Check your TOKEN is correct
- Make sure python-telegram-bot is installed
- Check internet connection

**Not receiving admin notifications:**
- Verify ADMIN_ID is set correctly
- Make sure you've started a chat with your bot first

**Photos not showing:**
- Use valid URLs or Telegram file_ids
- Check photo file size (must be under 10MB)

## Security Tips

1. ❌ Never share your bot TOKEN publicly
2. ✅ Use environment variables for the token
3. ✅ Keep `inquiries.json` private (contains customer data)
4. ✅ Regularly backup your data files

## Next Steps

1. Test all features thoroughly
2. Add your actual puppy listings
3. Upload quality photos
4. Update contact information
5. Share your bot link on YouTube
6. Promote on social media

## Support

If you need help:
- Read the python-telegram-bot documentation
- Check the code comments
- Test each feature one by one

## Legal Note

Make sure you comply with:
- Local breeding regulations
- Consumer protection laws
- Data privacy laws (customer information)
- Telegram's Terms of Service

---

Good luck with your Cane Corso puppy sales! 🐕
