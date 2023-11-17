from random import randint
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangobackend.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from datetime import date
from djangoapp.models import CarMake, CarModel

cars = [
    {"make": "Honda", "model": "Civic", "year": 2021, "car_type": "sedan"},
    {"make": "Honda", "model": "Civic", "year": 2004, "car_type": "coupe"},
    {"make": "Tesla", "model": "speedster", "year": 2023, "car_type":"sedan"},
    {"make": "Tesla", "model": "model X", "year": 2022, "car_type": "sedan"},
    {"make": "Tesla", "model": "model S", "year": 2022, "car_type": "sedan"},
    {"make": "Honda", "model": "Accord", "year": 2016, "car_type": "coupe"},
    {"make": "Honda", "model": "Pilot", "year": 2021, "car_type": "suv"},
]

def write():
    for dealer_id in range(4,21):
        for i in range(5):
            car = cars[randint(0,6)]
            car_make = CarMake(make_name=car["make"])
            car_make.save()
            car_model = CarModel(model_name=car["model"], year=date(car["year"], 5, 5), car_type=car["car_type"], dealer_id=dealer_id)
            car_model.car_make = car_make
            car_model.save()
    print("Car models saved")

if __name__ == "__main__":
    write()
