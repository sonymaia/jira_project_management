from django.shortcuts import render, redirect
from users.forms import LoginForms
from django.contrib import auth
from django.contrib import messages
#from django.contrib.auth.models import User

def login(request):
    form = LoginForms()

    if request.method == 'POST':
        form = LoginForms(request.POST)

        if form.is_valid():
            name = form['login'].value()
            password = form['password'].value()

        userAut = auth.authenticate(
            request,
            username=name,
            password=password
        )
        if userAut is not None:
            auth.login(request, userAut)
            #messages.success(request, f'{nome} logado com sucesso!')
            return redirect('/')
        else:
            messages.error(request, 'Erro ao efetuar login')

    return render(request, 'users/login.html', {'form': form})

def logout(request):
    auth.logout(request)
    messages.success(request, 'Logout efetuado com sucesso!')
    return redirect('login')



