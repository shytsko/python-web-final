# Создаем новый проект

### Создаем новый каталог для проекта

```commandline
mkdir python-web-final
cd .\python-web-final\
```

### Инициализация git

```commandline
git init
```

### Создаем и активируем виртуальное окружение

```commandline
python -m venv .venv
.\.venv\Scripts\activate
```

### Создаем файл .gitignore

```
/.venv/
/.idea/
**/__pycache__/
*.py[cod]
/.env
```

### Создаем первый коммит

### Создаем новый репозиторий на GitHub и связать с локальным

```commandline
git remote add origin https://github.com/******/python-web-final.git
git push -u origin main
```

### Устанавливаем пакет django

```commandline
pip install django
```

### Создаем проект django

```commandline
django-admin startproject ot_project
```

### Запускаем сервер для проверки

```commandline
cd .\ot_project\
python manage.py runserver
```

### Создаем файл с зависимостями

```commandline
pip freeze > requirements.txt
```

В дальнейшем эту команду нужно будет выполнять после добавления новых зависимостей

# Базовые настройки

### Добавим возможность получать параметры через переменные окружения

```commandline
django.db.backends
```

В файле settings.py добавим

```python
import os
from dotenv import load_dotenv

load_dotenv()
```

И заменим определение параметра SECRET_KEY

```python
SECRET_KEY = os.getenv('SECRET_KEY')
```

### Создаем новое приложение для управления пользователями

```commandline
python manage.py startapp user
```

Регистрируем новое приложение

```python
INSTALLED_APPS = [
    ...
    'user',
]
```

### Добавляем новую модель

Документация django рекомендует создавать собственную модель пользователя перед
выполнением первой миграции, поскольку в дальнейшем это позволит упростить внесение
изменений, если понадобится.

В файле допавляем модель _user/model.py_

```python
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass

``` 

Регистрируем модель в админской панели, прописываем в файле _user/admin.py_

```python
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

admin.site.register(User, UserAdmin)
``` 

В файле _settings.py_ указываем параметр, указывающий на класс модели пользователя

```python
AUTH_USER_MODEL = "user.User"
```

В дальнейшем на класс модели пользователя нужно будет ссылаться через этот параметр.
Также его будет возвращать функция ```django.contrib.auth.get_user_model()```

### Настройка подключения к базе данных

Для целей разрабатываемого приложения достаточно возможностей СУБД SQLite, которую Django использует по умолчанию.
Но, для учебных целей будем применять серверную СУБД, например PostgreSQL.

Изменим параметры подключения к базе данных в файле _settings.py_.

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT')
    }
}
```

Параметры подключения необходимо будет прописать в файле _.env_ или передать другим способом через переменные среды

Также необходимо установить пакет драйвера PostgreSQL

```commandline
pip install Django psycopg2
```

### Создаем и применяем первую миграцию

python manage.py makemigrations
python manage.py migrate

### Создаем суперпользователя

```commandline
python manage.py createsuperuser --username=admin --email=admin@mail.com
```

# Создаем базовый шаблон

Базовый шаблон будет содержать элементы интерфейса, общие для всех представлений

### Настраиваем каталог с общими шаблонами

Создаем каталог в корневом каталоге проекта

```commandline
mkdir templates
```

Прописываем параметры в файле _settings.py_.

```python
TEMPLATES = [
    {
        ...
    'DIRS': [BASE_DIR / 'templates', ],
...
},
]
```

### Настраиваем каталог для статических файлов, не относящихся к конкретному приложению

```commandline
mkdir templates
```

Прописываем параметры в файле _settings.py_.

```python
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
```

### Подключение bootstrap

Чтобы получить приемлемый внешний вид интерфейса приложения и, при этом, не тратить время на HTML/CSS верстку
будем использовать фреймворк bootstrap и дополнительно пакет
django-bootstrap5 (https://django-bootstrap5.readthedocs.io/en/latest/index.html),
который позволяет интегрировать bootstrap в шаблоны django.

Устанавливаем пакет django-bootstrap5

```commandline
pip install django-bootstrap5
```

Регистрируем приложение в файле _settings.py_.
```python
INSTALLED_APPS = [
    ...
    'django_bootstrap5',
    ...
]
```

### Создаем базовый шаблон

Создаем базовый шаблон в файле _templates/base.html_

# Приложение главной страницы

### Создаем приложение 
```commandline
python manage.py startapp home
```
### Регистрируем приложение в файле _settings.py_.
```python
INSTALLED_APPS = [
    ...
    'home',
]
```

### Создаем шаблон главной страницы _home/templates/home/home.html_

### Создаем представление главной страницы в файле _home/views.py_

### Создаем файле _home/urls.py_
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
]
```

### Добавляем маршруты в файле _urls.by_ проекта
```python
urlpatterns = [
    ...
    path('/', include('home.urls'))
]
```

 