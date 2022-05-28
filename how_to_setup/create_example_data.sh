curl -X POST \
  http://127.0.0.1:8000/doctor/ \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/json' \
  -d '[
  {
    "doctor_translations": [
      {
        "language_code": "EN",
        "name": "new name EN 1",
        "note": "new note EN 1"
      },
      {
        "language_code": "HK",
        "name": "new name HK 1",
        "note": "new note HK 1"
      }
    ],
    "location": {
      "district": "TP",
      "latitude": "123.456",
      "longitude": "111.111",
      "name": "new loc 1"
    },
    "phone": "+852800930001",
    "category": "GP",
    "price": "100.01",
    "available_time": "available time 1"
  },
  {
    "doctor_translations": [
      {
        "language_code": "EN",
        "name": "new name EN 2",
        "note": "new note EN 2"
      },
      {
        "language_code": "HK",
        "name": "new name HK 2",
        "note": "new note HK 2"
      }
    ],
    "location": {
      "district": "WTS",
      "latitude": "222.333",
      "longitude": "333.444",
      "name": "new loc 2"
    },
    "phone": "+852800930002",
    "category": "D",
    "price": "200.02",
    "available_time": "available time 2"
  },
  {
    "doctor_translations": [
      {
        "language_code": "EN",
        "name": "new name EN 3",
        "note": "new note EN 3"
      },
      {
        "language_code": "HK",
        "name": "new name HK 3",
        "note": "new note HK 3"
      }
    ],
    "location": {
      "district": "SK",
      "latitude": "666.666",
      "longitude": "777.777",
      "name": "new loc 3"
    },
    "phone": "+852800930003",
    "category": "C",
    "price": "300.03",
    "available_time": "available time 3"
  },
  {
    "doctor_translations": [
      {
        "language_code": "EN",
        "name": "new name EN 4",
        "note": "new note EN 4"
      },
      {
        "language_code": "HK",
        "name": "new name HK 4",
        "note": "new note HK 4"
      }
    ],
    "location": {
      "district": "SSP",
      "latitude": "515.515",
      "longitude": "232.232",
      "name": "new loc 4"
    },
    "phone": "+852800930004",
    "category": "K",
    "price": "400.04",
    "available_time": "available time 4"
  },
  {
    "doctor_translations": [
      {
        "language_code": "EN",
        "name": "new name EN 5",
        "note": "new note EN 5"
      },
      {
        "language_code": "HK",
        "name": "new name HK 5",
        "note": "new note HK 5"
      }
    ],
    "location": {
      "district": "TM",
      "latitude": "888.888",
      "longitude": "999.999",
      "name": "new loc 5"
    },
    "phone": "+852800930005",
    "category": "F",
    "price": "500.05",
    "available_time": "available time 5"
  }
]'
