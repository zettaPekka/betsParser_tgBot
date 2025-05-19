from mistralai import Mistral
from dotenv import load_dotenv

import os


load_dotenv()


api_key = os.environ['MISTRAL_API_KEY']
model = 'mistral-large-latest'
client = Mistral(api_key=api_key)


async def get_parsed_predict(predict_data: tuple):
    prompt = f'Привет, есть прогноз на матч {predict_data[0]} против {predict_data[1]}. Тебе необходимо немного перефразировать прогноз, например, заменив некоторые слова на синонимы, где это хорошо читается. Сам прогноз: {predict_data[6]}\nОтправь только готовый текст!'

    print(predict_data[6])
    try:
        chat_response = await client.chat.complete_async(
            model = model,
            messages = [
                {
                    'role': 'user',
                    'content': prompt,
                },
            ]
        )

        return chat_response.choices[0].message.content
    except:
        try:
            chat_response = await client.chat.complete_async(
                model = model,
                messages = [
                    {
                        'role': 'user',
                        'content': prompt,
                    },
                ]
            )

            return chat_response.choices[0].message.content
        except:
            return False