from django.shortcuts import render, redirect
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from .models import Paciente, Turno, Categoria, Producto, Tipopago, Estado, Pedido, Subpedido, Distancia, Armazon, Lado
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group, User
from django.contrib import messages
import xlsxwriter
import io
from datetime import date, timedelta

# Create your views here.

# Views para Pacientes
class FormPaciente(forms.Form):
    nombre = forms.CharField(label="Nombre:", widget=forms.TextInput(attrs={'class':'form-control'}))
    apellido = forms.CharField(label="Apellido:", widget=forms.TextInput(attrs={'class':'form-control'}))
    dni = forms.IntegerField(label="DNI:", widget=forms.TextInput(attrs={'class':'form-control'}))
    telefono = forms.CharField(label="Teléfono:", widget=forms.TextInput(attrs={'class':'form-control'}))
    direccion = forms.CharField(label="Dirección:", widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.CharField(label="E-Mail", widget=forms.TextInput(attrs={'class':'form-control'}))

def pacientescargar(request):
    # Rechazamos acceso y derivamos a la pantalla de login si no hay un usuario autenticado
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    if request.method == "POST":
        form = FormPaciente(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data["nombre"]
            apellido = form.cleaned_data["apellido"]
            dni = form.cleaned_data["dni"]
            telefono = form.cleaned_data["telefono"]
            direccion = form.cleaned_data["direccion"]
            email = form.cleaned_data["email"]
            p = Paciente(nombre=nombre, apellido=apellido, dni=dni, telefono=telefono, direccion=direccion, email=email, user_id=2)
            messages.success(request, 'El Paciente fue Cargado Exitosamente')
            p.save()
        return HttpResponseRedirect(reverse("pacientesindex"))
    else:
        return render(request, "pacientes/form.html", {
            "form" : FormPaciente()
        })

def pacientesindex(request):
    # Rechazamos acceso y derivamos a la pantalla de login si no hay un usuario autenticado
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    pacientes = Paciente.objects.all()
    return render(request, "pacientes/index.html", {
        "pacientes" : pacientes
    })

def pacientesupdate(request, paciente_id):
     # Rechazamos acceso y derivamos a la pantalla de login si no hay un usuario autenticado
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    paciente = Paciente.objects.get(id=paciente_id)
    form = FormPaciente(request.POST)
    if form.is_valid():
        paciente.nombre = form.cleaned_data["nombre"]
        paciente.apellido = form.cleaned_data["apellido"]
        paciente.dni = form.cleaned_data["dni"]
        paciente.telefono = form.cleaned_data["telefono"]
        paciente.direccion = form.cleaned_data["direccion"]
        paciente.email = form.cleaned_data["email"]
        paciente.save()
        messages.success(request, 'El Paciente fue Modificado Exitosamente')
        return HttpResponseRedirect(reverse("pacientesindex"))
    return render(request, 'pacientes/update.html', {
        'id': paciente.id,
        'form': FormPaciente(initial={'id': paciente.id, 'nombre': paciente.nombre, 'apellido': paciente.apellido, 'dni': paciente.dni, 'telefono': paciente.telefono, 'direccion': paciente.direccion,'email': paciente.email})
    })

def pacientesdelete(request, paciente_id):
     # Rechazamos acceso y derivamos a la pantalla de login si no hay un usuario autenticado
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    Paciente.objects.filter(id=paciente_id).delete()
    messages.success(request, 'El Paciente fue Eliminado Exitosamente')
    return HttpResponseRedirect(reverse("turnosindex"))

def pacienteshow(request, paciente_id):
     # Rechazamos acceso y derivamos a la pantalla de login si no hay un usuario autenticado
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    paciente = Paciente.objects.get(id=paciente_id)
    return render(request, "pacientes/show.html", {
        "paciente": paciente
    })

# Views para Turnos
class FormTurno(forms.Form):
    paciente = forms.ModelChoiceField(queryset=Paciente.objects.all(), required=True, widget=forms.Select(attrs={'class':'form-control'}))
    usuario = forms.ModelChoiceField(queryset=User.objects.filter(groups__name='Profesional Médico'), required=True, label="Profesional Médico:", widget=forms.Select(attrs={'class':'form-control'}))
    fecha = forms.DateField(label="Fecha:", widget=forms.DateInput(attrs={'class':'form-control','type':'date'}))
    hora = forms.TimeField(label="Hora:", widget=forms.TimeInput(attrs={'class':'form-control','type':'time'}))

def turnoscreate(request):
    # Rechazamos acceso y derivamos a la pantalla de login si no hay un usuario autenticado
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    if request.method == "POST":
        form = FormTurno(request.POST)
        #breakpoint()
        if form.is_valid():
            paciente = form.cleaned_data["paciente"].id
            fecha = form.cleaned_data["fecha"]
            hora = form.cleaned_data["hora"]
            usuario = form.cleaned_data["usuario"].id
            p = Turno(paciente_id=paciente, fecha=fecha, hora=hora, user_id=usuario, asistencia_id=1)
            messages.success(request, 'El Turno fue Creado Exitosamente')
            p.save()
        return HttpResponseRedirect(reverse("turnosindex"))
    else:
        return render(request, "turnos/create.html", {
            "form" : FormTurno()
        })

def turnosupdate(request, turno_id):
     # Rechazamos acceso y derivamos a la pantalla de login si no hay un usuario autenticado
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    turno = Turno.objects.get(id=turno_id)
    form = FormTurno(request.POST)
    if form.is_valid():
        turno.paciente_id = form.cleaned_data["paciente"].id
        turno.fecha = form.cleaned_data["fecha"]
        turno.hora = form.cleaned_data["hora"]
        turno.user_id = form.cleaned_data["usuario"].id
        turno.save()
        messages.success(request, 'El Turno fue Modificado Exitosamente')
        return HttpResponseRedirect(reverse("turnosindex"))
    return render(request, 'turnos/update.html', {
        'id': turno.id,
        'form': FormTurno(initial={'id': turno.id, 'paciente': turno.paciente_id, 'usuario': turno.user_id, 'fecha': turno.fecha, 'hora': turno.hora})
    })

def turnosdelete(request, turno_id):
     # Rechazamos acceso y derivamos a la pantalla de login si no hay un usuario autenticado
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    Turno.objects.filter(id=turno_id).delete()
    messages.success(request, 'El Turno fue Eliminado Exitosamente')
    return HttpResponseRedirect(reverse("turnosindex"))

def turnosindex(request):
    # Rechazamos acceso y derivamos a la pantalla de login si no hay un usuario autenticado
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    # Filtros
    if request.session ["tipousuario_id"] == 2:
        if request.method == "POST":
            fecha = request.POST["fecha"]
            mes = request.POST["mes"]
            year = request.POST["year"]
            if fecha != '' and mes == '' and year == '':
                turnos = Turno.objects.filter(fecha=fecha, user_id=request.user.id)
            elif mes != '' and fecha == '' and year == '':
                turnos = Turno.objects.filter(fecha__month=mes, user_id=request.user.id)
            elif year != '' and fecha == '' and mes == '':
                turnos = Turno.objects.filter(fecha__year=year, user_id=request.user.id)
            else:
                turnos = []
                messages.success(request, 'Por favor seleccione solo una opción para el filtrado')
        else:
            turnos = Turno.objects.filter(user_id=request.user.id)
        return render(request, "turnos/index.html", {
            "turnos" : turnos
        })
    else:
        if request.method == "POST":
            fecha = request.POST["fecha"]
            mes = request.POST["mes"]
            year = request.POST["year"]
            if fecha != '' and mes == '' and year == '':
                turnos = Turno.objects.filter(fecha=fecha)
            elif mes != '' and fecha == '' and year == '':
                turnos = Turno.objects.filter(fecha__month=mes)
            elif year != '' and fecha == '' and mes == '':
                turnos = Turno.objects.filter(fecha__year=year)
            else:
                turnos = []
                messages.success(request, 'Por favor seleccione solo una opción para el filtrado')
        else:
            turnos = Turno.objects.all()
        return render(request, "turnos/index.html", {
            "turnos" : turnos
        })


def turnoshow(request, turno_id):
     # Rechazamos acceso y derivamos a la pantalla de login si no hay un usuario autenticado
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    turno = Turno.objects.get(id=turno_id)
    return render(request, "turnos/show.html", {
        "turno": turno
    })

def turnoasistencia(request, turno_id, asistencia_id):
     # Rechazamos acceso y derivamos a la pantalla de login si no hay un usuario autenticado
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    turno = Turno.objects.get(id=turno_id)
    turno.asistencia_id = asistencia_id
    turno.save()   
    messages.success(request, f"El estado de Asistencia del Turno cambio a {turno.asistencia.nombre}.")
    return redirect('turnoshow', turno.id)

# Views para Categorias
class FormCategoria(forms.Form):
    nombre = forms.CharField(label="Nombre:", widget=forms.TextInput(attrs={'class':'form-control'}))

def categoriascreate(request):
    # Rechazamos acceso y derivamos a la pantalla de login si no hay un usuario autenticado
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    if request.method == "POST":
        form = FormCategoria(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data["nombre"]
            p = Categoria(nombre=nombre)
            p.save()
            messages.success(request, 'La Categoría fue Creada Exitosamente')
        return HttpResponseRedirect(reverse("categoriasindex"))
    else:
        return render(request, "categorias/create.html", {
            "form" : FormCategoria()
        })

def categoriasupdate(request, categoria_id):
     # Rechazamos acceso y derivamos a la pantalla de login si no hay un usuario autenticado
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    categoria = Categoria.objects.get(id=categoria_id)
    form = FormCategoria(request.POST)
    if form.is_valid():
        categoria.nombre = form.cleaned_data["nombre"]
        categoria.save()
        messages.success(request, 'La Categoría fue modificada Exitosamente')
        return HttpResponseRedirect(reverse("categoriasindex"))
    return render(request, 'categorias/update.html', {
        'id': categoria.id,
        'form': FormCategoria(initial={'id': categoria.id, 'nombre': categoria.nombre})
    })

def categoriasdelete(request, categoria_id):
     # Rechazamos acceso y derivamos a la pantalla de login si no hay un usuario autenticado
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    Categoria.objects.filter(id=categoria_id).delete()
    messages.success(request, 'La Categoría fue Eliminada Exitosamente')
    return HttpResponseRedirect(reverse("categoriasindex"))

def categoriasindex(request):
    # Rechazamos acceso y derivamos a la pantalla de login si no hay un usuario autenticado
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    categorias = Categoria.objects.all()
    return render(request, "categorias/index.html", {
        "categorias" : categorias
    })


def categoriashow(request, categoria_id):
     # Rechazamos acceso y derivamos a la pantalla de login si no hay un usuario autenticado
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    categoria = Categoria.objects.get(id=categoria_id)
    return render(request, "categorias/show.html", {
        "categoria": categoria
    })

# Views para Productos
class FormProducto(forms.Form):
    categoria = forms.ModelChoiceField(queryset=Categoria.objects.all(), required=True, widget=forms.Select(attrs={'class':'form-control'}))
    nombre = forms.CharField(label="Nombre:", widget=forms.TextInput(attrs={'class':'form-control'}))
    precio = forms.IntegerField(label="Precio:", widget=forms.NumberInput(attrs={'class':'form-control'}))
    detalle = forms.CharField(label="Detalle:", widget=forms.TextInput(attrs={'class':'form-control'}))

def productoscreate(request):
    # Rechazamos acceso y derivamos a la pantalla de login si no hay un usuario autenticado
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    if request.method == "POST":
        form = FormProducto(request.POST)
        if form.is_valid():
            categoria = form.cleaned_data["categoria"].id
            nombre = form.cleaned_data["nombre"]
            precio = form.cleaned_data["precio"]
            detalle = form.cleaned_data["detalle"]
            p = Producto(categoria_id=categoria, nombre=nombre, precio=precio, detalle=detalle)
            p.save()
            messages.success(request, 'El Producto fue Creado Exitosamente')
        return HttpResponseRedirect(reverse("productosindex"))
    else:
        return render(request, "productos/create.html", {
            "form" : FormProducto()
        })

def productosupdate(request, producto_id):
     # Rechazamos acceso y derivamos a la pantalla de login si no hay un usuario autenticado
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    producto = Producto.objects.get(id=producto_id)
    form = FormProducto(request.POST)
    if form.is_valid():
        producto.categoria_id = form.cleaned_data["categoria"].id
        producto.nombre = form.cleaned_data["nombre"]
        producto.precio = form.cleaned_data["precio"]
        producto.detalle = form.cleaned_data["detalle"]
        producto.save()
        messages.success(request, 'El Producto fue modificado Exitosamente')
        return HttpResponseRedirect(reverse("productosindex"))
    return render(request, 'productos/update.html', {
        'id': producto.id,
        'form': FormProducto(initial={'id': producto.id, 'categoria' : producto.categoria ,'nombre': producto.nombre, 'precio': producto.precio, 'detalle': producto.detalle})
    })

def productosdelete(request, producto_id):
     # Rechazamos acceso y derivamos a la pantalla de login si no hay un usuario autenticado
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    Producto.objects.filter(id=producto_id).delete()
    messages.success(request, 'El Producto fue Eliminado Exitosamente')
    return HttpResponseRedirect(reverse("productosindex"))

def productosindex(request):
    # Rechazamos acceso y derivamos a la pantalla de login si no hay un usuario autenticado
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    productos = Producto.objects.all()
    return render(request, "productos/index.html", {
        "productos" : productos
    })


def productoshow(request, producto_id):
     # Rechazamos acceso y derivamos a la pantalla de login si no hay un usuario autenticado
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    producto = Producto.objects.get(id=producto_id)
    return render(request, "productos/show.html", {
        "producto": producto
    })

# Views para Pedidos
class FormPedido(forms.Form):
    paciente = forms.ModelChoiceField(queryset=Paciente.objects.all(), required=True, widget=forms.Select(attrs={'class':'form-control'}))
    tipopago = forms.ModelChoiceField(label="Tipo de Pago:",queryset=Tipopago.objects.all(), required=True, widget=forms.Select(attrs={'class':'form-control'}))
    fechaentrega = forms.DateField(label="Fecha de Entrega:", widget=forms.DateInput(attrs={'class':'form-control','type':'date'}))

class FormSubpedido(forms.Form):
    producto = forms.ModelChoiceField(label="Producto:", queryset=Producto.objects.all(), required=True, widget=forms.Select(attrs={'class':'form-control'}))
    cantidad = forms.IntegerField(label="Cantidad:", required=True, widget=forms.NumberInput(attrs={'class':'form-control'}))
    lado = forms.ModelChoiceField(empty_label=None, label="Lado:", queryset=Lado.objects.all(), required=True, widget=forms.Select(attrs={'class':'form-control', 'style':'display:none'}))
    distancia = forms.ModelChoiceField(empty_label=None, label="Distancia:", queryset=Distancia.objects.all(), required=True, widget=forms.Select(attrs={'class':'form-control', 'style':'display:none'}))
    armazon = forms.ModelChoiceField(empty_label=None, label="Armazón:", queryset=Armazon.objects.all(), required=True, widget=forms.Select(attrs={'class':'form-control', 'style':'display:none'}))

def pedidoscreate(request):
    # Rechazamos acceso y derivamos a la pantalla de login si no hay un usuario autenticado
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    if request.method == "POST":
        form = FormPedido(request.POST)
        if form.is_valid():
            paciente = form.cleaned_data["paciente"].id
            tipopago = form.cleaned_data["tipopago"].id
            fechaentrega = form.cleaned_data["fechaentrega"]
            p = Pedido(estado_id=1, paciente_id=paciente, tipopago_id=tipopago, user_id=request.user.id, fechaentrega=fechaentrega, total=0)
            p.save()
            messages.success(request, 'El Pedido fue Creado Exitosamente')
        return redirect('pedidoshow', p.id)
    else:
        return render(request, "pedidos/create.html", {
            "form" : FormPedido()
        })

def pedidosupdate(request, pedido_id):
     # Rechazamos acceso y derivamos a la pantalla de login si no hay un usuario autenticado
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    pedido = Pedido.objects.get(id=pedido_id)
    form = FormPedido(request.POST)
    if form.is_valid():
        pedido.paciente_id = form.cleaned_data["paciente"].id
        pedido.tipopago_id = form.cleaned_data["tipopago"].id
        pedido.fechaentrega = form.cleaned_data["fechaentrega"]
        pedido.save()
        messages.success(request, 'El Pedido fue modificado Exitosamente')
        return redirect('pedidoshow', pedido.id)
    return render(request, 'pedidos/update.html', {
        'id': pedido.id,
        'form': FormPedido(initial={'id': pedido.id, 'paciente' : pedido.paciente_id , 'tipopago': pedido.tipopago_id, 'fechaentrega': pedido.fechaentrega})
    })

def pedidosdelete(request, pedido_id):
     # Rechazamos acceso y derivamos a la pantalla de login si no hay un usuario autenticado
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    Pedido.objects.filter(id=pedido_id).delete()
    messages.success(request, 'El Pedido fue Eliminado Exitosamente')
    return HttpResponseRedirect(reverse("pedidosindex"))

def pedidosindex(request):
    # Rechazamos acceso y derivamos a la pantalla de login si no hay un usuario autenticado
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    pedidos = Pedido.objects.all()
    return render(request, "pedidos/index.html", {
        "pedidos" : pedidos
    })

def pedidoshow(request, pedido_id):
     # Rechazamos acceso y derivamos a la pantalla de login si no hay un usuario autenticado
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    pedido = Pedido.objects.get(id=pedido_id)
    productos = Producto.objects.all()
    items = Subpedido.objects.filter(pedido_id=pedido_id)
    if request.method == "POST":
        form = FormSubpedido(request.POST)
        if form.is_valid():
            producto = form.cleaned_data["producto"].id
            lado = form.cleaned_data["lado"].id
            armazon = form.cleaned_data["armazon"].id
            distancia = form.cleaned_data["distancia"].id
            cantidad = form.cleaned_data["cantidad"]
            p = Subpedido(pedido_id=pedido_id, producto_id=producto, lado_id=lado, armazon_id=armazon, distancia_id=distancia, cantidad=cantidad)
            p.save()
            precioProducto = Producto.objects.get(id=producto).precio
            pedido.total = pedido.total + (cantidad * precioProducto)
            pedido.save()
            messages.success(request, 'El Item fue Agregado Exitosamente')
            return redirect('pedidoshow', pedido_id)
    else:
        return render(request, "pedidos/show.html", {
            "pedido": pedido,
            "items" : items,
            "productos": productos,
            "form" : FormSubpedido()
        })

def itemdelete(request, item_id):
     # Rechazamos acceso y derivamos a la pantalla de login si no hay un usuario autenticado
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    item = Subpedido.objects.get(id=item_id)
    pedido = Pedido.objects.get(id=item.pedido_id)
    precioProducto = Producto.objects.get(id=item.producto_id).precio
    pedido.total = pedido.total - (precioProducto * item.cantidad)
    pedido.save()
    item.delete()
    messages.success(request, 'El Item fue Eliminado Exitosamente')
    return redirect('pedidoshow', pedido.id)

def pedidoestado(request, pedido_id, estado_id):
     # Rechazamos acceso y derivamos a la pantalla de login si no hay un usuario autenticado
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    pedido = Pedido.objects.get(id=pedido_id)
    pedido.estado_id = estado_id
    pedido.save()   
    messages.success(request, f"El estado del pedido cambio a {pedido.estado.nombre}.")
    return redirect('pedidoshow', pedido.id)

# Views para Autenticación:
def index(request):
    # Rechazamos acceso y derivamos a la pantalla de login si no hay un usuario autenticado
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    return render(request, "usuarios/usuario.html")

def login_view(request):
    if request.method == "POST":
        nombreusuario = request.POST["nombreusuario"]
        password = request.POST["password"]
        user = authenticate(request, username = nombreusuario, password=password)
        if user:
            request.session ["user_id"] = request.user.id
            login(request, user)
            # Obtenemos el tipo de Usuario
            query_set = Group.objects.filter(user = request.user)
            for g in query_set:
                request.session ["tipousuario"] = g.name
                request.session ["tipousuario_id"] = g.id
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "usuarios/login.html", {
            "error": "El nombre de usuario o la clave son incorrectas."
            })

    return render(request, "usuarios/login.html")

def logout_view(request):
    logout(request)
    return render(request, "usuarios/login.html", {
    "mensaje": "Sesión Finalizada."
    })

def consulta(request, *a, **kw):
    # Notice I didn't directly try to access request.GET["check_this"]
    search_value = request.GET.get("check_this", None)
    if search_value:
        data = dict()
        # Finding some data that you want.
        producto = Producto.objects.get(id=search_value)
        data["result"] = producto.categoria_id
        # Using Django's beautiful JsonResponse class 
        # to return your dict as JSON.
        return JsonResponse(data)

def reportepacientes(request, asistencia_id, rango):
    hoy = date.today()
    if rango == 1:
        fechaInicial = hoy - timedelta(days=7) # Una semana de rango
    if rango == 2:
         fechaInicial = hoy - timedelta(days=30) # Un mes de rango
    turnos = Turno.objects.filter(fecha__range=(fechaInicial, hoy), asistencia_id= asistencia_id)
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()

    worksheet.write(0, 0, 'Nombre')
    worksheet.write(0, 1, 'Apellido')
    worksheet.write(0, 2, 'Fecha')
    worksheet.write(0, 3, 'Hora')
    worksheet.write(0, 4, 'Médico')
    
    i = 1
    for turno in turnos:
        worksheet.write(i, 0, turno.paciente.nombre)
        i = i + 1
    i = 1
    for turno in turnos:
        worksheet.write(i, 1, turno.paciente.apellido)
        i = i + 1
    i = 1
    for turno in turnos:
        worksheet.write(i, 2, str(turno.fecha))
        i = i + 1
    i = 1
    for turno in turnos:
        worksheet.write(i, 3, str(turno.hora))
        i = i + 1
    i = 1
    for turno in turnos:
        worksheet.write(i, 4, turno.user.get_username())
        i = i + 1
    
    workbook.close()
    output.seek(0)
    filename = 'Reporte.xlsx'
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response

def reportepacientespedidos(request, rango):
    hoy = date.today()
    if rango == 1:
        fechaInicial = hoy - timedelta(days=7) # Una semana de rango
    if rango == 2:
         fechaInicial = hoy - timedelta(days=30) # Un mes de rango
    pedidos = Pedido.objects.filter(created_at__range=(fechaInicial, hoy))
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()

    worksheet.write(0, 0, 'Nombre')
    worksheet.write(0, 1, 'Apellido')
    worksheet.write(0, 2, 'N° de Pedido')
    worksheet.write(0, 3, 'Vendedor')
    
    i = 1
    for pedido in pedidos:
        worksheet.write(i, 0, pedido.paciente.nombre)
        i = i + 1
    i = 1
    for pedido in pedidos:
        worksheet.write(i, 1, pedido.paciente.apellido)
        i = i + 1
    i = 1
    for pedido in pedidos:
        worksheet.write(i, 2, pedido.id)
        i = i + 1
    i = 1
    for pedido in pedidos:
        worksheet.write(i, 3, pedido.user.get_username())
        i = i + 1
    
    workbook.close()
    output.seek(0)
    filename = 'Reporte.xlsx'
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response

def reporteproductos(request):
    hoy = date.today()
    fechaInicial = hoy - timedelta(days=30) # Un mes de rango
    pedidos = Pedido.objects.filter(created_at__range=(fechaInicial, hoy))
    productos = Producto.objects.all()
    ultimoProducto = Producto.objects.last()
    total = [0] * ultimoProducto.id
    total2 = [0] * ultimoProducto.id
    for producto in productos:
        total[(producto.id)-1] = 0
        for pedido in pedidos:
            subpedidos = Subpedido.objects.filter(pedido_id=pedido.id, producto_id=producto.id)
            for subpedido in subpedidos:
                total[(producto.id)-1] = total[(producto.id)-1] + subpedido.cantidad
            total2[(producto.id)-1] = [producto.nombre, total[(producto.id)-1]]

    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()

    worksheet.write(0, 0, 'Nombre')
    worksheet.write(0, 1, 'Cantidad')
    
    
    def takeSecond(elem):
        return elem[1]
    total2.sort(key=takeSecond, reverse=True)
        
    i = 0
    for j in total2:
        worksheet.write(i+1, 0, total2[i][0])
        i = i + 1
    
    i = 0
    for j in total2:
        worksheet.write(i+1, 1, total2[i][1])
        i = i + 1
    
    workbook.close()
    output.seek(0)
    filename = 'Reporte.xlsx'
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response

def reporteventas(request):
    hoy = date.today()
    fechaInicial = hoy - timedelta(days=30) # Un mes de rango
    pedidos = Pedido.objects.filter(created_at__range=(fechaInicial, hoy))
    ususventas = User.objects.filter(groups__name='Ventas')
    dimension = ususventas.count()
    total = [0] * dimension
    i = 0
    for usuventas in ususventas:
        pedidos = Pedido.objects.filter(user_id=usuventas.id)
        conteo = pedidos.count()
        total[i] = [usuventas.username, conteo]
        i = i + 1

    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()

    worksheet.write(0, 0, 'Vendedor')
    worksheet.write(0, 1, 'Cantidad de Ventas')
    
    
    def takeSecond(elem):
        return elem[1]
    total.sort(key=takeSecond, reverse=True)
        
    i = 0
    for j in total:
        worksheet.write(i+1, 0, total[i][0])
        i = i + 1
    
    i = 0
    for j in total:
        worksheet.write(i+1, 1, total[i][1])
        i = i + 1
    
    workbook.close()
    output.seek(0)
    filename = 'Reporte.xlsx'
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response