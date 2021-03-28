# "Сласти от всех напастей"


## Данный проект представляет собой REST-сервис на `Flask` для интернет-магазина. Сервис позволяет:
1. Нанимать курьеров на работу
2. Принимать заказы
3. Оптимально распределять заказы между курьерами
4. При распределении попутно высчитывать рейтинг и заработок курьеров


## Установка
Для работы проекта требуются следующие зависимости:
- `python-dateutil`
- `flask`
- `sqlalchemy v1.3.23`
- `flask-sqlalchemy`


## Обработчики REST API
Подробная схема представлена в файле `openapi.yaml`
1. `POST /couriers`
2. `PATCH /couriers/:id`
3. `POST /orders`
4. `POST /orders/assign`
5. `POST /orders/complete`
6. `GET /couriers/:id`


## Развёртывание
В качестве примера рассмотрим развёртывание на сервере с Ubuntu 20.04 LTS.
Для развёртывания проекта понадобится веб-сервер `Apache` и модуль `mod_wsgi`


### Подготовка
После установки `Apache`, `mod_wsgi` и активации этого модуля нужно создать каталог, в котом будет хранится проект. Рекомендуется разместить его в подкаталоге по пути `/var/www/`. Пусть наш проект называется `slasty`, тогда его каталог будет находится по пути `/var/www/slasty/`.
В этот каталог можно склонировать репозиторий с помощью команды:
```bash
git clone https://github.com/vudeam/ya_backend /var/www/slasty/
```


### Настройка
В каталоге проекта нужно создать WSGI-скрипт, который будет запускать наш проект `slasty`. По сути, этот скрипт выполняет только одно: импортирует приложение `Flask`. Остальную *магию* на сеюя берёт Apache и его модуль mod_wsgi.
Назовём скрипт `slasty.wsgi` и запишем туда следующее:
```wsgi
#!/usr/bin/python3
import sys
sys.path.insert(0, '/var/www/slasty')

from slasty import app as application
```

Теперь нужно сконфигурировать Apache для работы с проектом. Для этого нужно создать файл конфигурации для сайта по пути `/etc/apache2/sites-available/slasty.conf` со следующим содержимым:
```apache
<VirtualHost *:8080>
    DocumentRoot /var/www/slasty
    WSGIScriptAlias / /var/www/slasty/slasty.wsgi

    <Directory /var/www/slasty/slasty>
        Order allow,deny
        Allow from all
        Require all granted
    </Directory>
</VirtualHost>
```

### Запуск
После создания двух небольшой структуры каталогов и двух файлов осталось выполнить некоторые действия для запуска сервиса.
Включение модуля mod_wsgi
```bash
sudo a2enmod wsgi
```

Включение созданного сайта в работу
```bash
sudo a2ensite slasty.conf
```

Перезапуск Apache для применения изменений
```bash
sudo systemctl reload apache2
```

### Работа
После выполнения перечисленных действий REST API-сервис должен начать работать. Проверить это можно в обычном веб-браузере, так как в сервисе есть маршруты, которые обслуживают запросы методом `GET`:
```
http://[IP-адрес сервера]:8080/couriers/1
```

В результате загрузки страницы можно получить либо ошибку `404 Not Found`, что означает, что курьера с переданным ID ещё не существует в базе, либо сведения о запрошенном курьере в формате `JSON`


## Дополнительная информация
Дополнительные материалы по запуску и развёртыванию приложений на `Flask` с помощью `Apache` и `mod_wsgi`:
* [Документация на сайте Flask](https://flask.palletsprojects.com/en/1.1.x/deploying/mod_wsgi/) ([PDF-версия](https://flask.palletsprojects.com/_/downloads/en/1.1.x/pdf/))
* [Простое руководство по развёртыванию приложения Flask](https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps)
* [Настройка конфигурационного файла .conf для Apache](https://www.digitalocean.com/community/tutorials/how-to-set-up-apache-virtual-hosts-on-ubuntu-18-04)
* [Перевод приложения на Flask в пакет (модуль) для Python](https://flask.palletsprojects.com/en/1.1.x/patterns/packages/)
