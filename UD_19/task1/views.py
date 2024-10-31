from django.shortcuts import render
from django.shortcuts import HttpResponse
from .forms import UserRegister


# Create your views here.
def platform(request):
    return render(request, 'platform.html')

def games(request):
    scroll = {'games': ['Atomic Heart ', 'Cyberpunk 2077 ', 'PayDay 2 ']}
    context = {'scroll': scroll,}
    return render(request, 'games.html', context)
def cart(request):
    return render(request, 'cart.html')

def sign_up(request):
    users = ['Ivan92', 'jonnaZ', 'Masha_K', 'LOTR',]
    info = {}
    if request.method == 'POST':
        user_exist = False
        form = UserRegister(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            repeat_password = form.cleaned_data['repeat_password']
            age = int(form.cleaned_data['age'])

            is_user = username in users
            if password == repeat_password:
                if age >= 18:
                    if is_user == False:
                        user_exist = True
                    else:
                        info['error'] = 'Пользователь уже существует'
                else:
                    info['error'] = 'Вы должны быть старше 18'
            else:
                info['error'] = 'Пароли не совпадают'
            if user_exist:
                message = (f"Приветствуем, {username}")
                print(message)
            else:
                message = info['error']
            return HttpResponse(message)
        return render(request, 'registration_page.html', info)
    else:
        form = UserRegister()
    return render(request, 'registration_page.html', info)
