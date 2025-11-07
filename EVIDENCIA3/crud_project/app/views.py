from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, Categoria

def listar_productos(request):
    productos = Producto.objects.all()
    return render(request, 'listar.html', {'productos': productos})

def crear_producto(request):
    categorias = Categoria.objects.all()
    if request.method == 'POST':
        nombre = request.POST['nombre']
        precio = request.POST['precio']
        descripcion = request.POST['descripcion']
        categoria_id = request.POST['categoria']
        categoria = Categoria.objects.get(id=categoria_id)
        Producto.objects.create(
            nombre=nombre,
            precio=precio,
            descripcion=descripcion,
            categoria=categoria
        )
        return redirect('listar')
    contexto = {'categorias': categorias}
    return render(request, 'crear.html', contexto)
 
def editar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    listar_categorias = Categoria.objects.all()

    if request.method == 'POST':
        producto.nombre = request.POST.get('nombre', producto.nombre)
        producto.precio = request.POST.get('precio', producto.precio)
        producto.descripcion = request.POST.get('descripcion', producto.descripcion)
        # Actualizar categoría si viene en el POST
        categoria_id = request.POST.get('categoria')
        if categoria_id:
            try:
                producto.categoria = Categoria.objects.get(id=categoria_id)
            except Categoria.DoesNotExist:
                # ignorar si categoria no encontrada (podrías manejarlo mejor)
                pass

        producto.save()
        return redirect('listar')

    contexto = {
        'producto': producto,
        'categorias': listar_categorias,
    }
    return render(request, 'editar.html', contexto)

def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    producto.delete()
    return redirect('listar')
