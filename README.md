# Парсер fixprice
Данный парсер собирает данные товаров с интернет-магазина [fix-price](https://fix-price.com/) по заданным категориям.

## Установка

```commandline
git clone https://github.com/Weffy61/fix_parse.git
```

## Установка зависимостей

Переход в директорию с исполняемым файлом

```commandline
cd fix_parse
```

Установка
```commandline
pip install -r requirements.txt
```

## Запуск
Для запуска паука используйте следующую команду:

```commandline
scrapy crawl fixprice -o output.json -a categories='категория1,категория2,категория3' -a use_proxy=True
```
Где:
- `output.json` - файл, в который будут сохранены собранные данные в формате JSON.  
- `категория1,категория2,категория3` - список категорий товаров, которые вы хотите парсить. 
Минимальное количество категорий для запуска паука — 3.
- use_proxy (по умолчанию `True`) - если указать `False`, парсер будет работать без использования прокси.
  

#### Пример:
Если вы хотите собрать данные для следующих категорий:
- товары для дома/товары для уборки
- бытовая химия/средства для кухни
- продукты и напитки/овощная консервация

С прокси:

```commandline
scrapy crawl fixprice -o 'products.json' -a categories='dlya-doma/tovary-dlya-uborki,bytovaya-khimiya/sredstva-dlya-kukhni,produkty-i-napitki/konservatsiya-ovoshchnaya' -a use_proxy=True
```

Без прокси:
```commandline
scrapy crawl fixprice -o 'products.json' -a categories='dlya-doma/tovary-dlya-uborki,bytovaya-khimiya/sredstva-dlya-kukhni,produkty-i-napitki/konservatsiya-ovoshchnaya' -a use_proxy=False
```
