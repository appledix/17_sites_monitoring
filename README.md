# Sites Monitoring Utility

Данный скрипт проверяет переданный ему список сайтов по следующим критериям:
* Сервер отвечает на запрос статусом HTTP 200;
* Доменное имя сайта проплачено как минимум на 1 месяц вперед.

Результат проверки выводится в терминал в виде списка сайтов с кодами состояния HTTP ответа и кол-вом оплаченных дней доменного имени. 
В зависимости от соответствия требованиям в скобках после значения пишется "OK", если все в порядке, или "Warning!", если полученные данные не соответствуют критериям.

### Использование
В терминале: `python3.5 check_sites_health.py  <расположение_текстового файла_со_списком_сайтов>`

### Пример работы
Ввод:
Файл test_urls.txt с содержимым:

    http://rushim.ru
    http://www.slovari.ru
    http://www.biodat.ru
    http://your-english.ru
    http://www.school-net.ru
    foo.bar
    ya.ru

Вывод:

    1) http://your-english.ru
     • HTTP status code: 200(OK)
     • Days until expiration date: 223(OK)
    2) http://www.biodat.ru
     • HTTP status code: 200(OK)
     • Days until expiration date: 384(OK)
    3) http://rushim.ru
     • HTTP status code: 200(OK)
     • Days until expiration date: 12(WARNING!)
    4) http://foo.bar
     • Failed to get HTTP status code.
     • Failed to get domain expiration date.
    5) http://ya.ru
     • HTTP status code: 200(OK)
     • Days until expiration date: 186(OK)
    6) http://www.school-net.ru
     • HTTP status code: 200(OK)
     • Days until expiration date: 254(OK)
    7) http://www.slovari.ru
     • HTTP status code: 200(OK)
     • Days until expiration date: 277(OK)


### Установка скрипта 
В терминале: `git clone https://github.com/appledix/17_sites_monitoring.git`

### Установка зависимостей
В терминале: `pip3 install -r requirements.txt`


# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
