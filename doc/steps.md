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

### Создаем новый репозиторий на GitHub и связываем с локальным

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

### Настройка подключения к базе данных

Для целей разрабатываемого приложения достаточно возможностей СУБД SQLite, которую Django использует по умолчанию.
Но, для учебных целей, будем применять серверную СУБД, например PostgreSQL.

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
будем использовать фреймворк bootstrap и дополнительно
пакет `django-bootstrap5` (https://django-bootstrap5.readthedocs.io/en/latest/index.html),
который позволяет упростить интеграцию bootstrap в шаблоны django.

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
Это не окончательный вариант шаблона. Пункты меню взяты для примера проверки работы на текущем этапе. Также имеются
ссылки на ресурсы, которые еще разработаны.

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    {% load django_bootstrap5 %}
    {% bootstrap_css %}
    {% bootstrap_javascript %}
    {% bootstrap_messages %}
    <title>{% block title %}{{ title }}{% endblock %}</title>
</head>
<body>
<div class="container">
    <nav class="navbar navbar-expand-lg bg-light">
        <div class="container-fluid">
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse"
                    data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent"
                    aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                    <li class="nav-item">
                        <a class="nav-link active" aria-current="page" href="{% url 'home' %}">Главная</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#">Link</a>
                    </li>
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown"
                           aria-expanded="false">
                            Dropdown
                        </a>
                        <ul class="dropdown-menu">
                            <li><a class="dropdown-item" href="#">Action</a></li>
                            <li><a class="dropdown-item" href="#">Another action</a></li>
                            <li>
                                <hr class="dropdown-divider">
                            </li>
                            <li><a class="dropdown-item" href="#">Something else here</a></li>
                        </ul>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link disabled" aria-disabled="true">Disabled</a>
                    </li>
                </ul>
            </div>
            <div class="navbar" id="navbarRight">
                <ul class="navbar-nav navbar-right">
                    {% if user.is_authenticated %}
                    <li class="nav-item">
                        <div class="nav-link">{{ user.username }}</div>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'logout' %}">Выход</a>
                    </li>
                    {% else %}
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'login' %}">Вход</a>
                    </li>
                    {% endif %}
                </ul>
            </div>
        </div>
    </nav>

</div>
<div class="container">
    {% bootstrap_messages %}
    {% block content %} CONTENT {% endblock %}
</div>
</body>
</html>
```

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

Контент главной страницы добавим позже

```html
{% extends 'base.html' %}
{% block content %}
<h1>NO CONTENT </h1>
{% endblock %}
```

### Создаем в маршрут для главной страницы в файле _home/urls.py_

Нет необходимости в представлении реализовывать какую-либо логику, поэтому не будем создавать представления,
а воспользуемся стандартным классом `TemplateView` и необходимые параметры передадим в конструктор.

```python
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='home/home.html',
                                  extra_context={"title": "Главная"}), name='home'),
]
```

### Добавляем маршруты в файле _urls.by_ проекта

```python
urlpatterns = [
    ...
    path('/', include('home.urls'))
]
```

# Приложение для управления пользователями

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

В файле _user/model.py_ добавляем модель

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
Также его будет возвращать функция `django.contrib.auth.get_user_model()`

### Создаем и применяем первую миграцию

```commandline
python manage.py makemigrations
python manage.py migrate
```

### Создаем суперпользователя

```commandline
python manage.py createsuperuser --username=admin --email=admin@mail.com
```

### Создаем файл _user/urls.py_

Django содержит готовые представления и формы для управления пользователями. В файле `django.contrib.auth.urls`
содержиться список _urlpatterns_ с маршрутами и представлениями. Поскольку в разрабатываемом приложении не
предполагается
самомтоятельная регистрация пользователей, готовый список избыточен. Скопируем его в свой файл
_user/urls.py_ и оставим только маршруты для входа и выхода

```python
from django.contrib.auth import views
from django.urls import path

urlpatterns = [
    path("login/", views.LoginView.as_view(template_name="user/login.html"), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
]
```

### Добавляем параметры в файл _settings.by_ для перенаправления на главную страницу после входа или выхода, а также URL, на который пользователь будет перенаправляться для аутентификации

```python
LOGIN_REDIRECT_URL = reverse_lazy('home')
LOGOUT_REDIRECT_URL = reverse_lazy('home')
LOGIN_URL = reverse_lazy('login')
```

# Создаем приложение для управления настройками предприятия

### Создаем новое приложение

```commandline
python manage.py startapp company
```

### Регистрируем новое приложение в файле _settings.py_.

```python
INSTALLED_APPS = [
    ...
    'company',
]
```

### Добавляем маршруты в файле _urls.by_ проекта

```python
urlpatterns = [
    ...
    path('company/', include('company.urls')),
]
```

### Создаем модели

```python
from django.db import models
from django.utils.translation import gettext_lazy as _


class Company(models.Model):
from django.core.validators import RegexValidator
from django.db import models


class Company(models.Model):
    """
    Данные организации
    name - Название организации
    unp - 9-значный учетный номер плательщика, должен быть уникальным
    address - адрес
    tel - номер телефона
    fax - номер факса
    email - email, должен быть уникальным
    """
    name = models.CharField(verbose_name="Название", max_length=100)
    unp = models.CharField(verbose_name="УНП", max_length=9, unique=True,
                           validators=[
                               RegexValidator(regex=r'^\d{9}$', message="УНП должен состоять из 9 цифр")
                           ])
    address = models.CharField(verbose_name="Адрес", max_length=100)
    tel = models.CharField(verbose_name="Номер телефона", max_length=20, null=True, blank=True)
    fax = models.CharField(verbose_name="Номер факс", max_length=20, null=True, blank=True)
    email = models.EmailField(verbose_name="E-mail", max_length=15, unique=True, )

    class Meta:
        ordering = ["name"]
        verbose_name = "Организация"
        verbose_name_plural = "Организации"

    def __str__(self):
        return f"({self.unp}) {self.name}"


class Department(models.Model):
    """
    Структурные подразделения организации
    company - организация
    name - наименование структурного подразделения
    """
    company = models.ForeignKey("Company", related_name="departments", on_delete=models.PROTECT)
    name = models.CharField(verbose_name="Название", max_length=100)

    class Meta:
        ordering = ["name"]
        verbose_name = "Подразделение"
        verbose_name_plural = "Подразделения"

    def __str__(self):
        return f"{self.name}"

```

### Регистрируем модели в панели администратора в файле _company/admin.py_

```python
from django.contrib import admin
from .models import Company, Department


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'unp',)
    ordering = ('name',)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('company', 'name',)
    ordering = ('company', 'name',)
    list_filter = ('company',)
```

### Создадим и выполним миграцию

```commandline
python manage.py makemigrations
python manage.py migrate
```

### Добавим в модель пользователя ссылку на модель Company.

Это необходимо, чтобы иметь возможность ограничивать доступ пользователю только к данным той организации,
с которой он связан

```python
class User(AbstractUser):
    company = models.ForeignKey("Company", null=True, default=None, related_name="+", on_delete=models.PROTECT)
```

### Снова создадим и выполним миграцию

```commandline
python manage.py makemigrations
python manage.py migrate
```

### Внесем изменения в настройки панели администратора
Создадим пользовательскую модель интерфейса администратора и изменим регистрацию модели User в файле.
Файл _user/admin.py_
```python
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from django.utils.translation import gettext_lazy as _


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password", "company")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", "company"),
            },
        ),
    )

    list_display = ("username", "email", "first_name", "last_name", "is_staff", 'company')
    list_filter = ("is_staff", "is_superuser", "is_active", "groups", 'company')
    search_fields = ("username", "first_name", "last_name", "email", 'company')
    ordering = ("username",)
```

### Добавим классы форм в файле _company/forms.py_
```python
from django.forms import ModelForm, inlineformset_factory
from .models import Company, Department


class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = '__all__'


DepartmentsFormSet = inlineformset_factory(Company, Department, fields=('name',))
```

### Добавим представление форм в файле _company/views.py_
```python
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import CompanyForm, DepartmentsFormSet


@login_required
def company_view(request):
    context = {'title': 'Организация'}
    company = request.user.company
    context['company'] = company
    if company:
        if request.method == 'POST':
            form = CompanyForm(request.POST, request.FILES, instance=company)
            formset = DepartmentsFormSet(request.POST, instance=company)
            if formset.is_valid() and form.is_valid():
                form.save()
                formset.save()
        else:
            form = CompanyForm(instance=company)
            formset = DepartmentsFormSet(instance=company)
        context['form'] = form
        context['formset'] = formset
    return render(request, 'company/company.html', context)
```

###  Создаем шаблон _company/templates/company/company.html_
```html
{% extends "base.html" %}
{% load django_bootstrap5 %}

{% block content %}
    <h2>Организация</h2>
    {% if company %}
        <form method="post" class="form">
        {% csrf_token %}
        {% bootstrap_form form %}
        <hr>
        <h4>Структуртные подразделения организации</h4>
        {% bootstrap_formset formset layout='horizontal' %}

        {% bootstrap_button button_type="submit" content="Сохранить" %}
        </form>
    {% else %}
        {% bootstrap_alert "Текущий пользователь не связан с организацией!!!" alert_type="warning" %}
    {% endif %}
{% endblock %}
```

###  Создаем URL для представления в файле  _company/urls.py_ 
```python
from django.urls import path
from .views import company_view

urlpatterns = [
    path('', company_view, name='company')
]
```

# Создаем приложение для управления настройками предприятия

### Создаем новое приложение

```commandline
python manage.py startapp company
```

### Регистрируем новое приложение в файле _settings.py_.

```python
INSTALLED_APPS = [
    ...
    'company',
]
```

### Добавляем маршруты в файле _urls.by_ проекта

```python
urlpatterns = [
    ...
    path('company/', include('company.urls')),
]
```

### Создаем модели

```python
class Company(models.Model):
    """
    Данные организации
    name - Название организации
    unp -  УНП
    address - адрес
    tel - телефон
    fax - факс
    email - email
    head - руководитель организации
    """
    name = models.CharField(max_length=100)
    unp = models.CharField(max_length=9)
    address = models.CharField(max_length=100)
    tel = models.CharField(max_length=20, null=True, blank=True)
    fax = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=15)


class Department(models.Model):
    """
    Структурные подразделения организации
    company - организация
    name - наименование структурного подразделения
    head - руководитель структурного подразделения
    """
    company = models.ForeignKey("Company", related_name="departments", on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
```

### Регистрируем модели в панели администратора в файле _company/admin.py_

```python
from django.contrib import admin
from .models import Company, Department

admin.site.register(Company)
admin.site.register(Department)
```

### Создадим и выполним миграцию

```commandline
python manage.py makemigrations
python manage.py migrate
```

### Добавим в модель пользователя ссылку на модель Company.

Это необходимо, чтобы иметь возможность ограничивать доступ пользователю только к данным той организации,
с которой о связан

```python
class User(AbstractUser):
    company = models.ForeignKey("Company", null=True, default=None, related_name="+", on_delete=models.PROTECT)
```

### Снова создадим и выполним миграцию

```commandline
python manage.py makemigrations
python manage.py migrate
```

### Внесем изменения в настройки панели администратора
Создадим пользовательскую модель интерфейса администратора и изменим регистрацию модели User в файле.
Файл _user/admin.py_
```python
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from django.utils.translation import gettext_lazy as _


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password", "company")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", "company"),
            },
        ),
    )

    list_display = ("username", "email", "first_name", "last_name", "is_staff", 'company')
    list_filter = ("is_staff", "is_superuser", "is_active", "groups", 'company')
    search_fields = ("username", "first_name", "last_name", "email", 'company')
    ordering = ("username",)
```
