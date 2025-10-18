import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt


class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter city name: ", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.tempreture_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")

        vbox = QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.tempreture_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)
        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.tempreture_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.tempreture_label.setObjectName("tempreture_label")
        self.emoji_label.setObjectName("emoji_label")
        self.get_weather_button.setObjectName("get_weather_button")
        self.description_label.setObjectName("description_label")

        self.setStyleSheet("""
            QLabel, QPushButton {
                font-family: Calibri;
            }
            QLabel#city_label {
                font-size: 40px;
                font-style: italic;
            }
            QLineEdit#city_input {
                font-size: 40px;
            }
            QPushButton#get_weather_button {
                font-size: 20px;
                background-color: lightblue;
                border: 2px solid gray;
                padding: 6px;
                border-radius: 5px;
                font-weight: bold;
            }
            QLabel#tempreture_label {
                font-size: 75px;
                font-weight: bold;
            }
            QLabel#emoji_label {
                font-size: 100px;
                font-family: Segoe UI emoji;
            }
            QLabel#description_label {
                font-size: 50px;
            }
        """)

        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        api_key = "2e688d29a780c99851009b9b843aa09c"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if data["cod"] == 200:
                self.display_weather(data)
        except requests.exceptions.HTTPError:
            if 'response' in locals():
                match response.status_code:
                    case 400:
                        self.display_error("❌ Bad Request\nThe server could not understand your request. Please check your city name or parameters.")
                    case 401:
                        self.display_error("🔒 Unauthorized\nInvalid or missing API key. Please verify your API key.")
                    case 403:
                        self.display_error("⛔ Forbidden\nYou do not have permission to access this resource.")
                    case 404:
                        self.display_error("🌍 City Not Found\nThe requested city could not be found. Please check the spelling.")
                    case 429:
                        self.display_error("⚠️ Too Many Requests\nYou have exceeded the request limit. Please wait before trying again.")
                    case 500:
                        self.display_error("💥 Internal Server Error\nSomething went wrong on the server side. Please try again later.")
                    case 502:
                        self.display_error("🔁 Bad Gateway\nThe server received an invalid response from the upstream server.")
                    case 503:
                        self.display_error("🛠 Service Unavailable\nThe server is currently overloaded or down for maintenance.")
                    case 504:
                        self.display_error("⏳ Gateway Timeout\nThe server took too long to respond. Please try again later.")
                    case _:
                        self.display_error(f"⚠️ Unexpected Error\nHTTP Status: {response.status_code}")
            else:
                self.display_error("❌ HTTP error occurred, but no response was received.")
        except requests.exceptions.RequestException:
            self.display_error("❌ Network Error - Please check your internet connection.")

    def display_error(self, message):
        self.tempreture_label.setStyleSheet("font-size:30px;")
        self.tempreture_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()

    def display_weather(self, data):
        self.tempreture_label.setStyleSheet("font-size:80px;")
        tempreture_k = data["main"]["temp"]
        tempreture_c = tempreture_k - 273.15
        tempreture_f = (tempreture_k * 9/5) - 459.67
        weather_id = data["weather"][0]["id"]
        weather_description = data["weather"][0]["description"]

        
        self.tempreture_label.setText(f"{tempreture_c:.0f}°C")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(weather_description)
    
    @staticmethod
    def get_weather_emoji(weather_id):
        
        if  200 <= weather_id <= 232:
            return "⛈️"
        elif 300 <= weather_id <= 321:
            return "⛅"
        elif 500 <= weather_id <= 531:
            return "🌧️"
        elif 600 <= weather_id <= 622:
            return "❄️"
        elif 701 <= weather_id <= 741:
            return "😶‍🌫️"
        elif  weather_id == 762:
            return "🌋"
        elif  weather_id == 771:
            return "💨"
        elif  weather_id == 781:
            return "🌪️"
        elif  weather_id == 800:
            return "☀️"
        elif 801 <= weather_id <= 804:
            return "☁️"  
        else:
            return ""  


if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec())
