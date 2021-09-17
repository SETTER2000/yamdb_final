# REST API YaMDb
![example workflow](https://github.com/SETTER2000/yamdb_final/actions/workflows/yamdb_workflow.yaml/badge.svg)

<a href="http://kino2000.ru/api/v1/" target="_blank">Demo API</a>

### Описание

База отзывов пользователей о фильмах, книгах и музыке. Впрочем ограничений 
по категориям не существует, всё зависит от потребностей. Можно легко создавать в 
административном разделе новые категории пользователей, отзывы и  т.д. 
Полный контроль над всем API. 
Всё выше сказанное возможно добавить через API с другого программного 
интерфейса.


### Технологии
Python 3

Django REST Framework 

PostgreSQL

Simple-JWT
(токены для авторизации и регистрации)

Docker
 
### Документация по API
_Документация по API будет доступна после установки, по адресу /redoc._


## Install
Предварительно установить Docker:

<a href="https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04-ru">Ubuntu 20.04</a>

<a href="https://docs.docker.com/desktop/windows/install/">Windows 10</a>


### Запуск проекта

- Переходим в главную директорию пользователя
```.env
cd ~
``` 

- Создать конфиг-файл  
```
sudo nano docker-compose.yaml
```
- Скопировать в него следующий конфиг
```
version: '3.8'

services:
  db:
    image: postgres:12.4
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    env_file:
      - ./.env
  web:
    image: setter2000/yamdb:latest
    restart: always
    command: gunicorn api_yamdb.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - static_value:/code/static/
      - media_value:/code/media/
    depends_on:
      - db
    env_file:
      - ./.env

  nginx:
    image: nginx:1.19.3
    ports:
      - "80:80"

    volumes:
      - ./nginx/default.conf:/etc/nginx/conf.d/default.conf
      - static_value:/var/html/static/
      - media_value:/var/html/media/

    depends_on:
      - web

volumes:
  postgres_data:
  static_value:
  media_value:

```
- Создать директорию 
```
sudo mkdir nginx 
```
- Создать конфиг для nginx в файле default.conf
```
sudo nano nginx/default.conf 
```
- Вставить в nginx/default.conf 
```
server {
    listen 80;
    server_name 127.0.0.1;
    server_tokens off;
    location /static/ {
        root /var/html/;
    }
    location /media/ {
        root /var/html/;
    }
    location / {
        proxy_pass http://web:8000;
        proxy_set_header Host $host;
    }
}
```

- Запускаем сервисы 

```
docker-compose up -d 
```

- Создаём структуру приложения в DB:

```
docker-compose exec web python manage.py makemigrations --noinput
```

```
docker-compose exec web python manage.py migrate --noinput
```

- Добавляем статику:

```
docker-compose exec web python manage.py collectstatic --no-input
```


- Добавляем тестовые данные в DB и superuser:

```
docker-compose exec web python manage.py loaddata fixtures.json
```
## Использование
После удачного выполнения всех команд выше, станет доступна 
административная часть и ваш API готов к приёму запросов.

- Админка
```
<your domain>/admin
```

- Login
```.env
admin   
```

- Password
```.env
123123
```

### Авторизация
Для использования API нужен токен

- Нужно получить токен для вашего email, который уже зарегистрирован в этом 
API. Зарегистрировать пользователя может superuser (по умолчанию admin), в 
административной 
панеле зарегистрировав нужного пользователя. Либо тоже самое superuser может
 сделать используя API (/redoc - раздел документации USERS)

- После регистрации пользователя сделать запрос на получения токена 
(/redoc - раздел документации AUTH)

## Подводные камни
При уставновке могут возникнуть обстоятельства при которых вы не сможете 
запустить приложение смотрите следующие варианты исправления:

- В Ubuntu у вас может быть занять 80 порт, например службой apache2. 
Остановить её можно командой
```.env
sudo systemctl stop apache2
``` 


### Авторы
<a href="https://github.com/keplian">keplian</a>,
<a href="https://github.com/SETTER2000">SETTER2000</a>,
<a href="https://github.com/KondratevAD">KondratevAD</a>


