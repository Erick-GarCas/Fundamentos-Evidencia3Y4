from django.urls import path
from . import views

urlpatterns = [
	path('', views.listar_contactos, name='listar'),
	path('crear/', views.crear_contacto, name='crear'),
	path('editar/<int:id>/', views.editar_contacto, name='editar'),
	path('eliminar/<int:id>/', views.eliminar_contacto, name='eliminar'),
]

