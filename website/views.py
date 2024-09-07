from django.shortcuts import render
import joblib
from .models import CarFormResult 
import pandas as pd
import numpy as np
from .models import CarFormResult
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.management.commands.createsuperuser import Command as CreateSuperuserCommand
from django.contrib.auth.forms import UserCreationForm

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')

    return render(request, 'login.html')

from django.shortcuts import render, redirect
from .models import SignUpForm

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')
            if password1 != password2:
                messages.error(request, "Passwords do not match.")
            else:
                form.save()
                return redirect('login')  
        else:
            messages.error(request, "Invalid form submission. Please correct the errors.")
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})



def home(request):
    return render(request, 'home.html', {})

def about(request):
    return render(request, 'about.html', {})

def upload(request):
    return render(request, 'upload.html', {})

from django.shortcuts import render
from .models import UploadedFormData

def buy(request):
    uploaded_forms = UploadedFormData.objects.all()
    return render(request, 'buy.html', {'uploaded_forms': uploaded_forms})


def contact(request):
    return render(request, 'contact.html', {})


def result(request):
    if request.method == 'GET':
        # Get values from the form
        fuel_type = request.GET.get('fuelType', 'Diesel')
        transmission = request.GET.get('transmission', 'Manual')
        owner_type = request.GET.get('ownerType', 'First')
        mileage = float(request.GET.get('mileage', 19.67))
        engine = float(request.GET.get('engine', 1582))
        power = float(request.GET.get('power', 126.2))
        seats = float(request.GET.get('seats', 5))
        name = request.GET.get('name', 'Hyundai')
        location = request.GET.get('location', 'Pune')
        year = int(request.GET.get('year', 2015))
        kilometers_driven = int(request.GET.get('kilometersDriven', 41000))

        # Mapping of options to numerical labels
        fuel_type_mapping = {'Diesel': 0, 'Petrol': 1, 'Electric': 2}
        transmission_mapping = {'Manual': 0, 'Automatic': 1}
        owner_type_mapping = {'First': 0, 'Second': 1, 'Third': 2, 'Fourth & Above': 3}
        name_mapping = {'Ambassador': 0, 'Audi': 1, 'Bentley': 2, 'BMW': 3, 'Chevrolet': 4, 'Datsun': 5,
                        'Fiat': 6, 'Force': 7, 'Ford': 8, 'Honda': 9, 'Hyundai': 10, 'Isuzu': 11,
                        'Jaguar': 12, 'Jeep': 13, 'Lamborghini': 14, 'Land': 15, 'Mahindra': 16,
                        'Maruti': 17, 'Mercedes-Benz': 18, 'Mini': 19, 'Mitsubishi': 20, 'Nissan': 21,
                        'Porsche': 22, 'Renault': 23, 'Skoda': 24, 'Tata': 25, 'Toyota': 26,
                        'Volkswagen': 27, 'Volvo': 28}
        location_mapping = {'Pune': 0, 'Chennai': 1, 'Coimbatore': 2, 'Jaipur': 3, 'Mumbai': 4,
                            'Kochi': 5, 'Kolkata': 6, 'Delhi': 7, 'Bangalore': 8, 'Hyderabad': 9,
                            'Ahmedabad': 10}

        # Encode values using the mappings
        fuel_type_encoded = fuel_type_mapping.get(fuel_type, 0)
        transmission_encoded = transmission_mapping.get(transmission, 0)
        owner_type_encoded = owner_type_mapping.get(owner_type, 0)
        name_encoded = name_mapping.get(name, 0)
        location_encoded = location_mapping.get(location, 0)

        # Prepare data for prediction
        data = {'Name': [name_encoded], 'Location': [location_encoded], 'Year': [year],
                'Kilometers_Driven': [kilometers_driven], 'Fuel_Type': [fuel_type_encoded],
                'Transmission': [transmission_encoded], 'Owner_Type': [owner_type_encoded],
                'Mileage(KM)': [mileage], 'Engine(CC)': [engine], 'Power(bhp)': [power],
                'Seats': [seats]}
        input_data = pd.DataFrame(data)

        # Load the trained machine learning model
        cls = joblib.load("ada_model.sav")

        # Make predictions using the loaded model
        predicted_price = cls.predict(input_data)

        # Save the entered values to MySQL
        CarFormResult.objects.create(
            fuel_type=fuel_type,
            transmission=transmission,
            owner_type=owner_type,
            mileage=mileage,
            engine=engine,
            power=power,
            seats=seats,
            name=name,
            location=location,
            year=year,
            kilometers_driven=kilometers_driven,
            predicted_price=predicted_price[0],
        )

        # Pass the values and predicted price to the template
        return render(request, "result.html", {'fuel_type': fuel_type, 'transmission': transmission,
                                                'owner_type': owner_type,'mileage': mileage, 
                                                'engine': engine, 'power': power, 'seats': seats,
                                                'name': name, 'location': location, 'year': year,
                                                'kilometers_driven': kilometers_driven,
                                                'predicted_price': predicted_price})
    
    else:
        # Handle other HTTP methods if needed
        return render(request, "result.html", {'error': 'Invalid HTTP method'})

# views.py

from django.shortcuts import render, redirect
from .models import UploadedFormData

def upload(request):
    return render(request, 'upload.html',{})

def upload_result(request):
    if request.method == 'POST':
        # Retrieve data from the request
        full_name = request.POST.get('fullName')
        email = request.POST.get('email')
        mobile_number = request.POST.get('mobileNumber')
        car_model = request.POST.get('carModel')
        car_year = request.POST.get('carYear')
        mileage = request.POST.get('mileage')
        kilometers_driven = request.POST.get('kilometersDriven')

        # Save the data to the database
        uploaded_data = UploadedFormData.objects.create(
            full_name=full_name,
            email=email,
            mobile_number=mobile_number,
            car_model=car_model,
            car_year=car_year,
            mileage=mileage,
            kilometers_driven=kilometers_driven,
            # Add more fields as needed
        )

        return render(request, 'upload_result.html', {
            'full_name': full_name,
            'email': email,
            'mobile_number': mobile_number,
            'car_model': car_model,
            'car_year': car_year,
            'mileage': mileage,
            'kilometers_driven': kilometers_driven,
            'person_image': uploaded_data.person_image,
            'car_image': uploaded_data.car_image,
        })

    return redirect('upload')  # Redirect to upload if not a POST request

