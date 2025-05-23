# База данных для организаторов выставки собак

## Описание проекта
Проект представляет собой приложение для управления информацией о выставках собак. Система позволяет хранить данные об участниках, экспертах, породах, клубах, рингах и медалистах, а также генерировать отчеты и справки. Реализован интерфейс для удобного взаимодействия с данными в режиме диалога.

## Технологии
- **СУБД**: SQLite
- **Язык программирования**: Python
- **Графический интерфейс**: PySide6 (Qt для Python)

## Основные функции
- **Управление данными**:

  - Добавление/удаление/редактирование записей участников, собак, клубов, экспертов и т.д.

  - Перемещение участников между клубами.

  - Назначение экспертов на ринги.

- **Отчеты**:

  - Справка о призовых местах участников.

  - Отчет о выступлении клуба (количество участников, победители по породам).

- **Поиск информации**:

  - Определение ринга для участника.

  - Список пород, представленных клубом.

  - Эксперты, обслуживающие конкретную породу.

## Структура базы данных
**Основные таблицы**:

- Участники (participants): ID, собака, клуб, номер участника.

- Собаки (dogs): ID, кличка, порода, возраст, регистрационные номера.

- Породы (breeds): ID, название.

- Клубы (clubs): ID, название, диапазон номеров участников.

- Эксперты (experts): ID, ФИО, клуб.

- Ринги (rings): ID, порода.

- Судейство (judging): связь экспертов и рингов.

- Медалисты (medalists): участник, тип медали.


## Пример открытой таблицы "Собаки"
![screenshot](https://github.com/user-attachments/assets/7d5534d5-b2a7-4b20-b77e-895f8f28c1d2)
