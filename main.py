import requests
import sqlite3
from datetime import datetime
from bs4 import BeautifulSoup


def get_weather():
    url = "https://www.bbc.com/weather/3060972"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        temperature_element = soup.find('span', class_='temperature')
        temperature = temperature_element.text.strip()
        return temperature
    else:
        print(f"Failed to retrieve weather data. Status code: {response.status_code}")
        return None

def save_to_database(date_time, temperature):
    connection = sqlite3.connect("hamburg_weather.db")
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS weather_data
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       date_time TEXT,
                       temperature REAL)''')
    cursor.execute("INSERT INTO weather_data (date_time, temperature) VALUES (?, ?)", (date_time, temperature))
    connection.commit()
    connection.close()

if __name__ == "__main__":
    current_temperature = get_weather()

    if current_temperature is not None:
        current_date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_to_database(current_date_time, current_temperature)
        print(f"Weather data saved to the database. Temperature: {current_temperature}°C at {current_date_time}")