from django.shortcuts import render, redirect
from graphics.main import project_status
from django.contrib import messages


def user_authentication(request):
    messages.error(request, 'Usuário não logado')
    return redirect('login')

def index(request):
    if not request.user.is_authenticated:
        return user_authentication(request)

    project_data = None
   
    if request.method == 'POST' and request.POST.get('search_field', ''):
        search_field = request.POST.get('search_field')
        project_data = project_status(search_field)
        
        if not isinstance(project_data, dict):
            messages.error(request, project_data)
            project_data = None
        else:
            #transform chart data into json
            project_data['fig'] = project_data['fig'].to_json()

    return render(request, 'graphics/index.html', project_data)


   