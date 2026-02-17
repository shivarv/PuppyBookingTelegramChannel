#!/usr/bin/env python3
"""
Cane Corso Puppy Sales Telegram Bot
Helps customers inquire about and purchase Cane Corso puppies
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters
)
import json
import os
from datetime import datetime
from aiohttp import web
import asyncio
import threading

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ Loading configuration from .env file")
except ImportError:
    print("⚠️  python-dotenv not installed. Install with: pip install python-dotenv")
    print("Using system environment variables instead...")

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Conversation states
CONTACT_NAME, CONTACT_PHONE, CONTACT_EMAIL, INQUIRY_MESSAGE = range(4)

# Data file for puppies
PUPPIES_FILE = 'puppies_data.json'
INQUIRIES_FILE = 'inquiries.json'

# Admin user ID (loaded from environment variable)
ADMIN_ID = os.getenv('TELEGRAM_ADMIN_ID')
if ADMIN_ID:
    try:
        ADMIN_ID = int(ADMIN_ID)
        print(f"✅ Admin ID configured: {ADMIN_ID}")
    except ValueError:
        print(f"⚠️  Invalid TELEGRAM_ADMIN_ID: {ADMIN_ID}")
        ADMIN_ID = None
else:
    print("⚠️  TELEGRAM_ADMIN_ID not set - you won't receive inquiry notifications")


class PuppyBot:
    def __init__(self):
        self.puppies = self.load_puppies()
        self.inquiries = self.load_inquiries()
    
    def load_puppies(self):
        """Load puppy data from JSON file"""
        if os.path.exists(PUPPIES_FILE):
            with open(PUPPIES_FILE, 'r') as f:
                return json.load(f)
        else:
            # Default sample data
            default_data = {
                "puppies": [
                    {
                        "id": 1,
                        "name": "Bruno",
                        "age": "8 weeks",
                        "gender": "Male",
                        "color": "Black Brindle",
                        "price": "$2,500",
                        "available": True,
                        "description": "Healthy, vaccinated, champion bloodline",
                        "photo_url": None
                    },
                    {
                        "id": 2,
                        "name": "Luna",
                        "age": "10 weeks",
                        "gender": "Female",
                        "color": "Blue/Grey",
                        "price": "$2,800",
                        "available": True,
                        "description": "Beautiful temperament, first shots completed",
                        "photo_url": None
                    }
                ],
                "about": "We breed premium Cane Corso puppies with excellent temperament and champion bloodlines. All puppies come with health certificates, first vaccinations, and a health guarantee.",
                "contact_info": {
                    "phone": "+1-XXX-XXX-XXXX",
                    "email": "info@canecorsopuppies.com",
                    "location": "Your Location"
                }
            }
            self.save_puppies(default_data)
            return default_data
    
    def save_puppies(self, data):
        """Save puppy data to JSON file"""
        with open(PUPPIES_FILE, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_inquiries(self):
        """Load inquiries from JSON file"""
        if os.path.exists(INQUIRIES_FILE):
            with open(INQUIRIES_FILE, 'r') as f:
                return json.load(f)
        return []
    
    def save_inquiry(self, inquiry):
        """Save a new inquiry"""
        self.inquiries.append(inquiry)
        with open(INQUIRIES_FILE, 'w') as f:
            json.dump(self.inquiries, f, indent=2)


bot_data = PuppyBot()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send welcome message with main menu"""
    keyboard = [
        [InlineKeyboardButton("🐕 View Available Puppies", callback_data='view_puppies')],
        [InlineKeyboardButton("ℹ️ About Our Breeding", callback_data='about')],
        [InlineKeyboardButton("💰 Pricing Information", callback_data='pricing')],
        [InlineKeyboardButton("📞 Contact Us", callback_data='contact')],
        [InlineKeyboardButton("❓ FAQ", callback_data='faq')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = (
        "🐾 *Welcome to Our Cane Corso Kennel!* 🐾\n\n"
        "We specialize in breeding premium Cane Corso puppies with "
        "excellent temperament and champion bloodlines.\n\n"
        "How can we help you today?"
    )
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button presses"""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'main_menu':
        await show_main_menu(query)
    elif query.data == 'view_puppies':
        await show_puppies(query)
    elif query.data.startswith('puppy_'):
        await show_puppy_details(query)
    elif query.data == 'about':
        await show_about(query)
    elif query.data == 'pricing':
        await show_pricing(query)
    elif query.data == 'contact':
        await show_contact(query)
    elif query.data == 'faq':
        await show_faq(query)
    elif query.data == 'start_inquiry':
        await start_inquiry(query, context)


async def show_main_menu(query):
    """Show the main menu"""
    keyboard = [
        [InlineKeyboardButton("🐕 View Available Puppies", callback_data='view_puppies')],
        [InlineKeyboardButton("ℹ️ About Our Breeding", callback_data='about')],
        [InlineKeyboardButton("💰 Pricing Information", callback_data='pricing')],
        [InlineKeyboardButton("📞 Contact Us", callback_data='contact')],
        [InlineKeyboardButton("❓ FAQ", callback_data='faq')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "🐾 *Main Menu* 🐾\n\nHow can we help you?",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


async def show_puppies(query):
    """Show list of available puppies"""
    available_puppies = [p for p in bot_data.puppies['puppies'] if p['available']]
    
    if not available_puppies:
        keyboard = [[InlineKeyboardButton("⬅️ Back to Menu", callback_data='main_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "Currently no puppies available. Please check back soon or contact us for upcoming litters!",
            reply_markup=reply_markup
        )
        return
    
    keyboard = []
    for puppy in available_puppies:
        button_text = f"{puppy['name']} - {puppy['gender']} ({puppy['age']})"
        keyboard.append([InlineKeyboardButton(button_text, callback_data=f"puppy_{puppy['id']}")])
    
    keyboard.append([InlineKeyboardButton("⬅️ Back to Menu", callback_data='main_menu')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = f"*🐕 Available Puppies ({len(available_puppies)})*\n\nSelect a puppy to view details:"
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')


async def show_puppy_details(query):
    """Show details of a specific puppy"""
    puppy_id = int(query.data.split('_')[1])
    puppy = next((p for p in bot_data.puppies['puppies'] if p['id'] == puppy_id), None)
    
    if not puppy:
        await query.edit_message_text("Puppy not found!")
        return
    
    details = (
        f"*🐕 {puppy['name']}*\n\n"
        f"*Gender:* {puppy['gender']}\n"
        f"*Age:* {puppy['age']}\n"
        f"*Color:* {puppy['color']}\n"
        f"*Price:* {puppy['price']}\n"
        f"*Status:* {'✅ Available' if puppy['available'] else '❌ Sold'}\n\n"
        f"*Description:*\n{puppy['description']}\n"
    )
    
    keyboard = [
        [InlineKeyboardButton("📝 Inquire About This Puppy", callback_data='start_inquiry')],
        [InlineKeyboardButton("⬅️ Back to Puppies", callback_data='view_puppies')],
        [InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # If photo is available, send it
    if puppy.get('photo_url'):
        # Note: You'll need to upload photos and get their file_id or use URLs
        await query.message.reply_photo(
            photo=puppy['photo_url'],
            caption=details,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        await query.delete_message()
    else:
        await query.edit_message_text(details, reply_markup=reply_markup, parse_mode='Markdown')


async def show_about(query):
    """Show about information"""
    about_text = (
        f"*ℹ️ About Our Kennel*\n\n"
        f"{bot_data.puppies['about']}\n\n"
        f"*What's Included:*\n"
        f"✅ Health Certificate\n"
        f"✅ First Vaccinations\n"
        f"✅ Deworming\n"
        f"✅ Health Guarantee\n"
        f"✅ Microchip\n"
        f"✅ Puppy Starter Pack\n"
    )
    
    keyboard = [[InlineKeyboardButton("⬅️ Back to Menu", callback_data='main_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(about_text, reply_markup=reply_markup, parse_mode='Markdown')


async def show_pricing(query):
    """Show pricing information"""
    pricing_text = (
        "*💰 Pricing Information*\n\n"
        "*Standard Puppies:* $2,500 - $3,000\n"
        "*Premium Bloodline:* $3,500 - $4,500\n"
        "*Champion Bloodline:* $5,000+\n\n"
        "*Payment Options:*\n"
        "• Full payment\n"
        "• Deposit to reserve ($500)\n"
        "• Payment plans available\n\n"
        "*What Affects Price:*\n"
        "• Bloodline\n"
        "• Color\n"
        "• Gender\n"
        "• Show quality vs. Pet quality\n\n"
        "Contact us for specific pricing on available puppies!"
    )
    
    keyboard = [
        [InlineKeyboardButton("📞 Contact Us", callback_data='contact')],
        [InlineKeyboardButton("⬅️ Back to Menu", callback_data='main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(pricing_text, reply_markup=reply_markup, parse_mode='Markdown')


async def show_contact(query):
    """Show contact information"""
    contact = bot_data.puppies['contact_info']
    contact_text = (
        "*📞 Contact Information*\n\n"
        f"*Phone:* {contact['phone']}\n"
        f"*Email:* {contact['email']}\n"
        f"*Location:* {contact['location']}\n\n"
        "We respond to inquiries within 24 hours!\n\n"
        "You can also submit an inquiry through this bot:"
    )
    
    keyboard = [
        [InlineKeyboardButton("📝 Submit Inquiry", callback_data='start_inquiry')],
        [InlineKeyboardButton("⬅️ Back to Menu", callback_data='main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(contact_text, reply_markup=reply_markup, parse_mode='Markdown')


async def show_faq(query):
    """Show frequently asked questions"""
    faq_text = (
        "*❓ Frequently Asked Questions*\n\n"
        "*Q: What age can I take my puppy home?*\n"
        "A: Puppies are ready at 8-10 weeks old.\n\n"
        "*Q: Are the puppies vaccinated?*\n"
        "A: Yes, first shots and deworming completed.\n\n"
        "*Q: Do you offer shipping?*\n"
        "A: Yes, we can arrange safe transport.\n\n"
        "*Q: What is your health guarantee?*\n"
        "A: 2-year health guarantee against genetic defects.\n\n"
        "*Q: Can I visit the puppies?*\n"
        "A: Yes! We encourage visits by appointment.\n\n"
        "*Q: Do you require a deposit?*\n"
        "A: Yes, $500 deposit to reserve a puppy.\n"
    )
    
    keyboard = [[InlineKeyboardButton("⬅️ Back to Menu", callback_data='main_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(faq_text, reply_markup=reply_markup, parse_mode='Markdown')


async def start_inquiry(query, context):
    """Start the inquiry conversation"""
    await query.edit_message_text(
        "📝 *Submit an Inquiry*\n\n"
        "Please provide your name:",
        parse_mode='Markdown'
    )
    return CONTACT_NAME


async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get customer name"""
    context.user_data['name'] = update.message.text
    await update.message.reply_text(
        "Thanks! Now please provide your phone number:"
    )
    return CONTACT_PHONE


async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get customer phone"""
    context.user_data['phone'] = update.message.text
    await update.message.reply_text(
        "Great! What's your email address?"
    )
    return CONTACT_EMAIL


async def get_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get customer email"""
    context.user_data['email'] = update.message.text
    await update.message.reply_text(
        "Perfect! Please tell us about your inquiry:\n"
        "(What would you like to know? Which puppy interests you?)"
    )
    return INQUIRY_MESSAGE


async def get_inquiry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Save the inquiry"""
    context.user_data['message'] = update.message.text
    
    # Save inquiry
    inquiry = {
        'date': datetime.now().isoformat(),
        'name': context.user_data['name'],
        'phone': context.user_data['phone'],
        'email': context.user_data['email'],
        'message': context.user_data['message'],
        'user_id': update.effective_user.id
    }
    
    bot_data.save_inquiry(inquiry)
    
    # Notify admin if set
    if ADMIN_ID:
        admin_message = (
            f"🔔 *New Inquiry!*\n\n"
            f"*Name:* {inquiry['name']}\n"
            f"*Phone:* {inquiry['phone']}\n"
            f"*Email:* {inquiry['email']}\n\n"
            f"*Message:*\n{inquiry['message']}"
        )
        try:
            await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=admin_message,
                parse_mode='Markdown'
            )
        except Exception as e:
            logger.error(f"Failed to notify admin: {e}")
    
    # Confirm to user
    keyboard = [[InlineKeyboardButton("🏠 Back to Menu", callback_data='main_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "✅ *Thank you for your inquiry!*\n\n"
        "We've received your message and will contact you within 24 hours.\n\n"
        "In the meantime, feel free to explore more about our puppies!",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel the conversation"""
    await update.message.reply_text(
        "Inquiry cancelled. Type /start to return to the main menu."
    )
    return ConversationHandler.END


async def health_check(request):
    """Health check endpoint for Render"""
    return web.Response(text="🐕 Cane Corso Bot is running!")


async def start_web_server():
    """Start health check web server for Render"""
    app = web.Application()
    app.router.add_get('/', health_check)
    app.router.add_get('/health', health_check)
    
    port = int(os.getenv('PORT', 10000))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"✅ Health check server running on port {port}")
    return runner


async def main_async():
    """Main async function"""
    # Get token from environment variable
    TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not TOKEN:
        print("\n" + "="*50)
        print("❌ ERROR: TELEGRAM_BOT_TOKEN not found!")
        print("="*50)
        print("\nPlease set your bot token in environment variables")
        print("="*50 + "\n")
        return
    
    print(f"✅ Bot token configured")
    
    # Start web server for Render health checks
    web_runner = await start_web_server()
    
    # Create application
    application = Application.builder().token(TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # Inquiry conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_inquiry, pattern='^start_inquiry$')],
        states={
            CONTACT_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            CONTACT_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
            CONTACT_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_email)],
            INQUIRY_MESSAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_inquiry)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    application.add_handler(conv_handler)
    
    # Start the bot
    print("\n" + "="*50)
    print("🚀 Bot is starting...")
    print("="*50)
    print("✅ Ready to accept connections!")
    print("💬 Users can now chat with your bot on Telegram")
    print("🔔 You'll receive inquiry notifications on Telegram")
    print("\nBot will run continuously...")
    print("="*50 + "\n")
    
    # Initialize and start polling
    await application.initialize()
    await application.start()
    await application.updater.start_polling(allowed_updates=Update.ALL_TYPES)
    
    # Keep running
    try:
        await asyncio.Event().wait()
    except (KeyboardInterrupt, SystemExit):
        print("\nShutting down...")
        await application.updater.stop()
        await application.stop()
        await application.shutdown()
        await web_runner.cleanup()


def main():
    """Entry point"""
    asyncio.run(main_async())


if __name__ == '__main__':
    main()