from django.contrib import admin
from .models import Buyer, Owner, Estate, EstateType, Employee, Deal

# Register your models here.


# class EmployeeAdmin(admin.ModelAdmin):
#     pass


admin.site.register(Buyer)
admin.site.register(Owner)
admin.site.register(Estate)
admin.site.register(EstateType)
admin.site.register(Employee)
admin.site.register(Deal)
# admin.site.register(Employee, EmployeeAdmin)
