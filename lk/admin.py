from django.contrib import admin
from .models import Promo


class PromoAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            # 'fields': ['user', 'name', 'discount', 'expire', 'active', 'private', 'user_receiver']
            'fields': ['user', 'name', 'discount', 'expire', 'active', 'private',]
        })
    ]

    list_display_links = ('pk',)
    list_display = ('pk', 'user', 'name', 'active',
                    'private', 'discount', 'expire',)
                    # 'private', 'discount', 'expire', 'user_receiver')


admin.site.register(Promo, PromoAdmin)
