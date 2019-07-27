## /api/users/ — Содержит api для работы с пользователями 

---

### /api/users/login/
Аутентификация по паролю.
#### Методы:
* POST
#### POST Параметры:
* email(`EmailField`) **REQUIRED** — "Email"
* password(`CharField`) **REQUIRED** — "Пароль"
#### POST Возвращает:
* id: (`IntegerField`) — "ID"
* email: (`EmailField`) — "Email адрес"
* username: (`CharField`) — "Ник"
* date_joined: (`DateTimeField`)
* social_auth: (`ManyRelatedField`) — "Список соц. сетей пользователя"

---

#### /api/users/logout/
Выход
#### Методы:
* GET

---
