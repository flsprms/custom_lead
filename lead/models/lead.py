from odoo import fields, models
from ..bot import send_message, SendMessageError

import logging
import logging.config


logger = logging.getLogger(__name__)


# Создание сообщения из частей адреса, которое будет отправлено работнику
def create_lead_message(start, data):
    lead_name = data.name
    city = data.city
    state = data.state_id.name
    country = data.country_id.name
    street = data.street
    street2 = data.street2
    zip = data.zip

    message_parts = []

    if country:
        message_parts.append(country)
    if state:
        message_parts.append(state)
    if city:
        message_parts.append(city)
    if street:
        message_parts.append(street)
    if street2:
        message_parts.append(street2)
    if zip:
        message_parts.append(zip)

    # {id лида}
    # {Новый лид/изменен адрес лида } {lead_name}
    # Адрес: {country}, {state}, {city}, {street}, {street2}, {zip}

    return f'\#{data.id}\n{start} \"__{lead_name}__\"\nАдрес: ' + ", ".join(message_parts)


class Lead(models.Model):
    _inherit = 'crm.lead'

    employee_id = fields.Many2one('hr.employee', string='Employee')

    def create(self, values):
        result = super(Lead, self).create(values)

        if result.employee_id.telegram_id:
            try:
                message = create_lead_message('Новый лид', result)
                send_message(result.employee_id.telegram_id, message)

            except SendMessageError as e:
                logger.error(e)

        return result

    def write(self, values):
        result = super(Lead, self).write(values)

        # проверка на изменение частей адреса
        address_fields = ['name', 'city_id', 'state_id', 'country_id', 'street', 'street2', 'zip']
        address_changed = any(field in values for field in address_fields)

        if self.employee_id.telegram_id:
            try:
                # поменялся работник
                if 'employee_id' in values:
                    message = create_lead_message('Новый лид', self)
                    send_message(self.employee_id.telegram_id, message)

                # поменялся адрес
                elif address_changed:
                    message = create_lead_message('Изменения в адресе лида', self)
                    send_message(self.employee_id.telegram_id, message)

            except SendMessageError as e:
                logger.error(e)

        return result
