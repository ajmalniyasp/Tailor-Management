from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from foundations.functions import get_auto_id

from accounts.models import User
from .models import Measurements, DressType, Order, Fabric, OrderItem
from django.shortcuts import get_object_or_404
from .forms import MeasurementsForm, DressTypeForm, OrderForm
from django.shortcuts import redirect
from decimal import Decimal
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem, Measurements
from .utils import update_order_totals  # adjust import if needed

# Create your views here.
from .utils import update_order_totals


def get_fields(request, dress_type_id):
    dress_type = DressType.objects.get(id=dress_type_id)
    return JsonResponse({"required_fields": dress_type.required_fields})


# measurements

@login_required
def measurement_list(request):
    dress_filter = request.GET.get("dress")

    measurements = (
        Measurements.objects.filter(customer=request.user, is_active=True)
        # ⬇️ EXCLUDE measurements that have been used in a placed order
        .exclude(order_items__order__status__in=["processing", "confirmed", "in-progress", "completed"])
        .distinct()
    )

    if dress_filter:
        measurements = measurements.filter(dress_type_id=dress_filter)

    dress_types = DressType.objects.all()

    return render(request, "measurements/list.html", {
        "measurements": measurements,
        "dress_types": dress_types,
    })


# add measurements

@login_required
def measurement_create(request):
    dress_type = None
    dress_type_id = request.GET.get("dress_type") or request.POST.get("dress_type")

    if dress_type_id:
        dress_type = get_object_or_404(DressType, id=dress_type_id)

    # fabric = Fabric.objects.all()

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        if dress_type:
            return JsonResponse({"fields": dress_type.required_fields or []})
        return JsonResponse({"fields": []})

    if request.method == 'POST':
        form = MeasurementsForm(request.POST or None, dress_type=dress_type)
        if form.is_valid():
            measurement = form.save(commit=False)
            measurement.customer = request.user
            measurement.dress_type = dress_type
            measurement.created_by = request.user
            measurement.updated_by = request.user
            measurement.staff = form.cleaned_data.get('staff')
            measurement.color = form.cleaned_data.get('color')

            # Auto generate auto_id
            last = Measurements.objects.order_by('-auto_id').first()
            measurement.auto_id = (last.auto_id + 1) if last else 1
            # measurement.auto_id = get_auto_id(Measurements)

            measurement.is_active = True

            # DEBUG: Print what we're saving
            print("Saving measurement with data:")
            print(f"Dress Type: {dress_type}")
            if dress_type and dress_type.required_fields:
                for field_name in dress_type.required_fields:
                    value = request.POST.get(field_name)
                    print(f"{field_name}: {value}")
                    if value:
                        try:
                            setattr(measurement, field_name, float(value))
                        except (ValueError, TypeError):
                            pass

            measurement.save()
            print("Measurement saved successfully!")
            return redirect('orders:measurement_list')
        else:
            # Form is invalid, print errors
            print("Form errors:", form.errors)
    else:
        form = MeasurementsForm(dress_type=dress_type)

    dress_types = DressType.objects.all()
    staff = User.objects.filter(role=3)
    return render(request, 'measurements/form.html', {
        'form': form,
        "dress_types": dress_types,
        "selected_dress": dress_type,
        'staff':staff,
        "fabrics": Fabric.objects.all(),
    })


# update measurements


@login_required
def measurement_update(request, pk):
    measurement = get_object_or_404(Measurements, pk=pk, customer=request.user)
    dress_type = measurement.dress_type


    if request.method == "POST":
        form = MeasurementsForm(request.POST, instance=measurement, dress_type=dress_type)
        if form.is_valid():
            form.save()
            return redirect("orders:measurement_list")
    else:
        form = MeasurementsForm(instance=measurement, dress_type=dress_type)

    return render(request, "measurements/edit.html", {
        "form": form,
        "measurement": measurement,
    })

    # # Prepare context with field values
    # context = {
    #     'measurement': measurement,
    #     'is_edit': True,
    # }
    #
    # # Add field values to context
    # if dress_type and dress_type.required_fields:
    #     for field_name in dress_type.required_fields:
    #         if hasattr(measurement, field_name):
    #             value = getattr(measurement, field_name)
    #             context[f'field_{field_name}'] = value if value is not None else ''
    #
    # if request.method == 'POST':
    #     form = MeasurementsForm(request.POST, instance=measurement, dress_type=dress_type)
    #     if form.is_valid():
    #         updated_measurement = form.save(commit=False)
    #         updated_measurement.updated_by = request.user
    #         updated_measurement.save()
    #         return redirect('measurement_list')
    #     context['form'] = form
    # else:
    #     context['form'] = MeasurementsForm(instance=measurement, dress_type=dress_type)
    #
    # return render(request, 'measurements/edit.html', context)
# Delete measurements

@login_required
def measurement_delete(request, pk):
    measurement = get_object_or_404(Measurements, pk=pk, customer=request.user)
    if request.method == 'POST':
        measurement.is_active = False
        measurement.deleted_by = request.user  # 👈 track deleter
        measurement.save()
        return redirect('orders:measurement_list')
    return render(request, 'measurements/delete.html', {'measurement': measurement})


@login_required
def measurement_detail(request, pk):
    measurements = get_object_or_404(Measurements, id=pk, customer=request.user)
    return render(request, 'measurements/details.html', {'measurement': measurements})

#dress type


def dresstype_list(request):
    dress_types = DressType.objects.filter(is_active=True)
    return render(request, "dress_type/list.html", {"dress_types": dress_types})


@login_required
def dresstype_create(request):
    if request.method == "POST":
        form = DressTypeForm(request.POST)
        if form.is_valid():
            dress_type = form.save(commit=False)
            dress_type.created_by = request.user
            dress_type.updated_by = request.user
            dress_type.is_active = True  # make it active on creation
            dress_type.save()
            messages.success(request, "Dress type added successfully")
            return redirect("dresstype_list")
    else:
        form = DressTypeForm()
    return render(request, "dress_type/form.html", {"form": form})


@login_required
def dresstype_update(request, pk):
    dress_type = get_object_or_404(DressType, pk=pk)
    if request.method == "POST":
        form = DressTypeForm(request.POST, instance=dress_type)
        if form.is_valid():
            updated_dress_type = form.save(commit=False)
            updated_dress_type.updated_by = request.user  # track who updated
            updated_dress_type.save()
            messages.success(request, "Dress type updated successfully")
            return redirect("dresstype_list")
    else:
        form = DressTypeForm(instance=dress_type)
    return render(request, "dress_type/form.html", {"form": form})


@login_required
def dresstype_delete(request, pk):
    dress_type = get_object_or_404(DressType, pk=pk)
    dress_type.is_active = False
    dress_type.deleted_by = request.user  # track deleter
    dress_type.save()
    messages.success(request, "Dress type deleted successfully")
    return redirect("dresstype_list")


def place_order(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.customer = request.user
            form.save()
            return redirect("order_list")
    else:
        form= OrderForm()
    return render(request, "orders/form.html", {"form": form})


def order_list(request):
    orders = Order.objects.select_related("measurement__staff", "measurement__dress_type").order_by("-created_at")
    return render(request, "orders/list.html", {"orders": orders})


def available_dresses(request):
    dresses = DressType.objects.all()
    return render(request,"booking/available_dresses.html", {"dresses": dresses})


@login_required
def add_measurement_to_order(request, measurement_id):
    measurement = get_object_or_404(Measurements, id=measurement_id, customer=request.user)

    order, created = Order.objects.get_or_create(
        customer=request.user,
        status="pending",
        defaults={"payment_status": "unpaid", "created_by": request.user},
    )

    price = Decimal(0.00)
    try:
        if measurement.dress_type and hasattr(measurement.dress_type, "price"):
            price = Decimal(measurement.dress_type.price or 0.00)
    except Exception:
        price = Decimal(0.00)

    # ✅ Use defaults with guaranteed numeric price
    order_item, created = OrderItem.objects.get_or_create(
        order=order,
        measurement=measurement,
        defaults={
            "quantity": measurement.quantity or 1,
            "price": price,  # always safe value
        }
    )

    if not created:
        order_item.quantity += measurement.quantity or 1
        order_item.save()

    update_order_totals(order)
    return redirect("orders:order_detail", order_id=order.id)


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    items = order.items.select_related("measurement","measurement__dress_type")
    return render(request, "orders/order_detail.html", {"order": order, "items": items})


@login_required
def update_quantity(request, item_id):
    item = get_object_or_404(OrderItem, id=item_id, order__customer=request.user)

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "increase":
            item.quantity += 1
        elif action == "decrease" and item.quantity > 1:
            item.quantity -= 1
        item.save()

        # Update order totals after quantity change
        update_order_totals(item.order)

    return redirect("orders:order_detail", order_id=item.order.id)


@login_required
def cancel_item(request, item_id):
    item = get_object_or_404(OrderItem, id=item_id, order__customer=request.user)

    if request.method == "POST":
        order = item.order
        item.delete()  # Remove the item from order
        update_order_totals(order)  # Update total after deletion
        messages.success(request, "Item removed from your cart.")

    return redirect("orders:order_detail", order_id=item.order.id)


@login_required
def confirm_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)

    order.status = "processing"
    order.save()

    messages.success(request, "✅ Order confirmed successfully!")

    return redirect("orders:measurement_list")


