# RU
## Описание
Данные проект предназначен для автоматизации анализа и мониторинга производственных процессов на основе видеоданных. Система использует модель компьютерного зрения для определения количества продукции на конвейерной ленте и предоставляет удобный интерфейс для визуализации данных через инструмент Metabase.

### Основные возможности:
- Обработка видеопотока с производственной линии.
- Обнаружение и подсчет продукции на основе модели YOLOv8.
- Визуализация данных и мониторинг ключевых метрик с помощью Metabase.
- Использование контейнеризации Docker для упрощения развертывания и масштабирования системы.

![work in progress](assets/short.gif)

## Структура проекта
```
project-root/
│
├── models/
│
├── notebooks/
│   ├── chaos
│   └── reports
│       └── yolo_train_pipeline.ipynb
│
├── src/
│   ├── database/
│   │   ├── config.py
│   │   ├── crud.py
│   │   ├── database.py
│   │   └── model.py
│   ├── helpers/
│   │   └── helpers.py
│   ├── services/
│   │   ├── config.py
│   │   ├── video_loader.py
│   │   └── video_processer.py
│   └── main.py
│
├── .pre-commit-config.yaml
├── docker-compose.yml
├── Dockerfile
├── poetry.lock
└── pyproject.toml
```

## Перед установкой
Перед установкой требуется выполнить несколько подготовительных шагов:

1. **Скачать обученную модель**:
   Можно использовать утилиту `gdown` для скачивания артифакта модели. Команда для скачивания:
   ```sh
   gdown --id 1obu1ou0-BcRruiGWY9-jT-lo7L-DhYIi -O models/
   ```

2. **Создать файл `.env`**:
   В корне проекта создайте файл `.env` с переменными окружения. Используйте следующий шаблон:
   ```env
    # app settings
    MODEL_NAME = "best.pt" # name of downloaded model
    RTSP_URL = "rtsp://77.232.139.186:8554/live.stream" # rtsp stream url (will be available until 18 of june 2024)
    VIDEO_LENGTH_S = 60 # length of the each video to download in seconds

    # db settings
    DB_HOST = "postgres"
    DB_PORT = 5432
    DB_NAME = "postgres"
    DB_PASSWORD = "admin"
    DB_USERNAME = "postgres"

    # postgres db settings
    POSTGRES_USER = "postgres"
    POSTGRES_PASSWORD = "admin"
    POSTGRES_DB = "postgres"

    # pgadmin settings
    PGADMIN_DEFAULT_EMAIL = "postgres@pg.com"
    PGADMIN_DEFAULT_PASSWORD = "xxx"
   ```

## Установка
Для установки и запуска проекта требуется установленный Docker. Выполните следующие шаги:

1. Убедитесь, что Docker установлен на вашем компьютере.
2. В корневом каталоге проекта выполните команду:
   ```sh
   docker-compose up -d
   ```
   Эта команда запустит все необходимые сервисы в фоновом режиме.

Будут доступны следующие сервисы:
* localhost:3333 - Metabase
* localhost:5050 - PgAdmin

Теперь ваша система готова к использованию! Вы можете использовать Metabase для визуализации и анализа данных, а также следить за производственными процессами в реальном времени.

## Обратная связь
Я буду рад получить обратную связь! Если у вас есть вопросы, предложения или вы столкнулись с проблемами, пожалуйста, свяжитесь со мной по следующим контактам:

- **Telegram**: [@smrtmr](t.me/smrtmr)
- **Email**: [smrtim17@gmail.com](mailto:smrtim17@gmail.com)


# EN
## Project Description
This project is designed to automate the analysis and monitoring of production processes based on video data. The system uses computer vision model to determine the quantity of products on the conveyor belt and provides a user-friendly interface for data visualization through Metabase.

### Key Features:
- Processing of video stream from the production line.
- Detection and counting of products using YOLOv8 model.
- Data visualization and monitoring of key metrics using Metabase.
- Use of Docker containerization for easy deployment and scaling of the system.

## Project Structure
```
project-root/
│
├── models/
│
├── notebooks/
│   ├── chaos
│   └── reports
│       └── yolo_train_pipeline.ipynb
│
├── src/
│   ├── database/
│   │   ├── config.py
│   │   ├── crud.py
│   │   ├── database.py
│   │   └── model.py
│   ├── helpers/
│   │   └── helpers.py
│   ├── services/
│   │   ├── config.py
│   │   ├── video_loader.py
│   │   └── video_processer.py
│   └── main.py
│
├── .pre-commit-config.yaml
├── docker-compose.yml
├── Dockerfile
├── poetry.lock
└── pyproject.toml
```

## Before Installation
Before installation, a few preparatory steps are required:

1. **Download the trained model**:
   Use the `gdown` utility to download the model artifact. Command for downloading:
   ```sh
   gdown --id 1obu1ou0-BcRruiGWY9-jT-lo7L-DhYIi -O models/
   ```

2. **Create a `.env` file**:
   Create a `.env` file in the root of the project with environment variables. Use the following template:
   ```env
    # app settings
    MODEL_NAME = "best.pt" # name of downloaded model
    RTSP_URL = "rtsp://77.232.139.186:8554/live.stream" # rtsp stream url (will be available until 18 of june 2024)
    VIDEO_LENGTH_S = 60 # length of the each video to download in seconds

    # db settings
    DB_HOST = "postgres"
    DB_PORT = 5432
    DB_NAME = "postgres"
    DB_PASSWORD = "admin"
    DB_USERNAME = "postgres"

    # postgres db settings
    POSTGRES_USER = "postgres"
    POSTGRES_PASSWORD = "admin"
    POSTGRES_DB = "postgres"

    # pgadmin settings
    PGADMIN_DEFAULT_EMAIL = "postgres@pg.com"
    PGADMIN_DEFAULT_PASSWORD = "xxx"
   ```

## Installation
To install and run the project, Docker must be installed on your computer. Follow these steps:

1. Ensure Docker is installed on your machine.
2. In the root directory of the project, run the command:
   ```sh
   docker-compose up -d
   ```
   This command will start all necessary services in the background.

Now your system is ready to use! You can use Metabase for data visualization and analysis, as well as monitor production processes in real-time.

## Feedback
I would be happy to receive your feedback! If you have any questions, suggestions, or encounter any issues, please contact me at:

- **Telegram**: [@smrtmr](t.me/smrtmr)
- **Email**: [smrtim17@gmail.com](mailto:smrtim17@gmail.com)