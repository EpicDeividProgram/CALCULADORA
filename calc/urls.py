
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('save/', views.save_result, name='save_result'),
    path('results/', views.get_results, name='get_results'),
    path('most-used-operation/', views.most_used_operation, name='most_used_operation'),  # Nueva ruta para la vista de la operación más usada
]
