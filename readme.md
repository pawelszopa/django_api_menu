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
`/admin` - CMS admin
`/accounts/login/` - DRF rest Login
`/accounts/registration/` -  DRF  registration
`/accounts/logout/` -  DRF  logout
`api-auth/` - login form redirect from browsable API
`api/v1/cards` allows to get list of menus
`api/v1/dishes`  allows to get list of dishes
`api/v1/cards/{id}` allows to get information about a menu by id
`api/v1/dishes/{id}` allows to get information about a dish by id

### To use  predefined data:
`docker-compose exec web python manage.py loaddata menu`

### Tests
1.API tests - type command `docker-compose exec web python manage.py test menu/tests` in terminal in project root directory.

### Coverage
Check coverage:
1. `docker-compose exec web coverage run manage.py test menu/tests`
2. `docker-compose exec web coverage report`

Name                               Stmts   Miss  Cover
------------------------------------------------------
config/__init__.py                     0      0   100%
config/settings.py                    34      0   100%
config/urls.py                        14      0   100%
manage.py                             12      2    83%
menu/__init__.py                       0      0   100%
menu/admin.py                          4      0   100%
menu/apps.py                           9      0   100%
menu/jobs.py                           7      0   100%
menu/migrations/0001_initial.py        9      0   100%
menu/migrations/__init__.py            0      0   100%
menu/models.py                        25      0   100%
menu/permissions.py                    9      0   100%
menu/serializers.py                   23      3    87%
menu/tests/tests_models.py            65      0   100%
menu/tests/tests_permissions.py      266      0   100%
menu/tests/tests_serializers.py       47      0   100%
menu/tests/tests_utilis.py            44      0   100%
menu/tests/tests_views.py             63      0   100%
menu/urls.py                           7      0   100%
menu/utils.py                         22      0   100%
menu/views.py                         25      5    80%
users/__init__.py                      0      0   100%
users/admin.py                         7      0   100%
users/apps.py                          4      0   100%
users/migrations/0001_initial.py       8      0   100%
users/migrations/__init__.py           0      0   100%
users/models.py                        3      0   100%
------------------------------------------------------
TOTAL                                707     10    99%


## Licence
```text
* ----------------------------------------------------------------------------
 * "THE BEER-WARE LICENSE" (Revision 42):
 * <expiren@gmail.com> wrote this file.  As long as you retain this notice you
 * can do whatever you want with this stuff. If we meet some day, and you think
 * this stuff is worth it, you can buy me a beer in return.  Pawel Szopa
 * ----------------------------------------------------------------------------
```

