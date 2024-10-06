# Telegram Crop Yield Prediction Bot

This is a Telegram bot that predicts crop yield based on user-provided location, date, and crop type. The bot fetches data from the **OpenWeather API**, **NASA Earth Data**, and a **Water Monitoring API** to give a comprehensive weather and water data report for better agricultural insights.

## Features

- **Location-based data**: The bot allows users to share their location, and it provides real-time weather data and crop yield predictions.
- **NASA Earth Data**: Retrieves relevant satellite images and data from NASA based on the user's location and date.
- **Water Data**: Fetches water-related data from NASA MODIS for the given location.
- **Weather Data**: Provides current temperature, humidity, and weather conditions using the OpenWeather API.

## APIs Used

1. **OpenWeather API**: Provides weather data such as temperature, humidity, and weather conditions based on the user's location.
2. **NASA Earth Data API**: Fetches satellite imagery and related data from NASA for the user's location and date.
3. **Water Monitoring API** (MODIS): Retrieves water-related data for the given location.

## Bot Commands

- `/start`: Initiates the bot and asks for the user's location.
- `/cancel`: Cancels the current operation and resets the conversation.

## Installation

### Prerequisites

- Python 3.8+
- A Telegram bot API token
- API keys for OpenWeather and NASA Earth Data
- Git and GitHub CLI installed

### Steps to Set Up Locally

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Set up environment variables for your API keys:

    ```bash
    export TELEGRAM_API_TOKEN='your-telegram-token'
    export OPENWEATHER_API_KEY='your-openweather-key'
    export NASA_API_KEY='your-nasa-key'
    ```

4. Run the bot:

    ```bash
    python bot.py
    ```

## Usage

Once the bot is running, users can interact with it through the following steps:

1. **Share location**: The bot will ask for the user's location using Telegram's location sharing feature.
2. **Enter date**: After receiving the location, the bot will prompt the user to enter a date in the format `YYYY-MM-DD`.
3. **Enter crop type**: The user will then be asked to enter the name of the crop they want predictions for.
4. **Receive data**: The bot will fetch weather data, NASA imagery, and water data, then provide a prediction for the crop yield.

## Contributing

Feel free to fork this repository, create a branch, and submit a pull request. For significant changes, please open an issue first to discuss what you would like to modify.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Acknowledgments

- The project makes use of the [OpenWeather API](https://openweathermap.org/api) and [NASA Earth Data](https://api.nasa.gov/).
