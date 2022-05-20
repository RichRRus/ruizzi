from django.contrib import admin

from prize import models


@admin.register(models.Prize)
class PrizeAdmin(admin.ModelAdmin):
    ...


@admin.register(models.PrizeRequest)
class PrizeRequestAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'prize',
        'state',
    )
    readonly_fields = (
        'user',
        'prize',
        'cost',
        'state',
    )
