#!/usr/bin/python3
# -*- coding: utf-8 -*-
import requests
from googletrans import Translator
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
import math


def fahrenheit_to_celsius_rounded_up(fahrenheit_str):
    fahrenheit_clean = fahrenheit_str.strip('°')
    fahrenheit = int(fahrenheit_clean)
    celsius = (fahrenheit - 32) * 5 / 9
    celsius_rounded_up = math.ceil(celsius)
    print("Temperature converted succesfully")
    return str(celsius_rounded_up) + "°"


def svg_generate(src_in):
    data = requests.get(src_in).content
    with open("weather_pic.svg", "wb") as f:
        f.write(data)    


def get_src(html_in):
    src_res = ""
    for i in range(len(html_in)):
        if html_in[i] + html_in[i+1] + html_in[i+2] == "src":
            i += 5
            while html_in[i] != '"':
                src_res += html_in[i]
                i += 1
            print("src got successfully")
            return src_res
    print("ERROR: no src found")


def get_weather_pic(url_in):
    response = requests.get(url_in)
    html = BeautifulSoup(response.text, 'html.parser')
    weather_pic = html.find_all('img', class_="simbW")
    pic_html = str(weather_pic[0])
    pic_src = get_src(pic_html)
    svg_generate(pic_src)
    pic_html = '<img alt="Clear" class="simbW" height="48" src="'+'weather_pic.png'+'"/>'
    print("Weather pic got succesfully")
    return pic_html


def get_weather(url_in):
    weather = []
    response = requests.get(url_in)
    html = BeautifulSoup(response.text, 'html.parser')
    temp_html = html.find_all('span', class_="dato-temperatura changeUnitT")
    name_html = html.find_all('img', class_="simbW")
    print("Weather info scrapped succesfully")

    name = name_html[0].attrs['alt']
    temp = fahrenheit_to_celsius_rounded_up(temp_html[0].text)
    weather.append([name, temp])

    translator = Translator()
    res = translator.translate('Weather: '+name, 'ru')
    name = res.text
    name = name[8:]
    name = name.capitalize()
    print("Weather translated succesfully")
    
    tz_madrid = pytz.timezone('Europe/Madrid')
    current_time = datetime.now(tz_madrid)
    with open("weather_info.html", "w", encoding="utf-8") as fp:
        fp.write(name + ', ' + temp)
    with open("pylog.log", "w", encoding="utf-8") as lg:
        lg.write("weather file was last updated at" + " " + current_time.strftime("%H:%M:%S"))
    print("Weather info file updated succesfully")
    
    weather_pic_html = get_weather_pic(url_in)
    with open("weather_pic.html", "w", encoding="utf-8") as fp:
        fp.write(str(weather_pic_html))
    print("Weather image file updated succesfully")


if __name__ == '__main__':
    url = "https://www.theweather.com/malaga-in-spain-c4279.htm"
    get_weather(url)
