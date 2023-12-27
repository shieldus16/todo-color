from django.forms import ValidationError
from django.shortcuts import render, redirect
from rest_framework import generics
from .models import User
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
import random
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.serializers import serialize
from django.http import HttpResponse
# def calendar(request):
#     return render(request, 'todolist/calendar.html')

@csrf_exempt
def login_api(request):
    if request.method == 'POST':
        username = request.POST.get('id')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({'success': True, 'message': '로그인 성공'})
        else:
            return JsonResponse({'success': False, 'message': '아이디 또는 비밀번호가 올바르지 않습니다.'})
    
    return JsonResponse({'success': False, 'message': 'GET 요청은 지원되지 않습니다.'})

@csrf_protect
def signup(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        password = request.POST.get('password')
        name = request.POST.get('name')
        
        # 아이디 중복 확인
        try:
            user = User.objects.get(user_id=id)
            return render(request, 'todolist/signup.html', {'error_message': '이미 존재하는 아이디입니다.'})
        except User.DoesNotExist:
            pass  # 아이디가 존재하지 않으면 계속 진행
        
        # 비밀번호 검증
        try:
            validate_password(password)
        except ValidationError as e:
            return render(request, 'todolist/signup.html', {'error_message': str(e)})
        
        # 비밀번호 DB 저장 전 해싱
        hashed_password = make_password(password)
        # 사용자 생성 및 랜덤 색상 할당
        new_user = User(user_id=id, user_password=password, user_name=name)
        new_user.user_color = generate_random_color()
        new_user.save()
        
        return redirect('login')
    
    return render(request, 'todolist/signup.html')

def generate_random_color():
    existing_colors = User.objects.values_list('user_color', flat=True)
    while True:
        # 랜덤한 색상을 #RRGGBB 형식으로 생성
        color = "#{:06x}".format(random.randint(0, 0xFFFFFF))

        # 생성한 색상이 이미 존재하는지 확인
        if color not in existing_colors:
            return color
