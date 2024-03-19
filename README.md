# Custom crm.lead & hr.employee

- К модели __crm.lead__ добавлено поле __employee__ (выбор работника из числа сотрудников)
- К модели __hr.employee__ добавлено поле __telegram_id__ (его можно получить в боте, нажав кнопку "Мой telegram ID")
- В модуле __lead__ также реализована отправка сообщения с адресом сотруднику:
    - *при создании лида*
    - *смене работника у лида*
    - *смене адреса лида*

# Telegram bot

Телеграм бот с помощью которого работник может:
- Получить свой telegram ID
- Получить сообщение о новом лиде / смене адреса у лида
- Отправить сообщение в __chatter__ лида

# Конфигурация

Odoo и telegram bot используют общий конигурационный файл  
В части __options__ прописываются настройки __odoo__ и __API TOKEN__ бота  
В части __odoo-auth__ прописываются настройки для авторизации Odoo External Api

### Пример:

[options]  
db_host = localhost  
db_port = 5432  
db_user = odoo  
db_password = odoo  
addons_path = ...
http_port = 8069  
admin_passwd = ...  
telegram_api_token = ... 

[odoo-auth]  
db_name = ...  
login = ...  
password = ...  

# Установка и запуск  

## Odoo

При запуске odoo (файл *odoo-bin*) нужно передать конфигурационный файл с параметром __-c__  
__Пример__:  
`-c C:\Users\...\conf\odoo.conf ...`

  
## Telegram bot
Для работы бота необходимо установить библиотеку __aiogram__  
  
`pip install aiogram==3.4.1`

  
При запуске бота (файл *bot/main.py*) также нужно передать файл конфигурации  
__Пример__:  
`C:\Users\...\conf\odoo.conf ...`
