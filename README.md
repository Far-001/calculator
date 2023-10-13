# Проект Calculator

## Описание

Калькулятор считает любые правильные математические выражения, и хранит историю для каждой отдельной сессии.

### Технологии
Python 3.10.12,
Django 3.2.3

## Запуск проекта в dev-режиме

- Клонировать репозиторий и перейти в него в командной строке.

```bash
git clone git@github.com:Far-001/calculator.git
```

```bash
cd calculator
```

- Установить и активировать виртуальное окружение:

```bash
python -m venv venv
```

```bash
source venv/Scripts/activate
```

- Установить/обновить pip и зависимости из файла requirements.txt:

```bash
python -m pip install --upgrade pip
```


```bash
pip install -r requirements.txt
```

- Выполняем миграции:

```bash
python manage.py migrate
```

- Запускаем проект:

```bash
python manage.py runserver
```

### Автор
Антон Корчагин - [Far-001](https://github.com/Far-001)