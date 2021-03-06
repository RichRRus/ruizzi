# RUIZZI 1.0.0 Backend

## Подготовительный этап

Для корректного запуска необходимо в корне проекта создать файл
`.env` и скопировать в него содержимое файла [.env.dist](.env.dist)
(при необходимости заменить занчение переменных).Так же необходимо в корне проекта
создать папки `media` и `static`

## Запуск с помощью docker-compose
Проект можно запустить внутри докер контейнера. Проект будет доступен по адресу
`http://localhost:8000`. Документация досутпна по адресу `http://localhost:8000/api/docs/swagger/`

__Запуск для разрабоки__:

```bash
$ docker-compose -f docker-compose.dev.yml up -d
```

__Запуск продакшн версии__:

В файле [.env](.env) установить значение переменной `DJANGO_SETTINGS_MODULE=ruizzi.settings.prod`.
Так же отредактировать все остальные значения переменных на более безопасные.

```bash
$ docker-compose up -d --build
```