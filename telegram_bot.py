import logging
import requests
import time

from environs import Env
from requests.exceptions import ReadTimeout, ConnectionError
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, \
    CallbackQueryHandler


logger = logging.getLogger('telegram_bot')
env = Env()
env.read_env()


def start(update: Update, context: CallbackContext) -> None:
    full_name = update.message.from_user.full_name
    text = (
        f"Привет, {full_name}. "
        f"На Девмане работы учеников проверяют в течение суток. "
        f"Этот бот напишет вам, как только работа будет проверена."
    )
    keyboard = [
        [InlineKeyboardButton("Продолжить", callback_data='continue')]
    ]
    update.message.reply_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


def get_user_reviews(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    context.bot.send_message(
        text='Бот начал отслеживать статусы работ',
        chat_id=update.effective_chat.id
    )
    api_devman_token = env.str('API_DEVMAN_TOKEN')
    url = 'https://dvmn.org/api/long_polling/'
    headers = {'Authorization': api_devman_token}
    while True:
        params = {}
        try:
            response = requests.get(
                url,
                headers=headers,
                timeout=60,
                params=params
            )
            response.raise_for_status()
            user_reviews = response.json()
            if user_reviews['status'] == 'found':
                params['timestamp'] = user_reviews['last_attempt_timestamp']
                lesson_title = user_reviews['new_attempts'][0]['lesson_title']
                lesson_url = user_reviews['new_attempts'][0]['lesson_url']
                if user_reviews['new_attempts'][0]['is_negative'] == True:
                    context.bot.send_message(
                        text=f'Преподаватель проверил работу: {lesson_title} {lesson_url}. '
                             f'К сожалению, в работе нашлись ошибки.',
                        chat_id=update.effective_chat.id
                    )
                else:
                    context.bot.send_message(
                        text=f'Преподаватель проверил работу: {lesson_title} {lesson_url}. '
                             f'Можно приступать к следующему уроку',
                        chat_id=update.effective_chat.id
                    )
            else:
                params['timestamp'] = user_reviews['timestamp_to_request']
        except ReadTimeout as e:
            print(type(e), 'Время ожидания истекло. Повторная попытка.')
        except ConnectionError as e:
            print(type(e), 'Проблемы соединения. Повторная попытка.')
            time.sleep(10)


def handle():
    updater = Updater(token=env.str('TELEGRAM_BOT_TOKEN'), use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(
        CallbackQueryHandler(get_user_reviews, pattern='continue')
    )

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s - %(funcName)s -  %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    logger.setLevel(logging.DEBUG)
    handle()
