
# Отчет по интеграционному тестированию

**Луценко Владимир, К3320**

---

## 1. Описание тестируемой системы
- **Telegram бот**: @dogpsybot для психологической саморефлексии
- **Стек**: Python/aiogram, PostgreSQL/SQLAlchemy, JSON для хранения текстов
- **Основные компоненты**:
  - Хранение ответов пользователей
  - Управление состояниями диалога

---

## 2. Тестируемые интеграции и обоснование их выбора

### 2.1 База данных и бизнес-логика
- Основное хранилище ответов пользователей — потеря данных критична

### 2.2 Управление состояниями
- Потеря состояния диалога аффектит пользовательский опыт
- Необходимость синхронизации состояний между разными обработчиками

### 2.3 Локализация
- Отсутствие текстов полностью блокирует работу бота

### 2.4 Журналирование (сохранение ответов)
- Ответы пользователей — основная ценность сервиса
- Требуется гарантия сохранности всех ответов

---

## 3. Реализованные тесты

### 3.1 Тест управления состояниями (test_state_management.py)

```python
async def test_state_management_integration(message_mock, state_mock):
    await choose(message_mock, state_mock)
    state_data = await state_mock.get_data()
    current_state = await state_mock.get_state()
    
    assert current_state == Jour.choose
    assert state_data is not None
```
### 3.2 Тест локализации (test_localization.py)

```python
async def test_localization_integration():
    assert data.main_menu.text is not None
    assert data.jour.choose.text is not None
    assert data.jour.notif.change_time_text is not None
```
### 3.3 Тест сохранения ответов (test_journaling.py)

```python
async def test_write_answer_integration(message_mock, state_mock, session):
    telegram_id = message_mock.from_user.id
    answer_text = "Test answer"
    message_mock.text = answer_text
    
    await create_user(
        session,
        telegram_id=telegram_id,
        full_name=message_mock.from_user.full_name,
        username=message_mock.from_user.username,
        language_code=message_mock.from_user.language_code
    )
    await session.commit()
    
    await state_mock.set_state(Jour.work_ans)
    await state_mock.set_data({
        "datas": [{
            "id": 1,
            "category": "daily",
            "question": "Test question"
        }]
    })
    
    await work_ans(message_mock, state_mock, session)
    
    saved_answers = await get_last_answers(
        session,
        telegram_id=telegram_id,
        category='daily'
    )
    assert len(saved_answers) == 1
    assert saved_answers[0]['answer'] == answer_text
```
### 3.4 Тест инициализации базы данных (init_test_db.py)

```python
def init_test_db():
    env_path = Path(__file__).parent.parent / '.env.test'
    load_dotenv(env_path)
    
    DATABASE_URL = (
        f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('POSTGRES_DB')}"
    )
    
    engine = create_engine(DATABASE_URL)
    
    # Создание БД если не существует
    if not database_exists(engine.url):
        create_database(engine.url)
        print(f"Created database: {os.getenv('POSTGRES_DB')}")
    
    try:
        connection = engine.connect()
        print("Successfully connected to the database!")
        connection.close()
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        sys.exit(1)
```
---

## 4. Результаты и выявленные проблемы
- **Race condition** при параллельном обновлении состояний
- Возможная потеря данных при сбоях
