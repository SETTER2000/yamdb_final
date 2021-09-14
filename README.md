# REST API YaMDb

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

- Клонировать репозиторий

```
git clone git@github.com:SETTER2000/infra_sp2.git
```

- Запускаем сервисы 


```
cd infra_sp2 
```
```
docker-compose up -d --build
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
Александр, Павел и Александр 

