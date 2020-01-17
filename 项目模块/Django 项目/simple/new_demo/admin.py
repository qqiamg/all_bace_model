from django.contrib import admin
from new_demo.models import BaceManber


# Register your models here.

class DepartmentAdmin(admin.ModelAdmin):
    # 指定后台网页要显示的字段
    list_display = ["id", "name", "year"]

admin.site.register(BaceManber,DepartmentAdmin)

