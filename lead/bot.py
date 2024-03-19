import json
import requests
from odoo.tools import config


API_TOKEN = config.get('telegram_api_token')


class SendMessageError(Exception):
    pass


def send_message(telegram_id, message):
    url = f'https://api.telegram.org/bot{API_TOKEN}/sendMessage'

    kb = {
        "inline_keyboard": [
            [
                {"text": "Отправить сообщение", "callback_data": "send_message"}
            ]
        ]
    }

    kb_json = json.dumps(kb)

    data = {
        'chat_id': telegram_id,
        'text': message,
        'parse_mode': 'MarkdownV2',
        'reply_markup': kb_json
    }

    try:
        response = requests.post(url, data=data)
        response.raise_for_status()

    except Exception as e:
        raise SendMessageError(e)
