import requests
from bs4 import BeautifulSoup


url = 'https://stavka.tv/predictions'

def get_predict_data(predict_filter: dict):
    if predict_filter['sport'] != 'Не указано':
        url += f'/{predict_filter["sport"]}'
    if predict_filter['k'] != 'Не указано':
        url += f'?rateFrom={predict_filter["k"][0]}&rateTo={predict_filter["k"][1]}'
    if predict_filter['date'] != 'Не указано':
        url += f'?period={predict_filter["date"]}' if '?' not in url else f'&period={predict_filter["date"]}'
    
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    
    match = soup.find('div', class_='PredictionsItem')
    
    command_1 = match.find('span', class_='text-slogan team team--home').text
    command_2 = match.find('span', class_='text-slogan team team--away').text
    
    time = match.find('span', class_='date__time').text
    date = match.find('span', class_='date__day').text
    
    k = match.find('div', class_='Rate--pending Rate--medium Rate--secondary Rate rate').text
    prediction = match.find('span', class_='outcome').text
    
    description = match.find('div', class_='prediction-text text-article').text
    
    return command_1, command_2, time, date, k, prediction, description
