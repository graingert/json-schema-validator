"""
Administration interface of the Dashboard application
"""

from django import forms
from django.contrib import admin
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext as _

from launch_control.dashboard_app.models import (
        Bundle,
        BundleStream,
        HardwareDevice,
        NamedAttribute,
        SoftwarePackage,
        )


class BundleAdmin(admin.ModelAdmin):

    def bundle_stream_pathname(self, bundle):
        return bundle.bundle_stream.pathname
    bundle_stream_pathname.short_description = _("Bundle stream")

    list_display = ('bundle_stream_pathname', 'uploaded_by', 'uploaded_on',
            'content_filename', 'is_deserialized')
    date_hierarchy = 'uploaded_on'
    fieldsets = (
            ('Document', {
                'fields': ('content', 'content_filename')}),
            ('Upload Details', {
                'fields': ('bundle_stream', 'uploaded_by')}),
            )


class BundleStreamAdminForm(forms.ModelForm):
    class Meta:
        model = BundleStream

    def clean(self):
        cleaned_data = self.cleaned_data
        print cleaned_data
        if (cleaned_data.get('user', '') is not None and
                cleaned_data.get('group') is not None):
            raise forms.ValidationError('BundleStream cannot have both user '
                    'and name set at the same time')
        return super(BundleStreamAdminForm, self).clean()


class BundleStreamAdmin(admin.ModelAdmin):
    form = BundleStreamAdminForm
    list_display = ('user', 'group', 'slug', 'name', 'pathname')
    prepopulated_fields = {"slug": ("name",)}
    fieldsets = (
            (None, {
                'fields': ('name', 'slug')}),
            ('Ownership', {
                'fields': ('user', 'group')}),
            )


class SoftwarePackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'version')
    search_fields = ('name', 'version')


class HardwareDeviceAdmin(admin.ModelAdmin):
    class NamedAttributeInline(generic.GenericTabularInline):
        model = NamedAttribute
    list_display = ('description', 'device_type')
    search_fields = ('description',)
    inlines = [NamedAttributeInline]


admin.site.register(Bundle, BundleAdmin)
admin.site.register(BundleStream, BundleStreamAdmin)
admin.site.register(HardwareDevice, HardwareDeviceAdmin)
admin.site.register(SoftwarePackage, SoftwarePackageAdmin)