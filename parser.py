import requests
from bs4 import BeautifulSoup


url = 'https://stavka.tv/predictions'

def get_html(url: str) -> str:
    response = requests.get(url)
    return response.text

def get_predict_data(html: str):
    soup = BeautifulSoup(html, 'html.parser')
    
    match = soup.find('div', class_='PredictionsItem')
    
    command_1 = match.find('span', class_='text-slogan team team--home').text
    command_2 = match.find('span', class_='text-slogan team team--away').text
    
    time = match.find('span', class_='date__time').text
    date = match.find('span', class_='date__day').text
    
    k = match.find('div', class_='Rate--pending Rate--medium Rate--secondary Rate rate').text
    prediction = match.find('span', class_='outcome').text
    
    description = match.find('div', class_='prediction-text text-article').text
    
    return command_1, command_2, time, date, k, prediction, description

html_content = get_html(url)
print(get_predict_data(html_content))