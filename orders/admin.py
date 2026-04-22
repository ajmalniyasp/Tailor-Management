from django.contrib import admin
from .models import Measurements, DressType, Fabric, Order, OrderItem


# Register your models here.


# @admin.register(DressType)
# class DressTypeAdmin(admin.ModelAdmin):
#     list_display = ("name", "is_active", "created_by", "updated_by")
#     readonly_fields = ("created_by", "updated_by", "deleted_by", "auto_id", "created_at", "updated_at")
#     exclude = ("deleted_by", "language")  # if you want to hide language

    # def save_model(self, request, obj, form, change):
    #     if not change:
    #         obj.created_by = request.user
    #         obj.is_active = True
    #     obj.updated_by = request.user
    #     super().save_model(request, obj, form, change)


@admin.register(Measurements)
class MeasurementsAdmin(admin.ModelAdmin):
    list_display = ("customer", "dress_type", "is_active", "created_by", "updated_by")
    readonly_fields = ("created_by", "updated_by", "deleted_by", "auto_id", "created_at", "updated_at")
    exclude = ("deleted_by", "language")

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
            obj.is_active = True
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Fabric)
admin.site.register(Order)
admin.site.register(DressType)
admin.site.register(OrderItem)


