from pyowm import OWM
import json
import codecs
import time
import requests


api_key = '12800a22dc23f13a781e8c707dc63d47' # Мой api-key 
owm = OWM(api_key) 

def get_cities_id():
    with open("city.list.json", encoding='utf-8') as json_file: # из json-го файла достаем первые 200-ти горов
        cities = json.load(json_file)[:200]
    ids = []
    for city in cities:
        ids.append(city["id"]) # записываем id первых 200-ти городов в список ids
    return ids

def get_city_and_temp():
    ids = get_cities_id() # достаем id-шки городов
    temperature = 25.0 # температура для сравнения
    cities = [] # список для сохранения городов
    temperatures = [] # список для сохранения городов
    for id in ids:
        obs = owm.weather_at_id(id) # создаем объект с наблюдениями
        temp = obs.get_weather().get_temperature(unit='celsius')['temp'] # достаем температуру в цельсиях
        if temp > temperature:
            location = obs.get_location() 
            name = location.get_name() # достаем название города
            cities.append(name) # добавляем город в список
            temperatures.append(temp) # добавляем температуру в список
            break
    if cities:
        return cities[0], temperatures[0]
    else:
        return cities, temperatures

def time_in_int(time): # функция для перевода времени из даты в int
    hours = int(time[11:13])
    minutes = int(time[14:16])
    seconds = int(time[17:19])
    real_time = hours * 3600 + minutes * 60 + seconds
    return real_time
    
def get_day_length():
    ids = get_cities_id() # достаем id-шки городов
    day_length = 43200 # 12 часов в секундах
    cit = []
    day_length = []
    for id in ids:
        obs = owm.weather_at_id(id)
        sunrise = obs.get_weather().get_sunrise_time('iso') # достаем время восхода
        sunset = obs.get_weather().get_sunset_time('iso') # достаем время заката
        sunrise_to_count = time_in_int(sunrise) # переводим время в int
        sunset_to_count = time_in_int(sunset) 
        day = sunset_to_count - sunrise_to_count # считаем разницу
        if day > 43200:
            location = obs.get_location()
            name = location.get_name()
            cit.append(name) # достали название города и записали в список
            h = int((day/3600) % 24)
            m = int((day/60) % 60)
            s = int(day % 60)
            day = str('{:02}:{:02}:{:02}'.format(h, m, s)) # перевели int-дату обратно в формат hh:mm:ss
            day_length.append(day) # добавили время в список
            break
    if cit:
        return cit[0], day_length[0]
    else:
        return cit, day_length

def get_wind_and_visibility():
    ids = get_cities_id() # достаем id-шки городов
    wind = 20 # скорость ветра для сравнения
    visibility = 300 # видимость в метрах
    cities = []
    for id in ids:
        obs = owm.weather_at_id(id)
        w = obs.get_weather().get_wind()['speed'] # достаем скорость ветра
        vis = obs.get_weather().get_visibility_distance() # достаем видимость в метрах
        if (w < wind) and (vis > visibility): 
            location = obs.get_location()
            name = location.get_name()
            cities.append(name)
            break
    if cities:
        return cities[0]
    else:
        return cities

def get_snow():
    ids = get_cities_id() # достаем id-шки городов
    cities = []
    for id in ids:
        obs = owm.weather_at_id(id)
        if (obs.get_weather().get_snow()): # идет ли снег?
            location = obs.get_location()
            name = location.get_name()
            cities.append(name)
            break
    if not cities:
        return cities
    else:
        return cities[0]

def get_pressure_and_humidity(): 
    ids = get_cities_id() # достаем id-шки городов
    cities = []
    hums = []
    press = []
    humidity = 75 # Влажность для сравнения
    pressure = 770 # Давление для сравнения
    for id in ids:
        obs = owm.weather_at_id(id)
        hum = obs.get_weather().get_humidity() # достаем влажность 
        pres = obs.get_weather().get_pressure()['press'] # достаем давление
        if (hum > humidity) and (pres > pressure):
            location = obs.get_location()
            name = location.get_name()
            cities.append(name)
            hums.append(hum)
            press.append(pres)
            break
    if cities:
        return cities[0], hums[0], press[0]
    if not cities:
        return cities, hums, press

def get_clouds():
    ids = get_cities_id()
    cities = []
    clouds = []
    dates = []
    cloud_to_check = 90
    flag = False
    for id in ids:
        if flag:
            break
        obs = owm.weather_at_id(id)
        fc = owm.three_hours_forecast_at_id(id) # достаем трехчасовой прогноз погоды
        f = fc.get_forecast()
        w = f.get_weathers() # достаем погоду
        for weather in w:
            cloud = weather.get_clouds() # достаем облака
            if cloud > cloud_to_check:
                location = obs.get_location()
                name = location.get_name()
                clouds.append(cloud)
                date = weather.get_reference_time('iso')
                date_without_time = date[0:10] # достаем дату
                dates.append(date_without_time)
                cities.append(name)
                flag = True # флаг для того, чтобы закончить цикл, если нашли хотя бы один город
    if cities:
        return cities[0], clouds, dates
    else:
        return cities, clouds, dates

def get_rain():
    ids = get_cities_id()
    cities = []
    status = []
    status_to_check = 'Rain' # Статус для сравнения
    descr = 'heavy intensity rain' # Описание для сравнения
    dates = []
    flag = False
    for id in ids:
        if flag:
            break
        res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                           params={'id': id, 'units': 'metric', 'APPID': '12800a22dc23f13a781e8c707dc63d47'}) # делаем запрос на погоду
        data = res.json() # записываем в data ответ на запрос
        for i in data['list']:
            status = i['weather'][0]['main'] # достаем статус из даты
            detailed_status = i['weather'][0]['description'] # достаем описание
            if (status == status_to_check) and (detailed_status == descr):
                obs = owm.weather_at_id(id)
                name = obs.get_location().get_name() # достаем название города
                cities.append(name)
                date = i['dt_txt']
                date_without_time = date[0:10] # достаем дату
                dates.append(date_without_time)
                flag = True # флаг для того, чтобы закончить цикл, если нашли хотя бы один город
    if cities:
        return cities[0], dates
    else:
        return cities, dates

def get_temp_diff():
    ids = get_cities_id()
    cities = []
    dates = []
    temp_to_check = 10 # температура для сравнения
    flag = False # флаг для прекращения цикла при условии нахождения хотя бы одного города
    morning = False # флаг, что утро найдено
    day = True # флаг, что день найден
    time_morning = 21600 # 6 утра в секундах
    time_middle = 43200 # 15 дня в секундах
    time_day = 64800 # 18 вечера в секундах
    temp_diff = []
    for id in ids:
        if flag:
            break
        res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                            params={'id': id, 'units': 'metric', 'APPID': '12800a22dc23f13a781e8c707dc63d47'}) # отправляем запрос
        data = res.json()
        timezone = data['city']['timezone'] # достаем таймзону
        for i in data['list']:
            date = i['dt_txt']
            date_with_time = date[11:19] # достаем время
            real_date = time_in_int(date)
            real_date = real_date + timezone # прибавляем к времени таймзону
            if (real_date >= time_morning) and (real_date < time_middle): # если время подходит под утреннее
                morning = True
                day = False
                temp_morning = i['main']['temp'] # достаем температуру утром
                h = int((real_date / 3600) % 24)
                m = int((real_date / 60) % 60)
                s = int(real_date % 60)
                real_date_to_print_morning = str('{:02}:{:02}:{:02}'.format(h, m, s)) # время для вывода
                #print('Morning', real_date_to_print_morning)
                #print(temp_morning)
            if (real_date >= time_middle) and (real_date <= time_day): # если время подоходи под дневное
                if day==False:
                    day=True
                    temp_day = i['main']['temp'] # достаем температуру
                    diff = temp_day - temp_morning
                    h = int((real_date / 3600) % 24)
                    m = int((real_date / 60) % 60)
                    s = int(real_date % 60)
                    real_date_to_print_day = str('{:02}:{:02}:{:02}'.format(h, m, s))
                    #print('Day', real_date_to_print_day)
                    #print(temp_day)
                    if diff > temp_to_check: # если разница > 10
                        print(diff)
                        obs = owm.weather_at_id(id)
                        name = obs.get_location().get_name()
                        dates.append(date[10:18])
                        cities.append(name)
                        temp_diff.append(int(diff))
                        #print(name)
                        flag = True # флаг для того, чтобы закончить цикл, если нашли хотя бы один город
    if cities:
        return cities[0], dates, temp_diff
    else:
        return cities, dates, temp_diff