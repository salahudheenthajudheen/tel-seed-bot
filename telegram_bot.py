import os
import requests
import logging
import re
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler

# Enable logging to track issues
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Replace with your API tokens
TELEGRAM_API_TOKEN = 'YOUR_TELEGRAM_API_TOKEN'
OPENWEATHER_API_KEY = 'YOUR_OPENWEATHER_API_KEY'
NASA_API_KEY = 'YOUR_NASA_API_KEY'

# States for conversation handler
LOCATION, DATE, CROP = range(3)

async def start(update: Update, context) -> None:
    """Send a message when the command /start is issued."""
    logger.info("Start command received")
    await update.message.reply_text(
        'Welcome! To provide you with accurate information, please share your location.',
        reply_markup=ReplyKeyboardMarkup(
            [[KeyboardButton("Share Location", request_location=True)]],
            one_time_keyboard=True
        )
    )
    return LOCATION

async def handle_location(update: Update, context) -> int:
    """Handle user location input."""
    user_location = update.message.location
    context.user_data['location'] = user_location
    logger.info(f"Location received: {user_location}")

    # Convert latitude and longitude to a readable format
    latitude = user_location.latitude
    longitude = user_location.longitude

    await update.message.reply_text(f"Location received! Latitude: {latitude}, Longitude: {longitude}. Now, enter the date (YYYY-MM-DD).")
    return DATE

async def handle_date(update: Update, context) -> int:
    """Handle user date input."""
    date = update.message.text
    context.user_data['date'] = date
    logger.info(f"Date received: {date}")

    # Validate date format
    if not re.match(r'\d{4}-\d{2}-\d{2}', date):
        await update.message.reply_text("Please enter the date in the format YYYY-MM-DD.")
        return DATE

    await update.message.reply_text(f"Date '{date}' received. Now, enter the crop name.")
    return CROP

async def handle_crop(update: Update, context) -> int:
    """Handle user crop input and give yield prediction."""
    crop = update.message.text
    location = context.user_data.get('location')
    date = context.user_data.get('date')

    if not location or not date:
        logger.error("Location or date missing from context.")
        await update.message.reply_text("Error: Missing location or date. Please start over by typing /start.")
        return ConversationHandler.END

    logger.info(f"Crop received: {crop}")

    # Get data from APIs
    weather_data = get_weather_data(location.latitude, location.longitude)
    nasa_image_url = get_nasa_data(location.latitude, location.longitude, date)
    water_data_url = get_water_data(location.latitude, location.longitude)  # Fetch water data

    # Extract weather data for better readability
    temperature_celsius = weather_data.get('main', {}).get('temp') - 273.15  # Convert from Kelvin to Celsius
    weather_description = weather_data.get('weather', [{}])[0].get('description', 'No description available.')
    humidity = weather_data.get('main', {}).get('humidity', 'No data')

    # Create a more readable result message
    result = (
        f"🌾 *Crop Yield Prediction* 🌾\n"
        f"*Crop*: {crop}\n"
        f"*Date*: {date}\n"
        f"*Location*: Latitude {location.latitude}, Longitude {location.longitude}\n\n"
        f"---\n"
        f"*Current Weather*:\n"
        f"Temperature: {temperature_celsius:.2f}°C\n"
        f"Condition: {weather_description.capitalize()}\n"
        f"Humidity: {humidity}%\n\n"
        f"---\n"
        f"*NASA Earth Data*:\n"
        f"Here’s an image from NASA related to your location:\n"
        f"[View Image]({nasa_image_url})\n"
        f"Water data can be found here: [Water Data]({water_data_url})\n"  # Add water data link
    )

    # Escape MarkdownV2 reserved characters
    result = escape_markdown(result)

    # Send result back to the user
    await update.message.reply_text(result, parse_mode='MarkdownV2')
    return ConversationHandler.END

def escape_markdown(text):
    """Escape MarkdownV2 reserved characters."""
    escape_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '.', '!', ':']
    for char in escape_chars:
        text = text.replace(char, f'\\{char}')
    return text

def get_weather_data(latitude, longitude):
    """Fetch weather data from OpenWeather API."""
    logger.info(f"Fetching weather data for Latitude: {latitude}, Longitude: {longitude}")
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={OPENWEATHER_API_KEY}"
    response = requests.get(url)

    logger.info(f"Weather API response: {response.status_code} - {response.text}")

    if response.status_code == 200:
        return response.json()
    else:
        logger.error(f"Weather API error: {response.json().get('message', 'No error message provided.')}")
        return {}

def get_nasa_data(latitude, longitude, date):
    """Fetch NASA Earth data."""
    logger.info(f"Fetching NASA data for Latitude: {latitude}, Longitude: {longitude} on {date}")
    url = f"https://api.nasa.gov/planetary/earth/assets?lon={longitude}&lat={latitude}&date={date}&dim=0.1&api_key={NASA_API_KEY}"
    response = requests.get(url)

    logger.info(f"Nasa API response: {response.status_code} - {response.text}")

    try:
        data = response.json()

        if response.status_code == 200:
            if 'count' in data and data['count'] > 0:
                return data['results'][0]['url']  # Modify based on your API response structure
            else:
                logger.error("No data available from NASA API.")
                return "No data available."
        else:
            logger.error(f"Nasa API error: {data.get('msg', 'No error message provided.')}")
            return "Error fetching data from NASA API."
    except Exception as e:
        logger.error(f"Error while processing NASA data: {str(e)}")
        return "An error occurred while processing NASA data."

def get_water_data(latitude, longitude):
    """Fetch water data from NASA's MODIS API."""
    logger.info(f"Fetching water data for Latitude: {latitude}, Longitude: {longitude}")

    # Replace with a real MODIS API endpoint
    url = f"https://api.nasa.gov/planetary/earth/assets?lon={longitude}&lat={latitude}&dim=0.1&api_key={NASA_API_KEY}"
    response = requests.get(url)

    try:
        data = response.json()

        # Check if the API returned a valid response and contains 'count'
        if response.status_code == 200:
            if 'count' in data and data['count'] > 0:
                water_data_url = data['results'][0]['url']  # Modify according to your endpoint's response structure
                return water_data_url
            else:
                logger.error("No water data available from NASA API.")
                return "No water data available."
        else:
            logger.error(f"Nasa API error: {data.get('msg', 'No error message provided.')}")
            return "Error fetching data from NASA API."
    except Exception as e:
        logger.error(f"Error while processing NASA water data: {str(e)}")
        return "An error occurred while processing NASA water data."

async def cancel(update: Update, context) -> int:
    """Cancel the conversation."""
    logger.info("Conversation cancelled")
    await update.message.reply_text('Operation cancelled.')
    return ConversationHandler.END

def main() -> None:
    """Run the bot."""
    application = Application.builder().token(TELEGRAM_API_TOKEN).build()

    # Add conversation handler for the flow: Location -> Date -> Crop
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            LOCATION: [MessageHandler(filters.LOCATION, handle_location)],
            DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_date)],
            CROP: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_crop)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    application.add_handler(conv_handler)

    # Start the bot
    logger.info("Bot started, polling for messages.")
    application.run_polling()

if __name__ == '__main__':
    main()
