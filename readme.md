# Django Menu App
Django Rest Framework application allows keeping menus and dishes in database.

## Prerequisites
You have to have installed docker and docker-compose on your computer.

## Starting
1. Rename .env-default file to .env.
2. Type command `docker-compose up --build` in terminal in project root directory.
3. Open browser with url `http://0.0.0.0:8000` or `http://127.0.0.1:8000` on Windows.
4. Enjoy!

### Swagger:
`http://localhost:8000/swagger/`

### Endpoints:
Views depending on permissions
Public:
1. `v1/menus`  GET - allows to get list of menus
2. `v1/dishes` GET - allows to get list of dishes
3. `v1/menus/{id}` GET - allows to get information about a menu by id
4. `v1/dishes/{id}` GET  - allows to get information about a dish by id

### To use  predefined data:
`docker-compose exec web python manage.py loaddata menu`
### Admin User:
`/admin` - username `admin` password `adminpass123`

### Tests
1.API tests - type command `docker-compose exec web python manage.py test menu/tests` in terminal in project root directory.

### Coverage
Check coverage:
1. `docker-compose exec web coverage run manage.py test menu/tests`
2. `docker-compose exec coverage report`

```text
Name                                         Stmts   Miss  Cover
----------------------------------------------------------------
config/__init__.py                               0      0   100%
config/settings.py                              32      0   100%
config/urls.py                                  13      0   100%
manage.py                                       12      2    83%
menu/__init__.py                                 0      0   100%
menu/admin.py                                    4      0   100%
menu/apps.py                                     8      0   100%
menu/jobs.py                                     7      0   100%
menu/migrations/0001_initial.py                  5      0   100%
menu/migrations/0002_auto_20210419_1554.py       5      0   100%
menu/migrations/0003_alter_menu_dish.py          5      0   100%
menu/migrations/0004_alter_dish_price.py         6      0   100%
menu/migrations/0005_dish_image.py               4      0   100%
menu/migrations/0006_alter_menu_dish.py          4      0   100%
menu/migrations/0007_alter_menu_dish.py          4      0   100%
menu/migrations/__init__.py                      0      0   100%
menu/models.py                                  22      0   100%
menu/serializers.py                             12      0   100%
menu/tests/tests_models.py                      52      0   100%
menu/tests/tests_privite_views.py              197      0   100%
menu/tests/tests_public_views.py               112      0   100%
menu/tests/tests_serializers.py                 44      0   100%
menu/urls.py                                     4      0   100%
menu/utils.py                                   23     15    35%
menu/views.py                                   68      2    97%
----------------------------------------------------------------
TOTAL                                          643     19    97%

```
## Licence
```text
* ----------------------------------------------------------------------------
 * "THE BEER-WARE LICENSE" (Revision 42):
 * <expiren@gmail.com> wrote this file.  As long as you retain this notice you
 * can do whatever you want with this stuff. If we meet some day, and you think
 * this stuff is worth it, you can buy me a beer in return.  Pawel Szopa
 * ----------------------------------------------------------------------------
```

