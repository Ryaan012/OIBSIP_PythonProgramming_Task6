import customtkinter as ctk
from PIL import Image, ImageTk
import requests
import io

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

API_KEY = "824b43820d140234262377f41dc588a6"

class WeatherApp:
    def __init__(self):
        self.city_input = ctk.StringVar(value="")

    def fetch_weather_data(self, city, ui):
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        final_url = f"{base_url}?q={city}&appid={API_KEY}&units=metric"
        
        try:
            response = requests.get(final_url, timeout=5)
            weather = response.json()

            if weather.get("cod") != 200:
                ui["location"].configure(text="City Not Found 😓")
                return

            country_code = weather["sys"]["country"]
            city_actual = weather["name"]
            ui["location"].configure(text=f"{city_actual}, {country_code}")

            icon_id = weather["weather"][0]["icon"]
            img_url = f"http://openweathermap.org/img/wn/{icon_id}@2x.png"
            icon_bytes = requests.get(img_url).content
            icon_pil = Image.open(io.BytesIO(icon_bytes)).resize((100, 100))
            icon_final = ImageTk.PhotoImage(icon_pil)

            ui["icon"].configure(image=icon_final, text="")
            ui["icon"].image = icon_final

            temperature = int(weather["main"]["temp"])
            condition = weather["weather"][0]["main"]
            humidity = weather["main"]["humidity"]
            wind_speed = int(weather["wind"]["speed"] * 3.6)

            ui["temperature"].configure(text=f"{temperature}°")
            ui["description"].configure(text=condition)
            ui["humidity"].configure(text=f"💧 {humidity}%\nHumidity")
            ui["wind"].configure(text=f"🌬 {wind_speed} km/h\nWind")

        except Exception as e:
            ui["location"].configure(text="Error fetching data")

root = ctk.CTk()
root.title("Weather App")
root.geometry("360x500")
root.resizable(False, False)
root.configure(fg_color="white")

app = WeatherApp()
ui_elements = {}

title = ctk.CTkLabel(root, text="🌀 Weather App", font=("Arial", 20, "bold"), text_color="#2C3E50")
title.pack(pady=(10, 5))

ui_elements["pin"] = ctk.CTkLabel(root, text="📍", font=("Arial", 24), text_color="orange")
ui_elements["pin"].pack(pady=(10, 0))

ui_elements["location"] = ctk.CTkLabel(root, text="", font=("Arial", 18, "bold"), text_color="black")
ui_elements["location"].pack(pady=(0, 10))

ui_elements["icon"] = ctk.CTkLabel(root, text="")
ui_elements["icon"].pack()

ui_elements["temperature"] = ctk.CTkLabel(root, text="", font=("Arial", 36, "bold"), text_color="black")
ui_elements["temperature"].pack()

ui_elements["description"] = ctk.CTkLabel(root, text="", font=("Arial", 16), text_color="gray")
ui_elements["description"].pack(pady=(0, 10))

info_frame = ctk.CTkFrame(root, fg_color="white")
info_frame.pack(pady=5)

ui_elements["humidity"] = ctk.CTkLabel(info_frame, text="", font=("Arial", 14), text_color="black")
ui_elements["humidity"].grid(row=0, column=0, padx=20)

ui_elements["wind"] = ctk.CTkLabel(info_frame, text="", font=("Arial", 14), text_color="black")
ui_elements["wind"].grid(row=0, column=1, padx=20)

search_frame = ctk.CTkFrame(root, fg_color="#9B59B6", corner_radius=20)
search_frame.pack(side="bottom", fill="x", padx=20, pady=15)

city_entry = ctk.CTkEntry(search_frame, textvariable=app.city_input, font=("Arial", 14, "bold"),
                          fg_color="#D8BFD8", text_color="black", corner_radius=10,
                          width=240, justify="center")
city_entry.pack(pady=(20, 10), padx=20)

def on_get_weather():
    user_city = app.city_input.get().strip()
    if user_city:
        app.fetch_weather_data(user_city, ui_elements)
        app.city_input.set("")

fetch_btn = ctk.CTkButton(search_frame, text="Get Weather", command=on_get_weather,
                          fg_color="#EAEAEA", hover_color="#D6D6D6", text_color="#7D3C98",
                          font=("Arial", 14, "bold"), corner_radius=10, width=200)
fetch_btn.pack(pady=(0, 20))

root.mainloop()
