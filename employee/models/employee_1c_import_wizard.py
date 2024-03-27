from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.tools import config
import requests
from datetime import datetime

GET_PERSONAL_DATA_URL = config.get('1c_get_personal_data_url')


class Employee1CImportWizard(models.TransientModel):
    _name = 'employee.1c.import.wizard'
    _description = 'Import Employee from 1C'

    is_employee_number = fields.Boolean(string='By Number', default=True)
    is_employee_name = fields.Boolean(string='By Name', default=False)

    employee_number = fields.Char(string='Number')
    employee_name = fields.Char(string='Name')

    def btn_import_from_1c(self):
        employee_number = self.employee_number
        employee_name = self.employee_name

        employee = self.env['hr.employee'].browse(self._context.get('active_id'))

        if employee:

            url = GET_PERSONAL_DATA_URL + f"?Name={employee_name if employee_name else ''}&ServiceNumber={employee_number if employee_number else ''}&Initiator=&Reason"

            response = requests.get(url, auth=('Admin', ""))

            if response.status_code != 200:
                raise ValidationError(_('Error' + str(response.status_code) + "\n" + response.text))

            try:

                data = response.json()

                if data['ErrorText'].endswith('не найдено'):
                    raise ValidationError(_('No records found'))

                passport = f"{data['PassportSeries']}, {data['PassportNumber']}, {data['PassportIssued']}, {data['PassportDateOfIssue']}, {data['PassportDivisionCode']}"

                employee.name = data['FullName']
                employee.private_phone = data['Phone']
                employee.private_street = data['ResidentialAddress']
                employee.ssnid = data['SNILS']
                employee.passport_id = passport
                employee.citizenship = data['Citizeship']
                employee.INN = data['INN']
                employee.birthday = datetime.strptime(data['DateOfBirth'], '%m.%d.%Y').date()

            except Exception as e:
                raise ValidationError(_(e))

            finally:
                return {'type': 'ir.actions.act_window_close'}


