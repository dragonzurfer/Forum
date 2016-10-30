from django.contrib import admin
from .models import Question,Forum,Choice


admin.site.register(Question)
admin.site.register(Forum)
admin.site.register(Choice)
# Register your models here.
