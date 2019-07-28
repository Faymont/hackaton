## /api/for_people/ — Содержит api для работы с тестами 

---

### /api/for_people/ticket/
Отправка номер талона, в ответ получаем 5 вопросов
#### Методы:
* POST
#### POST Параметры:
* ticket: (`CharField`) **REQUIRED** — "Номер талона."
#### POST Возвращает:
* array: (`ArrayField`) - "Вопросы."
    * id: (`IntegerField`) — "ID вопроса."
    * question: (`CharField`) — "Содержимое вопроса."

---

### /api/for_people/redeem/
Отправка ответов на вопросы
#### Методы:
* POST
#### POST Параметры:
* answers: (`ArrayField`) - "Ответы."
    * id: (`IntegerField`) — "ID вопроса."
    * answer: (`IntegerField`) — "Оценка."

---
