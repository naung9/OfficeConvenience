from django.contrib import admin
from . import models
from django.contrib.admin import helpers
# Register your models here.


class order_history_inline(admin.TabularInline):
    model = models.order_history
    extra = 0
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    
    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            read_only_fields = self.readonly_fields + ('item', 'original_price','quantity','discount')
#             if obj.order_status == 'delivered':
#                 read_only_fields += ('order_status',)
            return read_only_fields
        return self.readonly_fields
    
class confirmed_order_admin(admin.ModelAdmin):
    inlines = [order_history_inline]
    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + ('user',)
        return self.readonly_fields
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    def get_inline_formsets(self, request, formsets, inline_instances, obj=None):
        inline_admin_formsets = []
        for inline, formset in zip(inline_instances, formsets):
            fieldsets = list(inline.get_fieldsets(request, obj))
            readonly = list(inline.get_readonly_fields(request, obj))
            prepopulated = dict(inline.get_prepopulated_fields(request, obj))
            inline_admin_formset = helpers.InlineAdminFormSet(
                inline, formset, fieldsets, prepopulated, readonly,
                model_admin=self,
            )
            if isinstance(inline, order_history_inline):
                for form in inline_admin_formset.forms:
                #Here we change the fields read only.
                    instance = form.instance
                    if instance.order_status == 'delivered':
                        form.fields['order_status'].widget.attrs['disabled'] = True
    
            inline_admin_formsets.append(inline_admin_formset)
        return inline_admin_formsets

class admin_tabular_item(admin.TabularInline):
    model=models.item
    extra = 0
    
class admin_category(admin.ModelAdmin):
    inlines = [admin_tabular_item]

admin.site.register(models.category,admin_category)
admin.site.register(models.item)
admin.site.register(models.customer)
admin.site.register(models.confirmed_order,confirmed_order_admin)