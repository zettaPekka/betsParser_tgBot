import aiohttp
from bs4 import BeautifulSoup

from secrets import randbelow


async def get_predict_data(predict_filter: dict):
    url = 'https://stavka.tv/predictions'
    
    if predict_filter['sport'] != 'Не указано':
        url += f'/{predict_filter["sport"]}'
    if predict_filter['k'] != '1-10':
        url += f'?rateFrom={predict_filter["k"][0]}&rateTo={predict_filter["k"][1]}'
    if predict_filter['date'] != 'Не указано':
        url += f'?period={predict_filter["date"]}' if '?' not in url else f'&period={predict_filter["date"]}'
    url += '?predictorTypes=author&predictorTypes=expert' if '?' not in url else f'&predictorTypes=author&predictorTypes=expert'

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as res:
                soup = BeautifulSoup(await res.text(), 'html.parser')

                matches = soup.find_all('div', class_='PredictionsItem')
                match_index = randbelow(len(matches))
                match = matches[match_index]
                
                command_1 = match.find('span', class_='text-slogan team team--home').text
                command_2 = match.find('span', class_='text-slogan team team--away').text
                
                time = match.find('span', class_='date__time').text
                date = match.find('span', class_='date__day').text
                
                k = match.find('div', class_='Rate--pending Rate--medium Rate--secondary Rate rate').text
                prediction = match.find('span', class_='outcome').text
                
                description = match.find('div', class_='prediction-text text-article').text
                
                return command_1, command_2, time, date, k, prediction, description
    except:
        return False
