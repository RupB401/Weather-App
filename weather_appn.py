from tkinter import *
from tkinter import messagebox
import requests
from datetime import datetime
import json  

# API Key
user_api = ''

# GUI Setup
app = Tk()
app.title("Weather App")
app.geometry("520x700")
app.configure(bg='#D6EAF8') 

city_text = StringVar()
Entry(app, textvariable=city_text, font=('Arial', 14), width=30).pack(pady=10)
Button(app, text="Search Weather", font=('Arial', 12), command=lambda: search()).pack()

location_lbl = Label(app, font=('bold', 16), bg='#D6EAF8')
location_lbl.pack()

temp_lbl = Label(app, font=('Arial', 12), bg='#D6EAF8')
temp_lbl.pack()

weather_lbl = Label(app, font=('Arial', 12), bg='#D6EAF8')
weather_lbl.pack()

humidity_lbl = Label(app, font=('Arial', 12), bg='#D6EAF8')
humidity_lbl.pack()

wind_lbl = Label(app, font=('Arial', 12), bg='#D6EAF8')
wind_lbl.pack()

datetime_lbl = Label(app, font=('Arial', 10), bg='#D6EAF8')
datetime_lbl.pack()

Label(app, text="2-Day Forecast", font=('bold', 14), bg='#D6EAF8').pack(pady=10)

# Scrollable Frame
forecast_frame = Frame(app, bg='#D6EAF8')
forecast_frame.pack(padx=10, pady=5, fill='both', expand=True)

canvas = Canvas(forecast_frame, bg='#AED6F1', highlightthickness=0)
scrollbar = Scrollbar(forecast_frame, orient="vertical", command=canvas.yview)
forecast_inner_frame = Frame(canvas, bg='#AED6F1')

forecast_inner_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=forecast_inner_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")


def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

def get_forecast(location):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={location}&appid={user_api}"
    response = requests.get(url)
    data = response.json()
    if data['cod'] != '200':
        return None
    return data

def display_forecast(forecast_data):
    for widget in forecast_inner_frame.winfo_children():
        widget.destroy()

    forecast_list = forecast_data['list'][:16]  # 2 days * 4 entries/day

    for entry in forecast_list:
        time = entry['dt_txt']
        temp = kelvin_to_celsius(entry['main']['temp'])
        weather_main = entry['weather'][0]['main']
        weather_desc = entry['weather'][0]['description']
        text = f"{time}\n{temp:.1f}°C, {weather_main} ({weather_desc})\n"

        Label(forecast_inner_frame, text=text, font=('Arial', 10), bg='#AED6F1', anchor='w', justify=LEFT).pack(anchor='w', padx=10, pady=5)

def get_current_weather(location):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={user_api}"
    response = requests.get(url)
    data = response.json()
    if data['cod'] != 200:
        return None
    return data

def search():
    city = city_text.get()
    current = get_current_weather(city)
    forecast = get_forecast(city)

    if current and forecast:
        temp_c = kelvin_to_celsius(current['main']['temp'])
        temp_f = temp_c * 9/5 + 32
        location_lbl['text'] = f"{current['name']}, {current['sys']['country']}"
        temp_lbl['text'] = f"Temperature: {temp_c:.2f}°C / {temp_f:.2f}°F"
        weather_lbl['text'] = f"Weather: {current['weather'][0]['main']} ({current['weather'][0]['description']})"
        humidity_lbl['text'] = f"Humidity: {current['main']['humidity']}%"
        wind_lbl['text'] = f"Wind Speed: {current['wind']['speed']} m/s"
        datetime_lbl['text'] = f"Updated: {datetime.now().strftime('%d %b %Y | %I:%M:%S %p')}"
        display_forecast(forecast)

        # Pretty-print the output in JSON format
        output = {
            "current_weather": current,
            "forecast": forecast
        }
        print(json.dumps(output, indent=4)) 

    else:
        messagebox.showerror("Error", f"City '{city}' not found.")


app.mainloop()
