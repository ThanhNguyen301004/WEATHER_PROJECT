from django.shortcuts import render, redirect, get_object_or_404
import requests
from geopy.geocoders import Nominatim
import pickle
import numpy as np
from scipy.stats import linregress
from datetime import datetime, timedelta
from datetime import date
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Document
from .forms import DocumentForm

with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

def temperature_trend(temperatures):
    hours = np.arange(len(temperatures))
    slope, intercept, r_value, p_value, std_err = linregress(hours, temperatures)
    
    if slope > 0.1:  trend = "increase"
    elif slope < -0.1: trend = "diminish"
    else: trend = "stable"
    
    max_temp = max(temperatures)
    min_temp = min(temperatures)
    min_temp_index = temperatures.index(min_temp)
    max_temp_index = temperatures.index(max_temp)
    
    return trend, max_temp, min_temp, max_temp_index, min_temp_index


def feelslike_deltail(weather_data):
    feelslike = weather_data['feelslike']
    temperature = weather_data['temperature']
    dif =  feelslike - temperature

    if dif > 4:  ans = "Warm"
    elif dif > 1: ans = "Warmth"
    elif dif > -1: ans = "Normal"
    elif dif > -4: ans = "Slightly Cold"
    else: ans = "Cold"

    return ans, feelslike


def umbrella_recommendation(weather_data):
    precipitation = weather_data['precipitation']
    condition = weather_data['condition']

    if precipitation > 10 or 'rain' in condition or 'shower' in condition: return "Phải"
    elif precipitation > 5: return "Cần"
    elif precipitation > 2: return "Có khả năng cần thiết"
    elif precipitation > 0: return "Có khả năng không cần"
    else: return "Không cần"

def outdoor_activity_advice(weather_data):
    uv_index = weather_data['uv']
    wind_speed = weather_data['wind']
    temperature = weather_data['temperature']
    precipitation = weather_data['precipitation'] # Giả sử chỉ số chất lượng không khí theo US EPA

    # Đánh giá từng yếu tố
    if uv_index > 8:  uv_advice = "Rất tệ"
    elif uv_index > 6: uv_advice = "Kém"
    elif uv_index > 3:  uv_advice = "Khá tốt"
    else: uv_advice = "Tốt"

    if wind_speed > 40: wind_advice = "Rất tệ"
    elif wind_speed > 20: wind_advice = "Kém"
    elif wind_speed > 10:  wind_advice = "Khá tốt"
    else:  wind_advice = "Tốt"

    if temperature > 35 or temperature < 0:  temp_advice = "Rất tệ"
    elif temperature > 30 or temperature < 10:  temp_advice = "Kém"
    elif temperature > 25 or temperature < 15:  temp_advice = "Khá tốt"
    else: temp_advice = "Tốt"

    if precipitation > 10:  precip_advice = "Rất tệ"
    elif precipitation > 5: precip_advice = "Kém"
    elif precipitation > 2: precip_advice = "Khá tốt"
    else:  precip_advice = "Tốt"

    # Tổng hợp đánh giá
    advices = [uv_advice, wind_advice, temp_advice, precip_advice]
    if "Rất tệ" in advices: overall_advice = "Rất tệ"
    elif "Kém" in advices: overall_advice = "Kém"
    elif "Khá tốt" in advices: overall_advice = "Khá tốt"
    elif "Tốt" in advices:  overall_advice = "Tốt"
    else: overall_advice = "Tuyệt vời"

    return overall_advice

def danhgiaUV(weather_data):
    uv_index = weather_data['uv']
    if uv_index <= 2: return "Thấp"
    elif uv_index <=5: return "Bình thường"
    elif uv_index <= 7: return "Cao"
    elif uv_index <= 10: return "Rất cao"
    else:  return "Tột độ"
    
def driving_safety_index(weather_data):
    temperature = weather_data['temperature']
    wind_speed = weather_data['wind']
    precipitation = weather_data['precipitation']
    humidity = weather_data['humidity']
    uv_index = weather_data['uv']

    # Đánh giá từng yếu tố
    if temperature < 0 or temperature > 35: temp_advice = "Rất tệ"
    elif temperature < 10 or temperature > 30: temp_advice = "Kém"
    elif temperature < 15 or temperature > 25: temp_advice = "Khá tốt"
    else: temp_advice = "Tốt"

    if wind_speed > 40: wind_advice = "Rất tệ"
    elif wind_speed > 30:  wind_advice = "Kém"
    elif wind_speed > 20: wind_advice = "Khá tốt"
    else: wind_advice = "Tốt"

    if precipitation > 10: precip_advice = "Rất tệ"
    elif precipitation > 5: precip_advice = "Kém"
    elif precipitation > 2: precip_advice = "Khá tốt"
    else: precip_advice = "Tốt"

    if humidity > 90: humidity_advice = "Rất tệ"
    elif humidity > 80: humidity_advice = "Kém"
    elif humidity > 70: humidity_advice = "Khá tốt"
    else: humidity_advice = "Tốt"

    if uv_index > 8: uv_advice = "Rất tệ"
    elif uv_index > 6: uv_advice = "Kém"
    elif uv_index > 3: uv_advice = "Khá tốt"
    else: uv_advice = "Tốt"

    # Tổng hợp đánh giá
    advices = [temp_advice, wind_advice, precip_advice, humidity_advice, uv_advice]
    if "Rất tệ" in advices:  overall_advice = "Rất tệ"
    elif "Kém" in advices: overall_advice = "Kém"
    elif "Khá tốt" in advices: overall_advice = "Khá tốt"
    elif "Tốt" in advices: overall_advice = "Tốt"
    else: overall_advice = "Tuyệt vời"

    return overall_advice

def clothing_recommendation(weather_data):
    temperature = weather_data['temperature']
    wind_speed = weather_data['wind']
    precipitation = weather_data['precipitation']
    humidity = weather_data['humidity']

    # Đánh giá từng yếu tố
    if temperature < 10: temp_advice = "Áo khoác dày"
    elif temperature < 20: temp_advice = "Áo khoác nhẹ"
    elif temperature < 25: temp_advice = "Áo dài tay"
    elif temperature < 30: temp_advice = "Quần áo thoáng khí"
    else: temp_advice = "Quần đùi"

    if wind_speed > 30: wind_advice = "Áo khoác dày"
    elif wind_speed > 20:  wind_advice = "Áo khoác nhẹ"
    elif wind_speed > 10: wind_advice = "Áo dài tay"
    else:  wind_advice = "Quần áo thoáng khí"

    if precipitation > 5: precip_advice = "Áo khoác dày"
    elif precipitation > 2: precip_advice = "Áo khoác nhẹ"
    else: precip_advice = "Quần áo thoáng khí"

    if humidity > 80: humidity_advice = "Quần áo thoáng khí"
    else:  humidity_advice = "Quần đùi"

    # Tổng hợp đánh giá
    advices = [temp_advice, wind_advice, precip_advice, humidity_advice]
    if "Áo khoác dày" in advices: overall_advice = "Áo khoác dày"
    elif "Áo khoác nhẹ" in advices: overall_advice = "Áo khoác nhẹ"
    elif "Áo dài tay" in advices: overall_advice = "Áo dài tay"
    elif "Quần áo thoáng khí" in advices: overall_advice = "Quần áo thoáng khí"
    else: overall_advice = "Quần đùi"

    return overall_advice

def heat_index_advice(weather_data):
    temperature = weather_data['temperature']
    humidity = weather_data['humidity']

    # Tính toán chỉ số nhiệt (Heat Index)
    heat_index = temperature + 0.33 * humidity - 0.7

    # Đánh giá chỉ số nhiệt
    if heat_index >= 54: advice = "Cực kỳ nguy hiểm"
    elif heat_index >= 41: advice = "Nguy hiểm"
    elif heat_index >= 32: advice = "Hết sức thận trọng"
    elif heat_index >= 27: advice = "Thận trọng"
    else: advice = "An toàn"

    return advice


def index(request):
    api_key = '68571164b61e4eaca1d42437240609'
    current_weather_url = 'http://api.weatherapi.com/v1/current.json?key={}&q={}&aqi=no'
    forecast_url = 'http://api.weatherapi.com/v1/forecast.json?key={}&q={}&days=3&aqi=no&alerts=no'
    error_message = None
    if request.method == 'POST':

        if 'predict_btn' in request.POST:
            precipitation = float(request.POST.get('precipitation', 0))
            temp_max = float(request.POST.get('temp_max', 0))
            temp_min = float(request.POST.get('temp_min', 0))
            wind = float(request.POST.get('wind', 0))
            features = np.array([[precipitation, temp_max, temp_min, wind]])
            prediction = model.predict(features)

            return render(request, 'weather_app/index.html', {'prediction_text': prediction[0]})

        elif 'search_btn' in request.POST:
            city = request.POST.get('city', '').strip()
            if not city:
                error_message = 'Please enter the name of the city.'
            else:
                try:
                    weather_data, daily_forecasts, cur = fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url)
                    temperatures, times = get_data(city, api_key, forecast_url)

                    geolocator= Nominatim(user_agent="your_app_name")
                    location= geolocator.geocode(city)

                    latitude = location.latitude
                    longitude = location.longitude

                    temp_del, max_temp, min_temp, max_temp_index, min_temp_index = temperature_trend(temperatures[cur:])   
                    cur_temp = temperatures[cur]
                    min_temp_index += cur
                    max_temp_index += cur

                    feel_del, feel_temp = feelslike_deltail(weather_data)   

                    umbrella_rec = umbrella_recommendation(weather_data)
                    outdoor_act_adv = outdoor_activity_advice(weather_data)
                    danh_gia_UV = danhgiaUV(weather_data)
                    dri_saf_index = driving_safety_index(weather_data)
                    clo_recommendation = clothing_recommendation(weather_data)
                    heat_index_adv = heat_index_advice(weather_data)

                    context = {
                        'weather_data': weather_data,
                        'daily_forecasts': daily_forecasts,
                        'temperatures': temperatures,
                        'times': times,
                        'latitude': latitude,  
                        'longitude': longitude,
                        'temp_del': temp_del,
                        'max_temp': max_temp,
                        'min_temp': min_temp,
                        'cur_temp': cur_temp,
                        'max_temp_index': max_temp_index,
                        'min_temp_index': min_temp_index,
                        'feel_del': feel_del,
                        'feel_temp': feel_temp,
                        'umbrella_rec': umbrella_rec,
                        'outdoor_act_adv': outdoor_act_adv,
                        'danh_gia_UV': danh_gia_UV,
                        'dri_saf_index': dri_saf_index,
                        'clo_recommendation': clo_recommendation,
                        'heat_index_adv': heat_index_adv,
                    }
                    return render(request, 'weather_app/index.html', context)
                except Exception as e:
                    error_message = e
        elif 'send_btn' in request.POST:
            print(request.POST.get('weather'))
            
        if error_message == None:
            return render(request, 'weather_app/index.html')

    return render(request, 'weather_app/index.html', {'error_message': error_message})

def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url):
    response = requests.get(current_weather_url.format(api_key, city)).json()
    forecast_response = requests.get(forecast_url.format(api_key, city)).json()

    weather_data = {
        'city': city,
        'temperature': round(response['current']['temp_c'], 1),
        'description': response['current']['condition']['text'],
        'icon': response['current']['condition']['icon'],
        'wind': response['current']['wind_kph'],
        'humidity': response['current']['humidity'],
        'vis': response['current']['vis_km'],
        'pressure': response['current']['pressure_mb'],
        'dewpoint': response['current']['dewpoint_c'],
        'feelslike': response['current']['feelslike_c'],
        'precipitation': response['current']['precip_mm'],
        'condition' : response['current']['condition']['text'].lower(),
        'uv': response['current']['uv']
    }

    daily_forecasts = []
    for daily_data in forecast_response['forecast']['forecastday'][:3]:
        daily_forecasts.append({
            'day': datetime.fromtimestamp(daily_data['date_epoch']).strftime('%A'),
            'min_temp': round(daily_data['day']['mintemp_c'], 1),
            'max_temp': round(daily_data['day']['maxtemp_c'], 1),
            'description': daily_data['day']['condition']['text'],
            'icon': daily_data['day']['condition']['icon'],
        })
    
    last_updated = response['current']['last_updated']
    
    return weather_data, daily_forecasts, int(last_updated[-5:-3])

def get_data(city, api_key, forecast_url):
    data = requests.get(forecast_url.format(api_key, city)).json()

    forecast_hours = data['forecast']['forecastday'][0]['hour']
    temperatures = [hour['temp_c'] for hour in forecast_hours]
    times = [hour['time'][-5:] for hour in forecast_hours]

    return temperatures, times


from .forms import UserRegisterForm  

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.email = form.cleaned_data['email']
            user.save()
            messages.success(request, "Đăng ký thành công!")
            return redirect('login')  # Thay đổi theo tên URL của trang đăng nhập
    else:
        form = UserRegisterForm()
    return render(request, 'weather_app/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=username, email=email, password=password)
        if user is not None:
            login(request, user)
            # messages.success(request, "Đăng nhập thành công!")
            return redirect('index')  # Chuyển hướng tới home_page
        else:
            messages.error(request, "Thông tin đăng nhập không đúng.")
    return render(request, 'weather_app/login.html')

def user_logout(request):
    logout(request)
    messages.success(request, "Đăng xuất thành công!")
    return redirect('login')

def redirect_to_login(request):
    if request.user.is_authenticated:
        return redirect('index') 
    return redirect('login')


# @login_required
def user_list(request):
    users = User.objects.all()
    return render(request, 'weather_app/user_list.html', {'users': users})

# @login_required
def user_add(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "User created successfully!")
            return redirect('user_list')
    else:
        form = UserRegisterForm()
    return render(request, 'weather_app/user_form.html', {'form': form})

# @login_required
def user_edit(request, id):
    user = get_object_or_404(User, id=id)
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            if 'password' in form.cleaned_data:
                user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "User updated successfully!")
            return redirect('user_list')
    else:
        form = UserRegisterForm(instance=user)
    return render(request, 'weather_app/user_form.html', {'form': form})

# @login_required
def user_delete(request, id):
    user = get_object_or_404(User, id=id)
    user.delete()
    messages.success(request, "User deleted successfully!")
    return redirect('user_list')


def khihau(request):
    documents = Document.objects.all()
    return render(request, 'weather_app/khihau.html', {'documents': documents})

def chitietkhihau(request, id):
    document = get_object_or_404(Document, id=id)
    return render(request, 'weather_app/chitietkhihau.html', {'document': document})

def display_pdf(request, id):
    document = get_object_or_404(Document, id=id)
    return render(request, 'weather_app/display_pdf.html', {'document': document})

def home_page(request):
    return render(request, 'weather_app/index.html') 




def document_list(request):
    documents = Document.objects.all()
    return render(request, 'weather_app/document_list.html', {'documents': documents})


def add_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('document_list')  # Redirect to a list view or a success page
    else:
        form = DocumentForm()
    return render(request, 'weather_app/add_document.html', {'form': form})

def update_document(request, id):
    document = get_object_or_404(Document, id=id)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            form.save()
            return redirect('document_detail', id=document.id)  # Redirect to a detail view or a success page
    else:
        form = DocumentForm(instance=document)
    return render(request, 'weather_app/update_document.html', {'form': form, 'document': document})

def delete_document(request, id):
    document = get_object_or_404(Document, id=id)
    if request.method == 'POST':
        document.delete()
        return redirect('document_list')  # Redirect to a list view or a success page
    return render(request, 'weather_app/delete_document.html', {'document': document})



