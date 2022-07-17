# OPTI Программа газодинамического расчета турбины
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
___
OPTI является программой газодинамического расчета турбины. Разработана на смену предущей версии OPTI, написаной для операционной системы MS-DOS. Предназначена для студентов и преподавателей Высшей школы энергетического машиностроения Санкт-Петербургского политехнического университета Петра Великого.
___
### Технологии и библиотеки
Python 3.7, Auto PY to EXE, PyFPDF, PDF2DOCX

### Последовательность действий для запуска проекта и установки виртуального окружения
- Клонировать репозиторий и перейти в него в командной строке.
```
git clone https://github.com/madpenguinw/OPTI
```
- Из корневой папки проекта:
```
python -m venv venv
source venv/Scripts/activate
python -m pip install --upgrade pip
```
- Установка зависимостей из корневой папки проекта:
```
pip install -r requirements.txt
```
- Выход из виртуального окружения
```
deactivate
```
### Шаблон наполнения файла data.txt
```
7 3000 489000 3800000 446.49 828 0 1.33 461
0.13 0.136 1.33 1.336 124 132 0 90500 0.111 1 1
0.146 0.153 1.346 1.353 125 133 0 90500 0.122 0.875 1
0.164 0.172 1.364 1.372 126 134 0 90500 0.144 0.875 1
0.189 0.2 1.389 1.4 128 136 0 91000 0.166 0.875 1
0.229 0.242 1.429 1.442 130 138 0 91803 0.198 0.867 1
0.263 0.279 1.463 1.479 132 140 0 94000 0.218 0.867 1
0.305 0.31 1.505 1.51 134 142 0 102976.9 0.218 0.867 1
```
### Файл data.txt
- Файл data.txt содержит исходные данные для расчетов.
- При наличии файла data.txt, его следует положить в корневую папку проекта. В уже готовом файле data.txt, при работе программы, данные не изменяются. Пример файла data.txt содержится в данном репозитории, шаблон заполнения представлен выше.
- Если  файл data.txt отсутствует, он создатся в корневой папке проекта при первом ручном вводе данных в программе.
- При ручном внесении изменений в файл data.txt данные следует разделять пробелом, целую часть числа отделять точкой.
- В первой строке файла data.txt записываются параметры, общие для всей турбины (х - числовое значение задаваемого параметра):
1. Число ступеней (1 <= x <= 13). 
2. Чacтoта вpaщeния poтopa об/мин (0 < x <= 120000).
3. Дaвлeниe гaзa зa тypбинoй Па (1000 <= x <= 1000000).
4. Дaвлeниe торможения перед тypбинoй Па (0 < x <= 40000000)
5. Рacxoд гaзa (пара) нa вxoдe в тypбинy кг/с (0 < x <= 2000)
6. Тeмпepaтypа тopмoжeния пepeд тypбинoй К (0 < x <= 2200)
7. Влажность на входе в туpбину % (0 <= x <= 20)
8. Коэффициент изoэнтpoпы для гaзa (0 < x)
9. Газовая постоянная Дж/кг*К (0 < x)
- Далее в каждой строчке записываются параметры, задаваемые для каждой ступени в отдельности:
1. Выcoта направляющей лопатки м (0 < x).
2. Выcoта рабочей лопатки м (0 < x).
3. Средний диaмeтp НА м (0 < x).
4. Средний диaмeтp РК м (0 < x).
5. Число сопловых лопаток (0 < x).
6. Число рабочих лопаток (0 < x).
7. Влажность на выходе из ступени % (0 <= x < 20).
8. Рacпoлaгaeмый пepeпaд энтaльпий Дж/кг (0 < x < 300000).
9. Тepмoдинaмичecкая cтeпeнь peaктивнocти нa cpeднeм диaмeтpe (0 <= x <= 1).
10. Отнocительный pacxoд перед cтyпeнью (0 < x).
11. Пpизнaк нaличия бaндaжa (х = 1 или x = 0).

### Описание устройства программы и методики создания исполняемого файла
- В файле OPTI.py содержится расчетная часть программы. При работе в dev-режиме запускать следует именного его.
- Файл input_funcs.py отвечает за получение исходных данных и формировании, при необходимости, файла data.txt.
- Файл output_funcs.py отвечает за создание pdf файла, содержащего таблицы с данными, преобразовании .pdf файла в .docx файл.
- После произведения расчетов в корневой папке проекта появятся файлы с расширениями .pdf и .docx. Их название задается пользователем в начале работы с программой. При введении некорректного названия файлов, по умолчанию они будут создны, как Results.pdf и Results.docx.
- Для создания из файлов проекта исполняемого файла OPTI.exe в консоль следует ввести auto-py-to-exe. В возникшем окне необходимо ввести путь к файлу OPTI.py, выбрать вариант "Одна папка", выбрать вариант "Консольное приложение", ввести путь к иконке (пример файла .ico содержится в репозитории), ввести путь к дополнительным файлам input_funcs.py, output_funcs.py и TimesNewRoman.ttf, в настройках выбрать предпочитаемую папку вывода, нажать на кнопку "КОНВЕРТИРОВАТЬ .PY В .EXE".

### Автор

Соколов Михаил 

Проект сделан в рамках выпускной квалификационной работы (ВКР) бакалавра Санкт-Петербургского политехнического университета Петра Великого.
