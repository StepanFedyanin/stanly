from django.contrib import admin

from mann_whitney.models import Chunk as mann_whitney_chunk
from kruskal.models import Chunk as kruskal_chunk
from compare_two.models import Chunk as compare_two_chunk
from correlation.models import ChunkSpearman, ChunkPearson, ChunkKendall
from wilcox.models import Chunk as wilcox_chunk
from student_ind.models import Chunk as student_ind_chunk
from w.models import Chunk as w_chunk
from z.models import Chunk as z_chunk
from factor_analytic.models import Chunk as factor_analytic_chunk
from anova.models import Chunk as anova_chunk
from desc.models import Chunk as desc_chunk

from mw_calc.models import Order, Calc, Calculation, Chunk as mw_calc_chunk
from robokassa.models import SuccessNotification

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from import_export import resources
from import_export.admin import ImportExportModelAdmin


UserAdmin.list_display = ('email', 'username', 'date_joined', 'last_login')

class ChunkAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': ['title', 'name', 'value', 'html']
        })
    ]
    list_display_links = ('name',)
    list_display = ('title', 'name', 'value', 'html',)


class OrderAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': ['pk', 'user', 'calc_name', 'price', 'status', 'expire', 'expire_count', 'date', 'promo']
        })
    ]

    readonly_fields = ('pk', 'date')

    list_display_links = ('pk',)
    list_display = ('pk', 'user', 'calc_name', 'price',
                    'status', 'expire', 'expire_count',
                    'date', 'promo')
    search_fields = ['user__username']


class SuccessNotificationAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': ['pk', 'InvId', 'OutSum', 'created_at']
        })
    ]

    readonly_fields = ('pk', 'created_at')

    list_display_links = ('pk',)
    list_display = ('pk', 'InvId', 'OutSum', 'created_at')


class CalcAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': ['name', 'active']
        })
    ]

    # readonly_fields = ('name',)

    list_display_links = ('name',)
    list_display = ('name', 'active',)


class CalculationAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': ['pk', 'order_id', 'user', 'calc_name', 'date']
        })
    ]

    readonly_fields = ('pk', 'date')

    list_display_links = ('pk',)
    list_display = ('pk', 'order_id', 'user', 'calc_name', 'date')

    search_fields = ['user__username']


class CalculationResource(resources.ModelResource):

    class Meta:
        model = Calculation
        fields = ('user__username', 'calc_name', 'date',)
        export_order = ('user__username', 'calc_name', 'date',)


class UserResource(resources.ModelResource):

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'date_joined', 'last_login',)
        export_order = ('email', 'username', 'first_name', 'last_name', 'date_joined', 'last_login',)


class UserAdminExport(UserAdmin, ImportExportModelAdmin):
    resource_class = UserResource


class CalculationAdminExport(CalculationAdmin, ImportExportModelAdmin):
    resource_class = CalculationResource


admin.site.unregister(User)
admin.site.register(User, UserAdminExport)

admin.site.register(Order, OrderAdmin)
admin.site.register(Calculation, CalculationAdminExport)
admin.site.register(SuccessNotification, SuccessNotificationAdmin)
admin.site.register(mw_calc_chunk, ChunkAdmin)
admin.site.register(mann_whitney_chunk, ChunkAdmin)
admin.site.register(kruskal_chunk, ChunkAdmin)
admin.site.register(compare_two_chunk, ChunkAdmin)
admin.site.register(ChunkSpearman, ChunkAdmin)
admin.site.register(ChunkPearson, ChunkAdmin)
admin.site.register(ChunkKendall, ChunkAdmin)
admin.site.register(wilcox_chunk, ChunkAdmin)
admin.site.register(student_ind_chunk, ChunkAdmin)
admin.site.register(w_chunk, ChunkAdmin)
admin.site.register(z_chunk, ChunkAdmin)
admin.site.register(factor_analytic_chunk, ChunkAdmin)
admin.site.register(anova_chunk, ChunkAdmin)
admin.site.register(desc_chunk, ChunkAdmin)
