
# Отчет по юнит тестированию

**Луценко Владимир, К3320**

---

## 1. Анализ тестируемой системы
- **Telegram бот**: @dogpsybot для саморефлексии
- **Основные модули, требующие тестирования**:
  - Обработка ответов пользователей (`answers.py`)
  - Валидация входных данных (`validators.py`)
  - Форматирование сообщений (`formatters.py`)
  - Работа с конфигурацией (`config.py`)

---

## 2. Обоснование выбора компонентов для тестирования

### 2.1 Модуль обработки ответов (`answers.py`)
- Основная бизнес-логика бота


### 2.2 Валидаторы (`validators.py`)
- Защита от некорректных входных данных
- Предотвращение ошибок в БД
- Множество форматов данных

### 2.3 Форматирование (`formatters.py`)
- Корректное отображение сообщений
- Работа с разными типами данных
- Локализация текстов

### 2.4 Конфигурация (`config.py`)
- Критична для запуска бота
- Работа с переменными окружения
- Валидация настроек

---

## 3. Реализованные тесты

### 3.1 Тесты обработки ответов (`test_answers.py`)

```python
def test_process_answer_valid():
    '''
    Arrange: Подготовка валидного ответа
    Act: Обработка ответа
    Assert: Проверка результата
    '''
    # Arrange
    answer = "Это мой тестовый ответ"
    expected_length = len(answer)
    
    # Act
    result = process_answer(answer)
    
    # Assert
    assert result.is_valid
    assert len(result.text) == expected_length
    assert result.error is None

def test_process_answer_empty():
    '''
    Arrange: Подготовка пустого ответа
    Act: Обработка ответа
    Assert: Проверка ошибки
    '''
    # Arrange
    answer = ""
    
    # Act
    result = process_answer(answer)
    
    # Assert
    assert not result.is_valid
    assert result.error == "Answer cannot be empty"
```

### 3.2 Тесты валидации (`test_validators.py`)

```python
def test_validate_telegram_id():
    '''
    Arrange: Подготовка telegram ID
    Act: Валидация ID
    Assert: Проверка результата
    '''
    # Arrange
    valid_id = 123456789
    invalid_id = -1
    
    # Act & Assert
    assert validate_telegram_id(valid_id)
    assert not validate_telegram_id(invalid_id)

def test_validate_notification_time():
    '''
    Arrange: Подготовка времени уведомления
    Act: Валидация времени
    Assert: Проверка результата
    '''
    # Arrange
    valid_time = "09:00"
    invalid_time = "25:00"
    
    # Act & Assert
    assert validate_notification_time(valid_time)
    assert not validate_notification_time(invalid_time)
```

### 3.3 Тесты форматирования (`test_formatters.py`)

```python
def test_format_question():
    '''
    Arrange: Подготовка данных вопроса
    Act: Форматирование
    Assert: Проверка результата
    '''
    # Arrange
    question = {
        "text": "Как ваши дела?",
        "category": "daily"
    }
    
    # Act
    formatted = format_question(question)
    
    # Assert
    assert "Как ваши дела?" in formatted
    assert "[daily]" in formatted
```

### 3.4 Тесты конфигурации (`test_config.py`)

```python
def test_load_config():
    '''
    Arrange: Подготовка тестового конфиг файла
    Act: Загрузка конфига
    Assert: Проверка значений
    '''
    # Arrange
    test_config = {
        "BOT_TOKEN": "test_token",
        "DB_HOST": "localhost"
    }
    
    # Act
    config = load_config(test_config)
    
    # Assert
    assert config.BOT_TOKEN == "test_token"
    assert config.DB_HOST == "localhost"
```



## 4. Результаты тестирования и проблемы

- Отсутствие валидации специальных символов в ответах
- Отсутствие проверки на максимальную длину ответа
