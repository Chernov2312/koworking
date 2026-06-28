# TodoList || PetProject

---

### Предварительные требования

- [Python 3.11+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)

### Установка и запуск

1. Клонирование репозитория

```bash
git clone 
```

2. Переход в папку проекта

```bash
cd team-3
```

3. Создание виртуального окружения

Linux/macOS

```bash
python3 -m venv venv
```

Windows (PowerShell)

```powershell
python -m venv venv
```

4. Активация виртуального окружения

Linux/macOS

```bash
source venv/bin/activate
```

Windows (PowerShell)

```powershell
.\venv\Scripts\Activate.ps1
```

5. Установка зависимостей

Для запуска проекта

```bash
pip install -r requirements/prod.txt
```

6. Настройка переменных окружения

Linux/macOS

```bash
cp .env.example .env
```

Windows (PowerShell)

```powershell
Copy-Item .env.example .env
```

```

---
После запуска сервер будет доступен по адресу:

- Сайт: http://127.0.0.1:8000/


---

#### Функционал

**1. Пользователь проходит регистрацию**

Пользователь регистрируется в системе, при желании подключает Tg уведомления для напоминаний.

**2. Задания**

Пользователь может указывать сразу несколько заданий разной сложности, указывать им сроки выполнения

**3. История заданий**

После завершения результат сохраняется в историю пользователя. Для каждого задания доступны:
- дата и время
- выполнено/просрочено
- сделать копию
- удалить из истории

---

#### Установка зависимостей

Для разработки

```bash
pip install -r requirements/dev.txt
```

Для запуска тестов

```bash
pip install -r requirements/test.txt
```

---

#### Запуск тестов

Проверка flake8

```bash
flake8
```

Проверка black

```bash
black --check .
```

Тесты Django
```bash
python3 manage.py test
```

---

###### Разработчик

```
Максим Чернов
```

---

<small>© 2026 Work by Max</small>