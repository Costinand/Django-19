from django.shortcuts import render
from django.shortcuts import HttpResponse
from .forms import UserRegister
from task1.models import Buyer, Game


# Create your views here.
def platform(request):
    return render(request, 'platform.html')

def games(request):
    # scroll = {'games': ['Atomic Heart ', 'Cyberpunk 2077 ', 'PayDay 2 ']}
    games = Game.objects.all()
    context = {'games': games}
    return render(request, 'games.html', context)
def cart(request):
    return render(request, 'cart.html')

def sign_up(request):
    name_users = []  # список имен пользователей
    users = Buyer.objects.all() # список объектов из таблицы покупателей
    for user in users: # перебор объектов
        name_users.append(user.name) # в список покупателей достаются только имена объектов
    # print(name_users) # для наглядности вывод на терминале
    info = {}
    if request.method == 'POST':
        user_exist = False # по умолчанию новый пользователь не присутствует
        form = UserRegister(request.POST)
        if form.is_valid():   # если форма запроса заполнена
            username = form.cleaned_data['username'] # сбор каждого поля для обработки
            password = form.cleaned_data['password']
            repeat_password = form.cleaned_data['repeat_password']
            age = int(form.cleaned_data['age'])

            is_user = username in name_users  # пользователь - это кто-то среди имен пользователей
            if password == repeat_password:   # если пароли совпадают
                if age >= 18:                 # и если возраст соответстует
                    if is_user == False:     #  и если нету (34) то его присутсятвие меняется на положительное (26)
                        user_exist = True
                    else:
                        info['error'] = 'Пользователь уже существует'
                else:
                    info['error'] = 'Вы должны быть старше 18'
            else:
                info['error'] = 'Пароли не совпадают'
            if user_exist:             # итак он имеет право присутствовать в пользователях(37)
                message = (f"Приветствуем, {username}")
                Buyer.objects.create(name=username, balance=0, age=age)  # добавление в базу
                print(message)
            else:
                message = info['error']
            return HttpResponse(message)
        return render(request, 'registration_page.html', info)
    else:
        form = UserRegister()
    return render(request, 'registration_page.html', info)

