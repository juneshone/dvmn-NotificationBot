import logging
import requests
import time
import telegram

from environs import Env
from requests.exceptions import ReadTimeout, ConnectionError


logger = logging.getLogger('telegram_bot')


class TelegramLogsHandler(logging.Handler):

    def __init__(self, bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.bot = bot

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(chat_id=self.chat_id, text=log_entry)


def get_user_reviews(bot, chat_id, api_devman_token):
    url = 'https://dvmn.org/api/long_polling/'
    headers = {'Authorization': api_devman_token}
    while True:
        params = {}
        try:
            response = requests.get(
                url,
                headers=headers,
                params=params
            )
            response.raise_for_status()
            user_reviews = response.json()
            if user_reviews['status'] == 'found':
                params['timestamp'] = user_reviews['last_attempt_timestamp']
                lesson_title = user_reviews['new_attempts'][0]['lesson_title']
                lesson_url = user_reviews['new_attempts'][0]['lesson_url']
                if user_reviews['new_attempts'][0]['is_negative'] == True:
                    bot.send_message(
                        text=f'Преподаватель проверил работу: {lesson_title} {lesson_url}. '
                             f'К сожалению, в работе нашлись ошибки.',
                        chat_id=chat_id
                    )
                else:
                    bot.send_message(
                        text=f'Преподаватель проверил работу: {lesson_title} {lesson_url}. '
                             f'Можно приступать к следующему уроку',
                        chat_id=chat_id
                    )
            else:
                params['timestamp'] = user_reviews['timestamp_to_request']
        except ReadTimeout as e:
            logger.exception(f'{type(e)}:Время ожидания истекло. Повторная попытка.')
            continue
        except ConnectionError as e:
            logger.exception(f'{type(e)}:Проблемы соединения. Повторная попытка.')
            time.sleep(10)
            continue


def main():
    logging.basicConfig(
        format='%(asctime)s - %(funcName)s -  %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    logger.setLevel(logging.DEBUG)
    env = Env()
    env.read_env()
    api_devman_token = env.str('API_DEVMAN_TOKEN')
    bot = telegram.Bot(token=env.str('TELEGRAM_BOT_TOKEN'))
    chat_id = env.str('CHAT_ID')
    logger.addHandler(TelegramLogsHandler(bot, chat_id))
    logger.info('Бот запущен')
    get_user_reviews(bot, chat_id, api_devman_token)


if __name__ == '__main__':
    main()
