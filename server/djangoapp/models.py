from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object

class CarMake(models.Model):
    make_name = models.CharField(null=False, max_length=20)
    description = models.CharField(null=True, max_length=500)

    def __str__(self):
        return "Name: " + self.make_name + ", " \
               "Description: " + self.description

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object

class CarModel(models.Model):
    model_name = models.CharField(max_length=20)
    dealer_id = models.IntegerField()
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)

    SEDAN = 'sedan'
    SUV = 'suv'
    COUPE = 'coupe'
    TRUCK = 'truck'
    VAN = 'van'
    CAR_TYPES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (COUPE, 'Coupe'),
        (TRUCK, 'Truck'),
        (VAN, 'Van')
    ]
    car_type = models.CharField(max_length=5, choices=CAR_TYPES, default=SEDAN)
    year = models.DateField()

    def __str__(self):
        return "Name: " + self.model_name + ", " + \
               "Type: " + str(self.car_type) + ", " + \
               "Year: " + str(self.year)

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
