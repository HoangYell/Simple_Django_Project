# Simple_Django_Project

_a Django boilerplate with Pre-commit, DRF serializer, Pytest, and Github action_

<div id="header" align="center">
  <img src="https://media.giphy.com/media/iVS4wrp1XT3BqUAQjo/giphy.gif" width="100"/>
</div>

* * *

## A. Tech Stacks:

- [**Python:**](https://www.python.org/)
No need to say more, Python is a trend and It will be good for any backend web project
![python ranking 2022](https://user-images.githubusercontent.com/7069077/170808297-3c538fcb-8fdd-41b3-97f5-916e4c4a0393.png)

- [**Django:**](https://www.djangoproject.com/)
Django is one of the most powerful frameworks for any python web project using it to handle this task is a bit abusive. But it's still good to use it
  - _Question:_ Why don't you use Flask?
  - _Answer:_ Yes, Flask is also a good alternative. Let's go over some aspects:
    - _Time spent and ease of use:_ Flask might be easier because of its simplicity, but I know Django well.`Django = Flask`
    - _Library Support, Plugin Apps, Built-in Features, Security:_ Of course, `Django > Flask`
    - _Popularity, Community support, Job opportunities:_ Django > Flask. Nope, not really! `Django = Flask`
      [![Python Servey](https://user-images.githubusercontent.com/7069077/170833793-24a26aab-b365-4669-8dd0-3975b6337be9.png)](https://www.jetbrains.com/lp/devecosystem-2021/python/).
    - _Performance:_ Flask is smaller and has fewer layers so it's faster, but Django is more efficient in complex features. `Django = Flask`
    - _Summary:_ I believe both Django and Flask are fully capable of handling this task. Flask seems more native and can change the architecture flexibly. But Django makes me more confident about doing this task in a short time.

- [**DRF:**](https://www.django-rest-framework.org/)
In this project, we need it for serialization and API routing

- [**Pre-commit:**](https://pre-commit.com/ )
A good code cleaner, we can apply many lint rules to it. It will help to check and auto-format code when we commit code

- [**PyTest:**](https://docs.pytest.org/en/7.1.x/)
A well-known unit test framework for Python projects with rich external plugins

- [**Github Action:**](https://github.com/actions/setup-python/)
Automate all workflows with built-in CI/CD. Build, test, and deploy code right from GitHub.
We can use this to run Pytest, check test coverage

***
## B. Setup TL;DR

- _simple_setup.sh_
  - `git clone git@github.com:ngohoangyell/Simple_Django_Project.git`
  - `cd Simple_Django_Project`
  - `python3 -m venv hybeta_env`
  - `source hybeta_env/bin/activate`

  - `python3 -m pip install -r requirements.txt`
    - or `python3 -m pip install -r how_to_setup/fallback_requirements.txt`

  - `pre-commit install`
  - `pre-commit run --all-files`

  - `python manage.py migrate`

  - `pytest -s`

  - `python manage.py runserver`

- `sh how_to_setup/create_example_data.sh  `

_that's it, all done!_ 🥳

***
## C. Model

![hybeta tables](https://user-images.githubusercontent.com/7069077/170811289-f3dceb01-85b8-47dc-b9d9-fd7051edecc7.png)
- **Q&A 🤔🤷‍♀️🤷‍♂️**
  - `hybeta_doctor_translation`: not enough fields?
    - Okay, we may add more fields later.
  - `hybeta_doctor`: available_time is a text field?
    - Humm, a lot of things to handle this. The additional table is a must-have. We will update later.
  - `hybeta_location`: displaying only 1 language?
    - Hehe, we may create an additional table later.
  - Why do all tables have this `hybeta_.*` prefix?
    - We will use a lot of plugin apps in Django. The prefix will help easy to distinguish from another plugin app table.
  - Why do you use Soft Delete(`is_deleted`, `deleted_at`)?
    - DB fees are very cheap nowadays, so we should prioritize solutions that are convenient for maintenance and troubleshooting.

## D. API

**Postman collections:**
```
https://www.getpostman.com/collections/e735f5704363b0546881
```
---
### D.1. Get all doctors in any language:
**URL:** http://127.0.0.1:8000/doctor/

**cURL:**
```
curl --location --request GET 'http://127.0.0.1:8000/doctor/'
```
**Response:**
```
[
    {
        "id": 56,
        "doctor_translations": [
            {
                "id": 83,
                "language_code": "HK",
                "name": "new name HK 1",
                "note": "new note HK 1"
            },
            {
                "id": 82,
                "language_code": "EN",
                "name": "new name 1",
                "note": "new note 1"
            }
        ],
        "location": {
            "id": 44,
            "district": "TP",
            "latitude": "874.1669429",
            "longitude": "111.1669420",
            "name": "new loc 1"
        },
        "phone": "0905360911",
        "category": "D",
        "price": "123.11",
        "available_time": "available 1"
    }
]
```
---
### D.2. Get doctor by filter and sort:
_Usage:_
 - filter: `filter_{priority}__{field_name}={expected_value}`
 - sort: `sort_{priority}__{field_name}={asc/desc}`
 - advanced filter: `filter_{priority}__{field_name}__{lte/le/gte/ge/icontains}={expected_value}`

**URL:** http://127.0.0.1:8000/doctor/?filter_1__district=WTS&filter_2__category=D&filter_3__price__lte=200.02&filter_4__language_code=EN&sort_1__id=desc

**cURL:**
```
curl --location --request GET 'http://127.0.0.1:8000/doctor/?filter_1__district=WTS&filter_2__category=D&filter_3__price__lte=200.02&filter_4__language_code=EN&sort_1__id=desc'
```
**Response:**
```
[
    {
        "id": 38,
        "doctor_translations": [
            {
                "id": 53,
                "language_code": "EN",
                "name": "new name EN 2",
                "note": "new note EN 2"
            }
        ],
        "location": {
            "id": 33,
            "district": "WTS",
            "latitude": "222.3330000",
            "longitude": "333.4440000",
            "name": "new loc 2"
        },
        "phone": "+852800930002",
        "category": "D",
        "price": "200.02",
        "available_time": "available time 2"
    },
    {
        "id": 22,
        "doctor_translations": [
            {
                "id": 25,
                "language_code": "EN",
                "name": "new name EN 2",
                "note": "new note EN 2"
            }
        ],
        "location": {
            "id": 22,
            "district": "WTS",
            "latitude": "222.3330000",
            "longitude": "333.4440000",
            "name": "new loc 2"
        },
        "phone": "+852800930002",
        "category": "D",
        "price": "200.02",
        "available_time": "available time 2"
    }
]
```
---
### D.3. Get the doctor by ID & filter language:
**URL:** http://127.0.0.1:8000/doctor/1/?filter_1__language_code=HK

**cURL:**
```
curl --location --request GET 'http://127.0.0.1:8000/doctor/1/?filter_1__language_code=HK'
```
**Response:**
```
{
    "id": 1,
    "doctor_translations": [
        {
            "id": 2,
            "language_code": "HK",
            "name": "new name HK 1",
            "note": "new note HK 1"
        }
    ],
    "location": {
        "id": 1,
        "district": "TP",
        "latitude": "111.1669429",
        "longitude": "111.1669420",
        "name": "new loc 1"
    },
    "phone": "0905360911",
    "category": "D",
    "price": "123.11",
    "available_time": "available 1"
}
```
---
### D.4. Create a single doctor with an existing location
**URL:** http://127.0.0.1:8000/doctor/ or http://127.0.0.1:8000/doctor/bulk_create/

**cURL:**
```
curl --location --request POST 'http://127.0.0.1:8000/doctor/' \
--header 'Content-Type: application/json' \
--data-raw '  {
    "doctor_translations": [
      {
        "language_code": "EN",
        "name": "new name EN 6",
        "note": "new note EN 6"
      },
      {
        "language_code": "HK",
        "name": "new name HK 6",
        "note": "new note HK 6"
      }
    ],
    "location": {
      "id": 1
    },
    "phone": "+852800930005",
    "category": "F",
    "price": "500.05",
    "available_time": "available time 5"
  }'
```
**Response:**
```
{
    "id": 76,
    "doctor_translations": [
        {
            "id": 116,
            "language_code": "HK",
            "name": "new name HK 6",
            "note": "new note HK 6"
        },
        {
            "id": 115,
            "language_code": "EN",
            "name": "new name EN 6",
            "note": "new note EN 6"
        }
    ],
    "location": {
        "id": 1,
        "district": "TP",
        "latitude": "111.1669429",
        "longitude": "111.1669420",
        "name": "new loc 1"
    },
    "phone": "+852800930005",
    "category": "F",
    "price": "500.05",
    "available_time": "available time 5"
}
```
---
### D.5. Bulk create doctors with the new location
**URL:** http://127.0.0.1:8000/doctor/ or http://127.0.0.1:8000/doctor/bulk_create/

**cURL:**
```
curl --location --request POST 'http://127.0.0.1:8000/doctor/' \
--header 'Content-Type: application/json' \
--data-raw '[
    {
        "doctor_translations": [
            {
                "language_code": "EN",
                "name": "new name 1",
                "note": "new note 1"
            },
            {
                "language_code": "HK",
                "name": "new name HK 1",
                "note": "new note HK 1"
            }
        ],
        "location": {
            "district": "TP",
            "latitude": "874.1669429",
            "longitude": "111.1669420",
            "name": "new loc 1"
        },
        "phone": "0905360911",
        "category": "D",
        "price": "123.11",
        "available_time": "available 1"
    },
    {
        "doctor_translations": [
            {
                "language_code": "EN",
                "name": "new name 2",
                "note": "new note 2"
            }
        ],
        "location": {
            "district": "WTS",
            "latitude": "112.9429000",
            "longitude": "112.1942900",
            "name": "new loc 2"
        },
        "phone": "20244432322",
        "category": "K",
        "price": "32432.22",
        "available_time": "available 2"
    }
]'
```
**Response:**
```
[
    {
        "id": 74,
        "doctor_translations": [
            {
                "id": 113,
                "language_code": "HK",
                "name": "new name HK 1",
                "note": "new note HK 1"
            },
            {
                "id": 112,
                "language_code": "EN",
                "name": "new name 1",
                "note": "new note 1"
            }
        ],
        "location": {
            "id": 55,
            "district": "TP",
            "latitude": "874.1669429",
            "longitude": "111.1669420",
            "name": "new loc 1"
        },
        "phone": "0905360911",
        "category": "D",
        "price": "123.11",
        "available_time": "available 1"
    },
    {
        "id": 75,
        "doctor_translations": [
            {
                "id": 114,
                "language_code": "EN",
                "name": "new name 2",
                "note": "new note 2"
            }
        ],
        "location": {
            "id": 56,
            "district": "WTS",
            "latitude": "112.9429000",
            "longitude": "112.1942900",
            "name": "new loc 2"
        },
        "phone": "20244432322",
        "category": "K",
        "price": "32432.22",
        "available_time": "available 2"
    }
]
```

***
## E. Testing

- Test folder: [tests](https://github.com/ngohoangyell/Simple_Django_Project/tree/main/tests)

- Command: `pytest -s` or `pytest -s tests/jobs` or `pytest --cov=hybeta tests/`

- Test Database: `test_db.sqlite3`. You can update the settings in [test.py](https://github.com/ngohoangyell/Simple_Django_Project/blob/main/hybeta/settings/test.py) and [pytest.ini](https://github.com/ngohoangyell/Simple_Django_Project/blob/main/pytest.ini)

***
## F. Unfinished tasks and plans for the future

- Pagination: It must be implemented for sure!
- Django-hvad
- Django-filter
- Django-environ
- Update `hybeta_doctor.available_time`, create `hybeta_doctor.doctor_scheduled_time` to handle it.
- Expose API to retrieve doctor service(category)
- Return log_id in the response header if status_code = 500
- Check API Permission
- Validate payload
- API Throttling to prevent DDOS
- Cache model, Cache URL:
  - Clear cache when having the new update
- Bulk creates API, If we have to consume the large data:
  - Implement Queue to handle it
  - Implement Parallel Processing to decrease process time
- Accept to consume & return response in XML instead of only JSON
- Build log system(Sentry, Kibana, Datadog)
- Elasticsearch is also a nice tech to apply if we need to handle a more complex filter
