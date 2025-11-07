from django.shortcuts import render, redirect, get_object_or_404
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re
from .models import Contacto, Relacion

# Create your views here.

def listar_contactos(request):
	contactos = Contacto.objects.all()
	return render(request, 'listar.html', {'contactos': contactos})


def crear_contacto(request):
	if request.method == 'POST':
		nombre = request.POST.get('nombre', '').strip()
		primer_apellido = request.POST.get('primer_apellido', '').strip()
		segundo_apellido = request.POST.get('segundo_apellido', '').strip()
		alias = request.POST.get('alias', '').strip()
		relacion_id = request.POST.get('relacion')
		telefono = request.POST.get('telefono', '').strip()
		correo = request.POST.get('correo', '').strip()

		errors = {}
		if not nombre:
			errors['nombre'] = 'Nombre es obligatorio.'
		elif len(nombre) > 100:
			errors['nombre'] = 'Nombre demasiado largo (máx. 100).'

		if not primer_apellido:
			errors['primer_apellido'] = 'Primer apellido es obligatorio.'
		elif len(primer_apellido) > 100:
			errors['primer_apellido'] = 'Primer apellido demasiado largo (máx. 100).'

		if segundo_apellido and len(segundo_apellido) > 100:
			errors['segundo_apellido'] = 'Segundo apellido demasiado largo (máx. 100).'

		if alias and len(alias) > 100:
			errors['alias'] = 'Alias demasiado largo (máx. 100).'

		if not relacion_id:
			errors['relacion'] = 'Relación es obligatoria.'

		if not telefono:
			errors['telefono'] = 'Teléfono es obligatorio.'
		elif len(telefono) > 30:
			errors['telefono'] = 'Teléfono demasiado largo (máx. 30).'
		else:
			if not re.match(r'^[0-9+()\-\s]+$', telefono):
				errors['telefono'] = 'Teléfono contiene caracteres no permitidos.'

		if correo:
			try:
				validate_email(correo)
			except ValidationError:
				errors['correo'] = 'Correo inválido.'

		if errors:
			relaciones = Relacion.objects.all()
			phones = list(Contacto.objects.values_list('telefono', flat=True))
			emails = list(Contacto.objects.exclude(correo__isnull=True).exclude(correo__exact='').values_list('correo', flat=True))
			return render(request, 'crear.html', {'errors': errors, 'relaciones': relaciones, 'data': request.POST, 'phones': phones, 'emails': emails})

		# Comprobación de duplicados en servidor (seguridad)
		if Contacto.objects.filter(telefono=telefono).exists():
			errors['telefono'] = 'Ya existe un contacto con ese teléfono.'
		if correo:
			if Contacto.objects.filter(correo__iexact=correo).exists():
				errors['correo'] = 'Ya existe un contacto con ese correo.'
		if errors:
			relaciones = Relacion.objects.all()
			phones = list(Contacto.objects.values_list('telefono', flat=True))
			emails = list(Contacto.objects.exclude(correo__isnull=True).exclude(correo__exact='').values_list('correo', flat=True))
			return render(request, 'crear.html', {'errors': errors, 'relaciones': relaciones, 'data': request.POST, 'phones': phones, 'emails': emails})

		# Guardar en mayúsculas
		nombre = nombre.upper()
		primer_apellido = primer_apellido.upper()
		segundo_apellido = segundo_apellido.upper() if segundo_apellido else None
		alias = alias.upper() if alias else None
		correo = correo.upper() if correo else None

		relacion = get_object_or_404(Relacion, pk=relacion_id)
		Contacto.objects.create(
			nombre=nombre,
			primer_apellido=primer_apellido,
			segundo_apellido=segundo_apellido,
			alias=alias,
			relacion=relacion,
			telefono=telefono,
			correo=correo,
		)
		return redirect('listar')

	relaciones = Relacion.objects.all()
	phones = list(Contacto.objects.values_list('telefono', flat=True))
	emails = list(Contacto.objects.exclude(correo__isnull=True).exclude(correo__exact='').values_list('correo', flat=True))
	return render(request, 'crear.html', {'relaciones': relaciones, 'phones': phones, 'emails': emails})


def editar_contacto(request, id):
	contacto = get_object_or_404(Contacto, pk=id)
	if request.method == 'POST':
		nombre = request.POST.get('nombre', '').strip()
		primer_apellido = request.POST.get('primer_apellido', '').strip()
		segundo_apellido = request.POST.get('segundo_apellido', '').strip()
		alias = request.POST.get('alias', '').strip()
		relacion_id = request.POST.get('relacion')
		telefono = request.POST.get('telefono', '').strip()
		correo = request.POST.get('correo', '').strip()

		errors = {}
		if not nombre:
			errors['nombre'] = 'Nombre es obligatorio.'
		elif len(nombre) > 100:
			errors['nombre'] = 'Nombre demasiado largo (máx. 100).'

		if not primer_apellido:
			errors['primer_apellido'] = 'Primer apellido es obligatorio.'
		elif len(primer_apellido) > 100:
			errors['primer_apellido'] = 'Primer apellido demasiado largo (máx. 100).'

		if segundo_apellido and len(segundo_apellido) > 100:
			errors['segundo_apellido'] = 'Segundo apellido demasiado largo (máx. 100).'

		if alias and len(alias) > 100:
			errors['alias'] = 'Alias demasiado largo (máx. 100).'

		if not relacion_id:
			errors['relacion'] = 'Relación es obligatoria.'

		if not telefono:
			errors['telefono'] = 'Teléfono es obligatorio.'
		elif len(telefono) > 30:
			errors['telefono'] = 'Teléfono demasiado largo (máx. 30).'
		else:
			if not re.match(r'^[0-9+()\-\s]+$', telefono):
				errors['telefono'] = 'Teléfono contiene caracteres no permitidos.'

		if correo:
			try:
				validate_email(correo)
			except ValidationError:
				errors['correo'] = 'Correo inválido.'

		if errors:
			relaciones = Relacion.objects.all()
			return render(request, 'editar.html', {'errors': errors, 'relaciones': relaciones, 'contacto': contacto})

		contacto.nombre = nombre.upper()
		contacto.primer_apellido = primer_apellido.upper()
		contacto.segundo_apellido = segundo_apellido.upper() if segundo_apellido else None
		contacto.alias = alias.upper() if alias else None
		contacto.telefono = telefono
		contacto.correo = correo.upper() if correo else None
		contacto.relacion = get_object_or_404(Relacion, pk=relacion_id)
		contacto.save()
		return redirect('listar')

	relaciones = Relacion.objects.all()
	return render(request, 'editar.html', {'contacto': contacto, 'relaciones': relaciones})


def eliminar_contacto(request, id):
	contacto = get_object_or_404(Contacto, pk=id)
	if request.method == 'POST':
		contacto.delete()
		return redirect('listar')
	return render(request, 'eliminar.html', {'contacto': contacto})

