from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages

def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_superuser:
            login(request, user)
            return HttpResponse('''<h1>Login Success</h1>''')
        else:
            messages.error(request, 'Invalid login credentials or not a superuser.')

    return render(request, 'login.html')
