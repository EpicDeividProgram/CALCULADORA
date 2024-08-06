

from django.shortcuts import render
import numexpr as ne

def index(request):
    context = {}
    if request.method == 'POST':
        expression = request.POST.get('expression', '')
        try:
            # Evaluar la expresión de manera segura
            result = ne.evaluate(expression).item()
            context['result'] = result
        except Exception as e:
            context['result'] = f"Error: {str(e)}"
    
    return render(request, 'calc/index.html', context)
