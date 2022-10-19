# CISCO API CLASS

cisco.py

Класс использует REST API от Cisco ISE и содержит следующие методы:

```python
def add_user(
        login,  # будущий логин пользователя
        email,  # e-mail пользователя
        namefirst,  # имя пользователя
        namelast,  # фамилия пользователя
        description,  # описание (поле description в ISE) пользователя
        identitygroups,  # список id групп пользователя
        password_id_store='AD')  # метод авторизации (по умолчанию - Active Directory)


def find_userid_by_name(
        login)  # будущий логин пользователя


def find_user_profile_by_id(
        userid)  # уникальный ID пользователя


def modify_user(
        userid='',  # уникальный ID пользователя
        user_identity_groups='',  # список id групп пользователя
        username='',  # логин пользователя
        user_description='')  # описание (поле description в ISE) пользователя


def delete_user(
        userid='',  # уникальный ID пользователя
        username='')  # логин пользователя
```

Каждый из классов возвращаяет http статус и текст ответа в JSON

```python
return [response.status, response.read()]
```

Пример выдачи метода

```python
find_user_profile_by_id("<user-id>")
```

```yaml
{
  "InternalUser": {
    "id": "<user-id>",
    "name": "test",
    "description": "Added by script",
    "enabled": true,
    "email": "<email>@<domain>",
    "password": "*******",
    "firstName": "ERS",
    "lastName": "Test",
    "changePassword": false,
    "identityGroups": "<group-id-1>,<group-id-2>,<group-id-3>",
    "expiryDateEnabled": false,
    "enablePassword": "*******",
    "customAttributes": {
    },
    "passwordIDStore": "Internal Users",
    "link": {
      "rel": "self",
      "href": "https://<ISE-HOST>:9060/ers/config/internaluser/<user-id>",
      "type": "application/json"
    }
  }
}
```