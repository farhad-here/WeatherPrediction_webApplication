# import requests 
# import pandas as pd
# import matplotlib.pyplot as plt

# req =requests.get('https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&hourly=rain')
# data = req.json()
# rain = data['hourly']['rain']
# time_data = data['hourly']['time']
# month_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
# month_w = []
# day_w = []
# time_w = []
# year_w = []
# for i in time_data:
#        year,month,day =  i.split('-')
#        d,t = day.split('T')
#        year_w.append(year)
#        day_w.append(d)
#        time_w.append(t)
#        month_w.append(month_list[int(month)-1])
# df = pd.DataFrame({'Year':year_w,'Month':month_w,'Day':day_w,"Time":time_w,'Rainy':rain})
# df['YMDT']= df['Year']+' '+df['Month']+' '+df['Day']+' '+df['Time']
# # print(df.loc[df.Rainy == df.Rainy.max(),['Year','Month','Time','Rainy']])
# import numpy as np
# print(
#                 np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
# )
import requests
import pandas as pd
from bs4 import BeautifulSoup

# 📌 تنظیمات: انتخاب شهر (مثلاً تهران)
city = "tehran"
url = f"https://www.timeanddate.com/weather/iran/{city}/historic"

# 📥 دریافت صفحه HTML
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# 📊 استخراج داده‌های دما و وضعیت آب و هوا
data = []
table = soup.find("table", class_="zebra tb-wt fw va-m")
if table:
    rows = table.find_all("tr")[1:]  # حذف هدر جدول
    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 2:
            time = cols[0].text.strip()
            temperature = cols[1].text.strip()
            condition = cols[2].text.strip() if len(cols) > 2 else "-"
            data.append([time, temperature, condition])

# 📊 تبدیل داده‌ها به Pandas DataFrame
df = pd.DataFrame(data, columns=["Time", "Temperature", "Condition"])
print(df.head())  # نمایش ۵ سطر اول

# ذخیره در فایل CSV
df.to_csv("weather_data.csv", index=False)
print("✅ داده‌های آب و هوا ذخیره شدند!")
