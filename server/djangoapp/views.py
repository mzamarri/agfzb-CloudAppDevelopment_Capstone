from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import get_dealers_from_cf, get_dealer_by_id_from_cf, get_dealer_by_state_from_cf, \
                      get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from .models import CarMake, CarModel

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    return render(request, 'djangoapp/about.html')


# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, 'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == 'POST':
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, login the user with login method
            login(request, user)
            return redirect('djangoapp:index')
        else:
            # If user is not valid, return to login page again
            return render(request, 'djangoapp:index', context)
    else:
        return render(request, 'djangoapp:index', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    # If GET request, render the registration page
    if request.method == "GET":
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == "POST":
        # Get registration information. Username, Password, First Name and Last Name
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, password=password, 
                                            first_name=first_name, last_name=last_name)
            login(request, user)
            return redirect('djangoapp:index')
        else:
            return render(request, 'djangoapp:registration', context)
  
# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = dict()
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/e336f8e9-8c1c-4218-b880-1680d9a739fc/dealership-package/get-dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        print("Dealership ID: ", dealerships[0])
        print("Dealership ID end")
        context["dealership_list"] = dealerships
        print(context)
        # Return a list of dealer short name
        return render(request, 'djangoapp/index.html', context)

# Create `get_dealer_by_id` to get dealer with a particular id
def get_dealer_by_id(request, dealer_id):
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/e336f8e9-8c1c-4218-b880-1680d9a739fc/dealership-package/get-dealership"
        dealership = get_dealer_by_id_from_cf(url, dealer_id)
        dealer_name = dealership.short_name
        return HttpResponse(dealer_name)

# Create a `get_dealer_details_by_state` view to render the reviews of a dealer in particular state
def get_dealers_by_state(request, state):
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/e336f8e9-8c1c-4218-b880-1680d9a739fc/dealership-package/get-dealership"
        dealership_from_state = get_dealer_by_state_from_cf(url, state)
        print("Dealership by state:")
        print(dealership_from_state[0])
        dealer_names = ' '.join([dealer.short_name for dealer in dealership_from_state])
        return HttpResponse(dealer_names)

# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
def get_dealer_details(request, dealer_id):
    context = dict()
    print("Dealer ID: ", dealer_id)
    if request.method == "GET":
        dealer_url = "https://us-south.functions.appdomain.cloud/api/v1/web/e336f8e9-8c1c-4218-b880-1680d9a739fc/dealership-package/get-dealership"
        dealer = get_dealer_by_id_from_cf(dealer_url, dealer_id)
        context["dealer"] = dealer
        print("Dealer: ", context["dealer"])
        review_url = "https://us-south.functions.appdomain.cloud/api/v1/web/e336f8e9-8c1c-4218-b880-1680d9a739fc/dealership-package/get-review"
        reviews = get_dealer_reviews_from_cf(review_url, dealer_id)
        context["reviews"] = reviews
        context["dealer_id"] = dealer_id
        print("Test Point 1")
        print("Context: ", context)
        # review_content = ' '.join(dealer.sentiment for dealer in dealer_reviews)
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
def add_review(request, dealer_id):
    # if request.user.is_authenticated:
    print("TP 1")
    print({"request method": request.method})
    context = dict()
    dealer_url = "https://us-south.functions.appdomain.cloud/api/v1/web/e336f8e9-8c1c-4218-b880-1680d9a739fc/dealership-package/get-dealership"
    dealer = get_dealer_by_id_from_cf(dealer_url, dealer_id)
    context["dealer"] = dealer
    # print("Request: ", request)
    if request.method == "GET":
        context["cars"] = CarModel.objects.filter(dealer_id=dealer_id)
        print("Cars context: ", context["cars"])
        print("Car objects id: ", context["cars"][6].id)
        context["dealer_id"] = dealer_id
        return render(request, 'djangoapp/add_review.html', context)
    elif request.method == "POST":
        print("TP 2")
        print("Request POST: ",request.POST) 
        review_url = "https://us-south.functions.appdomain.cloud/api/v1/web/e336f8e9-8c1c-4218-b880-1680d9a739fc/dealership-package/post-review"
        car_id = request.POST["car"]
        purchase_check = False
        if "purchase_check" in request.POST:
            if request.POST["purchase_check"] == 'on':
                purchase_check = True
        car = CarModel.objects.get(id=car_id)
        review = {
            "time": datetime.utcnow().isoformat(),
            "name": request.user.username,
            "dealership": dealer_id,
            "review": request.POST['review'],
            "purchase": purchase_check,
            "purchase_date": request.POST['purchase_date'],
            "car_make": car.car_make.make_name,
            "car_model": car.model_name,
            "car_year": str(car.year.strftime("%Y")) 
        }
        json_payload = {"review": review}
        print("Test 1")
        response = post_request(review_url, json_payload=json_payload)
        print("Test 2") 
        print("Response: ", response)
        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)


