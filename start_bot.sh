#!/bin/bash

# Quick Start Script for Cane Corso Telegram Bot

echo "======================================"
echo "Cane Corso Puppy Bot - Quick Start"
echo "======================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "â Python3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "â Python found: $(python3 --version)"
echo ""

# Check if requirements are installed
echo "đĻ Checking dependencies..."
if ! python3 -c "import telegram" 2>/dev/null; then
    echo "Installing required packages..."
    pip install -r requirements.txt
else
    echo "â Dependencies already installed"
fi
echo ""

# Check for bot token
if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
    echo "â ī¸  TELEGRAM_BOT_TOKEN not set!"
    echo ""
    echo "Please set your bot token:"
    echo "  export TELEGRAM_BOT_TOKEN='your_token_here'"
    echo ""
    echo "Or edit cane_corso_bot.py and add it directly in the code."
    echo ""
    read -p "Do you want to enter it now? (y/n): " answer
    if [ "$answer" = "y" ]; then
        read -p "Enter your bot token: " token
        export TELEGRAM_BOT_TOKEN="$token"
    else
        exit 1
    fi
fi

echo "â Bot token configured"
echo ""

# Check if puppies_data.json exists
if [ ! -f "puppies_data.json" ]; then
    echo "âšī¸  puppies_data.json will be created automatically"
fi

echo "======================================"
echo "đ Starting bot..."
echo "======================================"
echo ""
echo "Bot is running! Press Ctrl+C to stop."
echo ""

if [ -d "venv" ]; then
    echo "✅ Activating virtual environment..."
    source venv/bin/activate
fi
# Run the bot
python3 cane_corso_bot.py
