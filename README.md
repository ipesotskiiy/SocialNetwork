# Django_blog

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
Создать .env файл в котором будут указаны данные для бд

Создать дирректорию log и файл log.log

![image](https://github.com/ipesotskiiy/Django_Shop/assets/82309024/10247509-f2e6-41a1-8044-304960991b22)

Сделать миграции ```python manage.py migrate```

### Для локального запуска

```python manage.py runserver```

# Функции API
- http://127.0.0.1:8000/swagger - получение свагера
- http://127.0.0.1:8000/article/all - получение всех статей
- http://127.0.0.1:8000/comment/all - получение всех комментариев
- http://127.0.0.1:8000/rating/all - получение всех рейтингов
- http://127.0.0.1:8000/article/add - добавить статью
- http://127.0.0.1:8000/comment/add - добавить коммаентарий
- http://127.0.0.1:8000/rating/add - добавить рейтинг
- http://127.0.0.1:8000/comment/<pk> - получить конкрентый комментарий
- http://127.0.0.1:8000/article/<pk> - получить конкретную статью
- http://127.0.0.1:8000/rating/<pk> - получить конкретный рейтинг
- http://127.0.0.1:8000/article/update/<pk> - изменить статью
- http://127.0.0.1:8000/comment/update/<pk> - изменить комментарий
- http://127.0.0.1:8000/rating/update/<pk> - изменить рейтинг
- http://127.0.0.1:8000/article/delete/<pk> - удалить статью
- http://127.0.0.1:8000/comment/delete/<pk> - удалить комментарий
- http://127.0.0.1:8000/rating/delete/<pk> - удалить рейтинг
- http://127.0.0.1:8000/comment/like/<int:pk> - поставить лайк
- http://127.0.0.1:8000/comment/dislike/<int:pk> - поставить дизлайк

Блог напианный на DRF

Логирование 

![image](https://github.com/Ireal-ai/Django_blog/assets/82309024/5b3046ab-4f53-4df3-9a4f-bc223a2b943d)

Модели приложения пользователя

Модель пользователя

![image](https://github.com/Ireal-ai/Django_blog/assets/82309024/55760365-f64d-45e8-9e76-870da13d6b87)

Сериализаторы приложения пользователя

Сериализатор регистрации с проверкой на уникальность адреса электронной почты, свободен ли ввеённый пользователем логин и идентичность вводимых паролей

![image](https://github.com/Ireal-ai/Django_blog/assets/82309024/b195fa5d-4071-4641-b6f7-c391e3a15634)

![image](https://github.com/Ireal-ai/Django_blog/assets/82309024/c9bb94ee-7608-41de-88a9-4e80b61c6730)

![image](https://github.com/Ireal-ai/Django_blog/assets/82309024/cfc73f05-c1bb-4d71-8d33-fbbfb3af7b20)

Сериализатор входа

![image](https://github.com/Ireal-ai/Django_blog/assets/82309024/824b3e87-6ea8-426c-95b9-038635af2f21)

Views приложения пользователя

Регистрации

![image](https://github.com/Ireal-ai/Django_blog/assets/82309024/80afcc57-3952-4745-86ef-916cc3e65772)

Входа

![image](https://github.com/Ireal-ai/Django_blog/assets/82309024/29c18dd7-38ae-47ce-822d-ddcb37827979)

Модели приложения Статьи

Модель статьи

![image](https://github.com/Ireal-ai/Django_blog/assets/82309024/b0a247d0-3e6a-4de7-8d5f-42c55735f76f)

Модель комментария

![image](https://github.com/Ireal-ai/Django_blog/assets/82309024/01e34503-e7e9-4459-b578-94586f916711)

Модель рейтинга

![image](https://github.com/Ireal-ai/Django_blog/assets/82309024/cbb75d10-42cd-4471-aa46-f34a088cd4e9)

Модели лайка и дизлайка

![image](https://github.com/Ireal-ai/Django_blog/assets/82309024/2671268f-f356-43fb-af2a-84eee10b6dee)

Сериализаторы модели Статьи

Сериализатор рейтинга 

![image](https://github.com/Ireal-ai/Django_blog/assets/82309024/d2fc1692-bc6f-4b44-8cf2-b8e6f1b8b151)

Сериализатор статьи

![image](https://github.com/Ireal-ai/Django_blog/assets/82309024/e9faf034-3dcb-4c74-b5bd-4e0df104a746)

![image](https://github.com/Ireal-ai/Django_blog/assets/82309024/5e46c218-e40a-49c0-835e-9a99bbb5a011)

Сериализатор комментариев

![image](https://github.com/Ireal-ai/Django_blog/assets/82309024/ab8af44b-5e75-43b1-9b6e-641d6994588d)

Сериализаторы лайков и дизлайков

![image](https://github.com/Ireal-ai/Django_blog/assets/82309024/cf5c8730-4a7f-4e27-a5c9-df08feeb8d15)

Views приложеня Статьи

viewset Статьи

![image](https://github.com/Ireal-ai/Django_blog/assets/82309024/348482ef-e322-44ed-9da4-2b78aa71b496)

viewset Комментария

![image](https://github.com/Ireal-ai/Django_blog/assets/82309024/b298cf9e-a0c5-414c-a4cd-61f225e23050)

viewset Рейтинга

![image](https://github.com/Ireal-ai/Django_blog/assets/82309024/a8591f1b-8bb9-446c-917b-220af8799ee7)

APIView Лайка

![image](https://github.com/Ireal-ai/Django_blog/assets/82309024/2003ed9e-db91-41df-b03c-343032d11468)

APIView Дизлайка

![image](https://github.com/Ireal-ai/Django_blog/assets/82309024/191f53ba-d05f-4978-8779-80a26ad97ae2)

