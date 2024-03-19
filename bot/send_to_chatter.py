import xmlrpc.client
import configparser
import logging
import logging.config

from main import CONFIG_PATH


logger = logging.getLogger(__name__)


class SendMessageToChatterError(Exception):
    pass


def get_auth_data(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)

    data = {'host': 'localhost',
            'port': config.get('options', 'http_port'),
            'db_name': config.get('odoo-auth', 'db_name'),
            'login': config.get('odoo-auth', 'login'),
            'password': config.get('odoo-auth', 'password')}

    return data


async def send_to_chatter(lead_id, message):
    auth_data = get_auth_data(CONFIG_PATH)

    url = 'http://' + auth_data['host'] + ':' + auth_data['port']
    db_name = auth_data['db_name']
    login = auth_data['login']
    password = auth_data['password']

    common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
    uid = common.authenticate(db_name, login, password, {})

    models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

    try:
        models.execute_kw(db_name, uid, password, 'mail.message', 'create', [{
            'model': 'crm.lead',
            'res_id': int(lead_id),
            'body': 'Сообщение от работника:\n' + message
        }])

    except Exception as e:
        logger.error(e)
        raise SendMessageToChatterError(e)
