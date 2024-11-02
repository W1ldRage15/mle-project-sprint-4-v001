# Подготовка виртуальной машины

## Склонируйте репозиторий

Склонируйте репозиторий проекта:

```
git clone https://github.com/yandex-praktikum/mle-project-sprint-4-v001.git
```

## Активируйте виртуальное окружение

Используйте то же самое виртуальное окружение, что и созданное для работы с уроками. Если его не существует, то его следует создать.

Создать новое виртуальное окружение можно командой:

```
python3 -m venv env_recsys_start
```

После его инициализации следующей командой

```
. env_recsys_start/bin/activate
```

установите в него необходимые Python-пакеты следующей командой

```
pip install -r requirements.txt
```

### Скачайте файлы с данными

Для начала работы понадобится три файла с данными:
- [tracks.parquet](https://storage.yandexcloud.net/mle-data/ym/tracks.parquet)
- [catalog_names.parquet](https://storage.yandexcloud.net/mle-data/ym/catalog_names.parquet)
- [interactions.parquet](https://storage.yandexcloud.net/mle-data/ym/interactions.parquet)
 
Скачайте их в директорию локального репозитория. Для удобства вы можете воспользоваться командой wget:

```
wget https://storage.yandexcloud.net/mle-data/ym/tracks.parquet

wget https://storage.yandexcloud.net/mle-data/ym/catalog_names.parquet

wget https://storage.yandexcloud.net/mle-data/ym/interactions.parquet
```

## Запустите Jupyter Lab

Запустите Jupyter Lab в командной строке

```
jupyter lab --ip=0.0.0.0 --no-browser
```

# Расчёт рекомендаций

Код для выполнения первой части проекта находится в файле `recommendations.ipynb`. Изначально, это шаблон. Используйте его для выполнения первой части проекта.  

  
# Результат  
Ссылка на проект: https://github.com/W1ldRage15/mle-project-sprint-4-v001.git
S3_BUCKET_NAME:s3-student-mle-20240729-52fe31e1ec

# Сервис рекомендаций

Код сервиса рекомендаций находится в файле `recommendations_service.py`.

<*укажите здесь необходимые шаги для запуска сервиса рекомендаций*>  
Перейти в папку с сервисами: cd fastapi
Запустить сервис: uvicorn recommendations_service:app --port 8000  
Запустить сервис для поиска похожих: uvicorn features_service:app --port 8010  
Запустить сервис для событий: uvicorn events_service:app --port 8020  
Онлайн- и офлайн-рекомендации выбирабтся как чет и нечет (чет - офлайн, нечет - онлайн). 

# Инструкции для тестирования сервиса

Код для тестирования сервиса находится в файле `test_service.py`.

<*укажите здесь необходимые шаги для тестирования сервиса рекомендаций*>  
Выполнить команду: python3 test_service.py из папки mle-project-sprint-4-v001  
Логи результатов находятся в файле: test_service.log  
Логи рекомендаций для пользователя находятся в файле: rec_service.log  
  
# Вывод  
  
По логам можно определить, что для пользователя без персональных рекомендаций в качестве офлайн рекомендаций выдаются треки из топа популярных.  
У позьзователей без онлайн-истории нет онлайн рекомендаций.  
Для пользователя с персональными рекомендациями и онлайн-историей в качестве офлайн рекомендаций выдаются треки из персональных рекомендаций,  
а в качестве онлайн рекомендаций выдаются похожие треки.
