* Создать новый каталог для проекта

```
mkdir python-web-final
cd .\python-web-final\
```

* Инициализация git

`git init`

* Создать и активировать виртуальное окружение

```
python -m venv .venv
.\.venv\Scripts\activate
```

* Создать файл .gitignore
```
/.venv/
/.idea/
**/__pycache__/
*.py[cod]
/.env
```
* Создать первый коммит
* Создать новый репозиторий на GitHub и связать с локальным
```
git remote add origin https://github.com/******/python-web-final.git
git push -u origin main
```
* Установить пакет django

`pip install django`

* Создать проект django

`django-admin startproject ot_project`

* Запуск сервера
```
cd .\ot_project\
python manage.py runserver
```
