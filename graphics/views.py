from django.shortcuts import render
from graphics.main import project_status



def index(request):
    context = None
    
    if request.method == 'POST':
        search_field = request.POST.get('search_field', '')
        fig = project_status(search_field)

        context = {
            'fig': fig.to_json(),
            'search_field': search_field
        }

    return render(request, 'graphics/index.html', context)


   