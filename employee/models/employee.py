from odoo import api, fields, models


class Employee(models.Model):
    _inherit = 'hr.employee'

    telegram_id = fields.Char(string='Telegram ID')
    citizenship = fields.Char(string='Citizenship')
    INN = fields.Char(string='INN')

