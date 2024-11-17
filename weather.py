import tkinter as tk
from tkinter import messagebox
import requests

class WeatherApp:
    def __init__(self, master):
        self.master = master
        self.master.title("天气预报")
        self.master.geometry("500x700")
        self.master.configure(bg='#f0f8ff')

        # 标题标签
        self.title_label = tk.Label(master, text="请输入城市名称以获取天气预报", font=("Helvetica", 14), bg='#f0f8ff', pady=10)
        self.title_label.pack()

        # 城市输入框
        self.city_label = tk.Label(master, text="城市:", font=("Helvetica", 12), bg='#f0f8ff')
        self.city_label.pack(pady=5)
        
        self.city_entry = tk.Entry(master, font=("Helvetica", 12), width=30)
        self.city_entry.pack(pady=5)

        # 获取天气按钮
        self.get_weather_button = tk.Button(master, text="获取天气", command=self.get_weather, 
                                            font=("Helvetica", 12), bg='#32CD32', fg='#FFFFFF', padx=10, pady=5)
        self.get_weather_button.pack(pady=10)

        # 显示天气信息的标签
        self.weather_info_label = tk.Label(master, text="", font=("Helvetica", 12), bg='#f0f8ff', fg='#333333', pady=10)
        self.weather_info_label.pack()

        # 设置输入框启动时自动获取焦点
        self.city_entry.focus_force()  # 或使用 focus_set()

        # 绑定回车键到城市输入框，按回车自动查询天气
        self.city_entry.bind("<Return>", self.on_enter)

    def on_enter(self, event):
        # 按下回车键时调用 get_weather 函数
        self.get_weather()

    def get_weather(self):
        city = self.city_entry.get()
        if not city:
            messagebox.showwarning("输入错误", "请输入城市名称")
            return

        weather_data = self.fetch_weather_from_api(city)
        
        if weather_data:
            self.weather_info_label.config(text=f"城市: {weather_data["city"]}\n"
                                                f"当前温度: {weather_data["temperature"]}°C\n"
                                                f"天气: {weather_data["description"]}\n"
                                                f"湿度: {weather_data["humidity"]}\n"
                                                f"空气质量指数：{weather_data["air"]}\n\n"
                                                f"明天：{weather_data["tomorrow"] + "    "+ \
                                                      weather_data["tomorrow_low"] +"~"+ \
                                                        weather_data["tomorrow_high"]}\n"

                                                f"后天：{weather_data["day_after_tomorrow"] +"    "+ \
                                                      weather_data["day_after_tomorrow_low"] +"~"+ \
                                                        weather_data["day_after_tomorrow_high"]}\n\n"
                                                f"最后更新时间：{weather_data["last_update"]}")
        else:
            self.weather_info_label.config(text="您输入的不是城市\n或\n您输入的不是中国的城市\n请重新输入")

    def fetch_weather_from_api(self, city):
        today_url = f"https://api.lolimi.cn/API/weather/?city={city}"
        future_url= f"https://api.tangdouz.com/tq.php?dz={city}&return=json"
        response = requests.get(today_url)
        response_future = requests.get(future_url)
        
        if response.status_code == 200:
            today = response.json()
            
            if today["code"] == 1:
                future = response_future.json()
                weather_data = {
                     "city": today["data"]["city"],
                     "temperature": today["data"]["current"]["temp"],
                     "description": today["data"]["current"]["weather"],
                     "humidity": today["data"]["current"]["humidity"],
                     "air": today["data"]["current"]["air"],
                     "last_update": today["data"]["current"]["time"],

                     "tomorrow": future["2"]["weather"],
                     "tomorrow_high": future["2"]["high"],
                     "tomorrow_low": future["2"]["low"],

                     "day_after_tomorrow": future["3"]["weather"],
                     "day_after_tomorrow_high": future["3"]["high"],
                     "day_after_tomorrow_low": future["3"]["low"]
                }
                return weather_data
            else:
                return None
        else:
            return None

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
