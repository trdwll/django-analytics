from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.conf import settings
from django.db.models import Count, Sum, Min, Max
from django.db.models.functions import Trunc
from django.db.models import DateTimeField
from django.utils.safestring import mark_safe

from .models import (
    GlobalPageHit, Visitor, VisitorPageHit,
    GlobalPageHitSummary, VisitorSummary, VisitorPageHitSummary
)

class PageHitFilter(SimpleListFilter):
    title = 'Page Hits Type'
    parameter_name = 'pagehit'

    def lookups(self, request, model_admin):
        return [('highestcount', 'Highest Count'), ('newest', 'Newest'), ('oldest', 'Oldest'), ('file', 'File'), ('page', 'Page')]

    # this queryset using __contains is probably the worst way to verify if it's a file or not - however it does work... for now lol
    def queryset(self, request, queryset):
        if self.value() == 'highestcount':
            return queryset.order_by('-hit_count')
        elif self.value() == 'newest':
            return queryset.order_by('-id')
        elif self.value() == 'oldest':
            return queryset.order_by('id')
        elif self.value() == 'file':
            return queryset.filter(page_url__contains='.')
        elif self.value() == 'page':
            return queryset.exclude(page_url__contains='.')
        else:
            return queryset

@admin.register(GlobalPageHitSummary)
class GlobalPageHitAdminSummary(admin.ModelAdmin):
    change_list_template = 'admin/globalpagehitsummary_change_list.html'

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )

        return response

class GlobalPageHitAdmin(admin.ModelAdmin):
    change_list_template = 'admin/analytics_change_list.html'
    list_display = ('get_link', 'hit_count', 'created', 'modified', )
    list_filter = (PageHitFilter, )
    search_fields = ['page_url', 'hit_count', 'created', 'modified']

    def get_link(self, instance):
        return mark_safe('%(url)s&nbsp;&nbsp;&nbsp;<a href="%(url)s" target="_blank"><i class="fas fa-external-link-alt"></i></a>' % {'url': instance.page_url})
    get_link.short_description = 'Page URL'
    get_link.allow_tags = True

class VisitorAdmin(admin.ModelAdmin):
    change_list_template = 'admin/analytics_change_list.html'
    list_display = ('created', 'get_ip_address', 'ip_country', 'last_visit', )
    list_filter = ['ip_country']
    search_fields = ['created', 'ip_address', 'ip_country', 'last_visit']

    def get_ip_address(self, instance):
        return mark_safe('<a href="?ip_address=%(ip)s">%(ip)s</a>&nbsp;&nbsp;&nbsp;<a href="https://whatismyipaddress.com/ip/%(ip)s" target="_blank"><i class="fas fa-search"></i></a>' % {'ip': instance.ip_address})
    get_ip_address.short_description = 'IP Address'
    get_ip_address.allow_tags = True

class VisitorPageHitAdmin(admin.ModelAdmin):
    change_list_template = 'admin/analytics_change_list.html'
    list_display = ('get_link', 'get_ip_address', 'hit_count', 'created', )
    list_filter = (PageHitFilter, 'visitor__ip_country', )
    search_fields = ['page_url', 'visitor__ip_address', 'hit_count', 'created', 'user_agent']

    def get_ip_address(self, instance):
        return mark_safe('<a href="?ip_address=%(ip)s">%(ip)s</a>&nbsp;&nbsp;&nbsp;<a href="https://whatismyipaddress.com/ip/%(ip)s" target="_blank"><i class="fas fa-search"></i></a>' % {'ip': instance.visitor.ip_address})
    get_ip_address.short_description = 'IP Address'
    get_ip_address.allow_tags = True

    def get_link(self, instance):
        return mark_safe('%(url)s&nbsp;&nbsp;&nbsp;<a href="%(url)s" target="_blank"><i class="fas fa-external-link-alt"></i></a>' % {'url': instance.page_url})
    get_link.short_description = 'Page URL'
    get_link.allow_tags = True

admin.site.register(GlobalPageHit, GlobalPageHitAdmin)
admin.site.register(Visitor, VisitorAdmin)
admin.site.register(VisitorPageHit, VisitorPageHitAdmin)
