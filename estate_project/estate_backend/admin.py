from django.contrib import admin

from .models import (
    Buyer,
    Owner,
    Estate,
    EstateType,
    Employee,
    Deal,
    CustomUser,
    Post,
    PromoCode,
    FAQ,
    JobVacancy,
    Review
)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

# Register your models here.


admin.site.register(Buyer)
admin.site.register(Owner)
admin.site.register(Estate)
admin.site.register(EstateType)
admin.site.register(Employee)
admin.site.register(Deal)
admin.site.register(CustomUser)
admin.site.register(PromoCode)
admin.site.register(FAQ)
admin.site.register(JobVacancy)
admin.site.register(Review)

