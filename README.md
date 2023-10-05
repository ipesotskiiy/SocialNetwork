# SocialNetwork

Этот проект ещё в разработке, но уже обладает внцшительным функционалом среди которого: аутентификация по токенам, система комментариев, система рейтинга (в том числе подсчёт среднего), а так же система лайков и дизлайков

 # Используемые языки и фреймворки 
 - Python 3.10
 - Django 4.2.2
 - Django Rest Framework 3.14.0

# Используемые базы данных
- PostgreSQL 2.9.3

# Запуск проекта 
Для начала необходимо сделать клон проекта
```
git clone https://github.com/ipesotskiiy/Django_blog/tree/master
```

После чего необходимо установить библиотеки pip install -r requirements.txt

Создать .env файл в котором будут указаны данные для бд

Создать дирректорию log и файл log.log

![image](https://github.com/ipesotskiiy/Django_blog/assets/82309024/7cacfa9f-1c9f-4cd7-9946-5ba1b20c1a4a)


Сделать миграции ```python manage.py migrate```

### Для локального запуска

```python manage.py runserver```

# Функции API
- http://127.0.0.1:8000/swagger - получение свагера

