# **EN**
# Kolomenskoe

Model for recognition, classification and counting of bakery products moving along a conveyor belt in production. SKU 10 units. Considering for 1 line.

## FILES

* load_videos.sh - command for saving videos from rtsp to ./videos
* main.py - script for processing videos from ./videos to insert data to the db
* pyproject.toml - requirements for the project

## Installation

Install dependencies
```bash
pip install -r requirements.txt
```

## Usage

Run docker container
```bash
docker-compose up -d --build
```

Run video saving
```bash
bash load_vodeos.sh &
```

Run the script
```bash
python main.py
```

## Results
The results will be saved in the database

# **RU** 
# Коломенское

Модель для распознавания, классификации и подсчета хлебобулочной продукции, движущейся по конвейерной ленте на производстве. SKU 10 единиц. Рассматриваем для 1 линии.

## Установка

Установите необходимые библиотеки
```bash
poetry install
```

## Запуск

Run video saving
```bash
bash load_vodeos.sh &
```

Run the script
```bash
python main.py
```

## Результаты

Итоговое видео будет находиться в базовой папке с именем **new_video.mp4** или в папке, указанной вами в output_path.