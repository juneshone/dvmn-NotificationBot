# dvmn-NotificationBot

Получение уведомлений о проверенных задачах и отправка сообщений о статусе задачи в Telegram. 

![NotificationBot](https://github.com/juneshone/dvmn-NotificationBot/blob/main/bot_tg.png)

## Как установить

Python должен быть уже установлен. Склонируйте репозиторий и создайте виртуальную среду командой:

```python
python -m venv venv
```

Активируйте виртуальную среду для Windows(в ином случае см. [документацию](https://docs.python.org/3/library/venv.html)):

```python
.\venv\Scripts\activate.bat
```

Затем используйте pip для установки зависимостей:

```python
pip install -r requirements.txt
```

## Переменнные окружения

Часть данных проекта берётся из переменных окружения. Чтобы их определить, создайте файл `.env` и присвойте значения переменным окружения в формате: ПЕРЕМЕННАЯ=значение.

_Переменные окружения проекта:_

`API_DEVMAN_TOKEN` — это персональный токен API DEVMAN. Документация к API DEVMAN находится [здесь](https://dvmn.org/api/docs/).

`TELEGRAM_BOT_TOKEN` — токен доступа к Telegram-боту. Чтобы сгенерировать токен, вам нужно поговорить с `@BotFather` и выполнить несколько простых шагов описанных [здесь](https://core.telegram.org/bots#6-botfather).

`CHAT_ID` — идентификатор Telegram-чата. Чтобы получить свой `chat_id`, напишите в Telegram специальному боту: [@userinfobot](https://telegram.me/userinfobot).
## Как запустить

Убедитесь, что в терминале находитесь в директории кода и запустите бота, используя команду:

```python
python .\telegram_bot.py
```

В результате после проверки задания преподавателем в Telegram чате появляется уведомление о статусе работы.

## Цель проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).