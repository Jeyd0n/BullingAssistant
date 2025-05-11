PYTHON=python3.11.9
VENV?=.venv
SRC_DIR=src
TEST_DIR=tests

# Основные команды
up:
	docker-compose up --build

down:
	docker-compose down

restart: down up

build:
	docker-compose build

logs:
	docker-compose logs -f

# Тестирование
test:
	docker-compose run --rm pytest ./tests

# Линтинг и автоформатирование (опционально)
lint:
	black .

# Установка зависимостей локально
install:
	pip install -r ./requirements.txt

# Удаление всех контейнеров
clean:
	docker-compose down -v --remove-orphans

# Проверка подключения
healthcheck:
	docker exec telegram-bot python -c "import main; print('Application is ready')"