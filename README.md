# flask_test
Тестовое задание на вакансию - https://spb.hh.ru/vacancy/42424608 <br />
Реализовано API - url для доступа ```http://35.228.49.159/api/v1``` <br />
Доступные функции: <br />
Регистрация - ```/register/``` (доступны методы ['POST']) <br />
Пример регистрации на Python
```
import requests
params = {'email': '***@gmail.com', 'username': '123', 'passwd': '456'}
r = requests.post('url', params = params)
```
Далее все запросы на создание/изменение/удаление постов/комментариев требует базовой авторизации <br />
Работа с постами - ```/post/``` <br />
Создание поста
```
import requests
auth = ('123', '456')
params = {'title': 'content', 'content':'content'}
r = requests.post('url', params=params, auth=auth)
```
Редактирование поста
```
import requests
auth = ('123', '456')
params = {'post_id': 'id', 'title': 'content', 'content':'content'}
r = requests.put('url', params=params, auth=auth)
```
Удаление поста
```
import requests
auth = ('123', '456')
params = {'post_id': 'id'}
r = requests.delete('url', params=params, auth=auth)
```
Получить все посты (без авторизации)
```
import requests
r = requests.get('url')
```

Работа с комментариями - ```/comment/``` <br />
Создание комментария
```
import requests
auth = ('123', '456')
params = {'post_id': 'id', 'title': 'content', 'content':'content'}
r = requests.post('url', params=params, auth=auth)
```
Редактирование коммментария
```
import requests
auth = ('123', '456')
params = {'comment_id': 'id', 'title': 'content', 'content':'content'}
r = requests.put('url', params=params, auth=auth)
```
Удаление комментария
```
import requests
auth = ('123', '456')
params = {'comment_id': 'id'}
r = requests.delete('url', params=params, auth=auth)
```
Получить все комментарии (без авторизации)
```
import requests
r = requests.get('url')
```
