from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render

from dashboard.models import PurchaseOrder


@login_required
def order_list(request):

    orders = PurchaseOrder.objects.all()

    search = request.GET.get("search", "").strip()
    almacen = request.GET.get("almacen", "").strip()
    categoria = request.GET.get("categoria", "").strip()
    modelo = request.GET.get("modelo", "").strip()

    # Buscar por código o nombre
    if search:
        orders = orders.filter(
            Q(codigo_item__icontains=search) |
            Q(item_name__icontains=search)
        )

    # Filtrar por almacén
    if almacen:
        orders = orders.filter(
            almacen=almacen
        )

    # Filtrar por categoría
    if categoria:
        orders = orders.filter(
            categoria=categoria
        )

    # Filtrar por modelo ganador
    if modelo:
        orders = orders.filter(
            modelo_ganador=modelo
        )

    # Ordenamos de mayor a menor valor
    orders = orders.order_by(
        "-valor_orden"
    )

    # Paginación
    paginator = Paginator(
        orders,
        25
    )

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(
        page_number
    )

    # Opciones para filtros
    warehouses = (
        PurchaseOrder.objects
        .values_list(
            "almacen",
            flat=True
        )
        .distinct()
        .order_by("almacen")
    )

    categories = (
        PurchaseOrder.objects
        .values_list(
            "categoria",
            flat=True
        )
        .distinct()
        .order_by("categoria")
    )

    models = (
        PurchaseOrder.objects
        .exclude(modelo_ganador="")
        .values_list(
            "modelo_ganador",
            flat=True
        )
        .distinct()
        .order_by("modelo_ganador")
    )

    context = {
        "page_obj": page_obj,

        "search": search,
        "almacen": almacen,
        "categoria": categoria,
        "modelo": modelo,

        "warehouses": warehouses,
        "categories": categories,
        "models": models,
    }

    return render(
        request,
        "orders/orders.html",
        context
    )