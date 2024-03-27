# Расширение модели hr.employee (интеграция с 1с) __(27.03.2024)__

## Odoo

- В окне создания и изменения сотрудников появилась кнопка __"Import from 1c"__
  ![image](https://github.com/flsprms/custom_lead/assets/149524130/ebd3faa9-b883-4e72-ad7d-a5113933fa85)

- Кнопка открывает окно, с помощью которого можно импортировать данные о сотруднике из 1с по табельному номеру или ФИО
  ![image](https://github.com/flsprms/custom_lead/assets/149524130/db859490-a094-48f4-bb1d-8da082ebd0e7)

- Если сотрудник найден в ИБ 1с, будут заполнены поля: ФИО, дата рождения, паспортные данные, СНИЛС, ИНН, адрес проживания, контактный телефон, гражданство.
  ![image](https://github.com/flsprms/custom_lead/assets/149524130/ac651bbe-9f84-4509-868d-38c0ea16eca7)
  ![image](https://github.com/flsprms/custom_lead/assets/149524130/58387dbe-5702-40fa-af8f-de47f84e7341)

## Установка и запуск

- В Odoo установить модуль employee (/employee) в папку с модулями, обновить список приложений, активировать модуль custom_employee в списке приложений Odoo.
  В настройках групп пользователей определить необходимого пользователя (кто будет иметь доступ к импорту из 1с) в группу *User 1C Employee Import*
  ![image](https://github.com/flsprms/custom_lead/assets/149524130/3d6c437a-3fcc-4106-b3ab-79088b7d0d0b)

- В 1С:Предприятие:
    - Установить расширение (__1c/СервисДляПолученияДанныхСотрудников.cfe__):  
      Администрирование -> Печатные формы, отчеты и обработки -> Расширения -> Добавить из файла
    - Установить обработку для открытия папок интерфейсу Odata (__1c/СервисДляПолученияДанныхСотрудников.cfe__)
     ![image](https://github.com/flsprms/custom_lead/assets/149524130/de79282b-7304-4403-932c-17902d4386e7)  
      Файл -> Открыть -> Выбрать (__1c/odata.epf__) -> Выбрать все -> Сохранить
    ![image](https://github.com/flsprms/custom_lead/assets/149524130/f2b8c4c8-f11c-4716-807a-cbe682ff41a2)

## Конфигурация

В файле конфигурации Odoo необходимо указать параметр __1c_get_personal_data_url__  
{url}/{IBName}/hs/personaldata/v1/getpassportdata  
Пример:
`1c_get_personal_data_url = http://localhost/DemoHRMCorp/hs/personaldata/v1/getpassportdata`

# Расширение моделей crm.lead, hr.employee, telegram bot __(19.03.2024)__

## Odoo

- К модели __crm.lead__ добавлено поле __employee__ (выбор работника из числа сотрудников)
- К модели __hr.employee__ добавлено поле __telegram_id__ (его можно получить в боте, нажав кнопку "Мой telegram ID")
- В модуле __lead__ также реализована отправка сообщения с адресом сотруднику:
    - *при создании лида*
    - *смене работника у лида*
    - *смене адреса лида*
 
![image](https://github.com/flsprms/custom_lead/assets/149524130/108c5b6e-15b0-4f4e-930d-425fe6d525d6)


## Telegram bot

Телеграм бот с помощью которого работник может:
- Получить свой telegram ID
- Получить сообщение о новом лиде / смене адреса у лида
- Отправить сообщение в __chatter__ лида

![image](https://github.com/flsprms/custom_lead/assets/149524130/ec0e0748-28e2-4aab-9656-673f24c3b0ae)  

![image](https://github.com/flsprms/custom_lead/assets/149524130/f7ef9e94-6cda-4771-93f3-baec3e69cb6c)



## Конфигурация

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

## Установка и запуск  

### Odoo

При запуске odoo (файл *odoo-bin*) нужно передать конфигурационный файл с параметром __-c__  
__Пример__:  
`-c C:\Users\...\conf\odoo.conf ...`

  
### Telegram bot
Для работы бота необходимо установить библиотеку __aiogram__  
  
`pip install aiogram==3.4.1`

  
При запуске бота (файл *bot/main.py*) также нужно передать файл конфигурации  
__Пример__:  
`C:\Users\...\conf\odoo.conf ...`
