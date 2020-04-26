*** Settings ***
Resource    resource.robot

*** Variables ***
${apikey}    12800a22dc23f13a781e8c707dc63d47
${BROWSER}    googlechrome

*** Keywords ***
Open Browser to check
    Open Browser    ${LOGIN URL}    ${BROWSER}
Run Loop
    [Arguments]    ${size}    ${result}    ${keys}    ${values}
    :FOR    ${i}    IN RANGE    ${size}
    \    ${key}    Get From List    ${keys}    ${i}
    \    ${value}    Get From List    ${values}    ${i}
    \    Set To Dictionary    ${result}    ${key}    ${value}
    Log Dictionary    ${result}
Run Second Loop
    [Arguments]    ${size}    ${result}    ${keys}
    :FOR    ${i}    IN RANGE    ${size}
    \    ${key}    Get From List    ${keys}    ${i}
    \    Set To Dictionary    ${result}    ${key}    Heavy intensity rain
    Log Dictionary    ${result}
        
*** Test cases ***
Get cities and temperature
    [Documentation]    Выбираем города, в которых температура > 25 градусов цельсия. Если есть хотя бы один - выводим его и его температуру в Log в формате City - {city_name}. Temperature - {temperature}, тест пройден. Если таких городов нет, тест не пройден и в Log сообщение об этом.
    [Tags]    city    temperature 
    ${city}    ${temperature}    get city and temp
    ${length}    Get Length    ${city}
    Run Keyword Unless    ${length}==0    Log    City - ${city}. Temperature - ${temperature}!
    Run Keyword If    ${length}==0    Fail    No cities with temperature more than 25.0
Get cities and day length
    [Documentation]    Выбираем города, в которых световой день длится больше 12 часов. Если есть хотя бы один - выводим его и его продолжительность светового дня в Log в формате City - {city_name}. Day length - {day_length}, тест пройден. Если таких городов нет, тест не пройден и в Log сообщение об этом.
    [Tags]    city    day
    ${city}    ${day_length}    get day length
    ${length}    Get Length    ${city}
    Run Keyword Unless    ${length}==0    Log    City - ${city}. Day Length - ${day_length}!
    Run Keyword If    ${length}==0    Fail    No cities with day light more than 12 hours
Get cities and conditions
    [Documentation]    Выбираем города, в которых скорость ветра < 20 м/с и видимость > 300 метров. Если есть хотя бы один - выводим его и сообщение о хороших погодных условиях в Log в формате City - {city_name}. Good conditions, тест пройден. Если таких городов нет, тест не пройден и в Log сообщение об этом.
    [Tags]    city    wind    visibility
    ${city}    get wind and visibility
    ${length}    Get Length    ${city}
    Run Keyword Unless    ${length}==0    Log    City - ${city}. Good conditions!
    Run Keyword If    ${length}==0    Fail    No cities with good condition
Get cities with snow
    [Documentation]    Выбираем города, в которых идет снег на данный момент. Если есть хотя бы один - выводим его и сообщение о том, что там снег в Log в формате  City - {city_name}. Snow!, тест пройден. Если таких городов нет, тест не пройден и в Log сообщение об этом.
    [Tags]    city    snow
    ${city}    get snow
    ${length}    Get Length    ${city}
    Run Keyword Unless    ${length}==0    Log    City - ${city}. Snow!
    Run Keyword If    ${length}==0    Fail    No cities with snow
Get cities and humidity and pressure
    [Documentation]    Выбираем города, в которых влажность больше 75% и давление больше 755 мм рт.ст. Если есть хотя бы один - выводим его, его влажность и давление в Log в формате City - {city_name}. Humidity - {humidity}, pressure - {pressure}, тест пройден. Если таких городов нет, тест не пройден и в Log сообщение об этом.
    [Tags]    city    humidity    pressure
    ${city}    ${hum}    ${pres}    get pressure and humidity
    ${length}    Get Length    ${city}
    Run Keyword Unless    ${length}==0    Log    City - ${city}. Humidity - ${hum}. Pressure - ${pres}!
    Run Keyword If    ${length}==0    Fail    No cities with day light more than 12 hours
Get cities and clouds
    [Documentation]    По каждому городу из списка получить прогноз погоды на ближайшие пять дней.Выбрать те города, в которых хотя бы в один из пяти дней облачность будет больше 90%. Если есть хотя бы один город, то вывести сообщение в лог в формате City - {city_name}. Clouds - {clouds_percent}, date - {clouds_date}. Тест считать пройденным.Если таких дней несколько, то необходимо каждый из них писать в лог с новой строки.Если таких городов нет, то вывести соответствующее сообщение в лог. Тест считать не пройденным.
    [Tags]    city    clouds
    ${cities}    ${clouds}    ${dates}    get clouds
    ${length}    Get Length    ${cities}
    ${result}    Create Dictionary
    ${size}    Get Length    ${clouds}
    Run Keyword Unless    ${length}==0    Log    City - ${cities}
    Run Keyword Unless    ${length}==0    Run Loop    ${size}    ${result}    ${dates}    ${clouds}
    Run Keyword If    ${length}==0    Fail    No cities with clouds more than 90
Get cities and rain
    [Documentation]    По каждому городу из списка получить прогноз погоды на ближайшие пять дней.Выбрать те города, в которых хотя бы в один из пяти дней погода будет отмечена как "Rain", а в описании будет значение"heavy intensity rain".Если есть хотя бы один город, то вывести сообщение в лог в формате City - {city_name}. Heavy intensity rain - {rain_date}. Тест считать пройденным.Если таких дней несколько, то необходимо каждый из них писать в лог с новой строки.Если таких городов нет, то вывести соответствующее сообщение в лог. Тест считать не пройденным. 
    [Tags]    city    rain
    ${cities}    ${dates}    get rain
    ${length}    Get Length    ${cities}
    ${size}    Get Length    ${dates}
    ${result}    Create Dictionary
    Run Keyword Unless    ${length}==0    Log    City - ${cities}
    Run Keyword Unless    ${length}==0    Run Second Loop    ${size}    ${result}    ${dates}
    Run Keyword Unless    ${length}==0    Log Dictionary    ${result}
    Run Keyword If    ${length}==0    Fail    No cities with heavy intensity rain
Get temperature difference
    [Documentation]    По каждому городу из списка получить прогноз погоды на ближайшие пять дней.Выбрать те города, в которых хотя бы в один из пяти дней разница температуры утром и в дневное время будет больше 10 градусов. Если есть хотя бы один город, то вывести сообщение в лог в формате City - {city_name}. Temperature difference - {difference}, date - {difference_day}. Тест считать пройденным. Если таких дней несколько, то необходимо каждый из них писать в лог с новой строки.Если таких городов нет, то вывести соответствующее сообщение в лог. Тест считать не пройденным.
    [Tags]    city    temperature difference
    ${cities}    ${dates}    ${temp_diff}    get temp diff
    ${length}    Get Length    ${cities}
    ${result}    Create Dictionary
    ${size}    Get Length    ${dates}
    Run Keyword Unless    ${length}==0    Log    City - ${cities}
    Run Keyword Unless    ${length}==0    Run Loop    ${size}    ${result}    ${dates}    ${temp_diff}
    Run Keyword If    ${length}==0    Fail    No cities with temperature difference more than 10