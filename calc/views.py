# calc/views.py

from django.shortcuts import render, redirect
from .models import CalculationResult
from collections import Counter
import numexpr as ne

# Función principal de la calculadora
def index(request):
    context = {}
    if request.method == 'POST':
        expression = request.POST.get('expression', '')
        try:
            result = ne.evaluate(expression).item()
            context['result'] = result
            context['expression'] = expression
        except Exception as e:
            context['result'] = f"Error: {str(e)}"
    
    return render(request, 'calc/index.html', context)

# Función para guardar los resultados en la base de datos
def save_result(request):
    if request.method == 'POST':
        expression = request.POST.get('expression')
        result = request.POST.get('result')
        CalculationResult.objects.create(expression=expression, result=result)
    return redirect('/')

# Función para obtener los resultados almacenados en la base de datos
def get_results(request):
    results = CalculationResult.objects.all()
     
    operation_type = request.GET.get('operation_type')
    if operation_type == 'suma':
        results = CalculationResult.objects.filter(expression__contains='+')
    elif operation_type == 'resta':
        results = CalculationResult.objects.filter(expression__contains='-')
    elif operation_type == 'multiplicacion':
        results = CalculationResult.objects.filter(expression__contains='*')
    elif operation_type == 'division':
        results = CalculationResult.objects.filter(expression__contains='/')
    
    context = {'results': results}
    return render(request, 'calc/results.html', context)

def most_used_operation(request):
    # Obtenemos todos los resultados almacenados en la base de datos
    results = CalculationResult.objects.all()
    operations = []

    # Analizamos cada expresión para determinar qué operaciones se utilizaron
    for result in results:
        expression = result.expression
        if '+' in expression:
            operations.append('Suma (+)')
        if '-' in expression:
            operations.append('Resta (-)')
        if '*' in expression:
            operations.append('Multiplicación (*)')
        if '/' in expression:
            operations.append('División (/)')

    # Contamos cuántas veces se ha utilizado cada operación
    operation_counts = Counter(operations)

    # Ordenamos por la operación más común
    sorted_operations = operation_counts.most_common()

    # Pasamos las operaciones ordenadas a la plantilla
    context = {'sorted_operations': sorted_operations}
    return render(request, 'calc/most_used_operation.html', context)