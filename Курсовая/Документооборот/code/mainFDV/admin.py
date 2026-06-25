from django.contrib import admin
from .models import DatasetOtchet, PracType, DocumentTemplate, Document

class DatasetOtchetAdmin(admin.ModelAdmin):
    list_display = ('id_dataset', 'familia', 'name', 'otchestvo', 'group', 'prac_type', 'user', 'hours')
    list_filter = ('prac_type', 'group', 'kurs')
    search_fields = ('familia', 'name', 'otchestvo', 'group', 'mesto', 'address', 'mdk')
    raw_id_fields = ('user',)
    fieldsets = (
        ('Личная информация', {
            'fields': ('familia', 'name', 'otchestvo')
        }),
        ('Информация о практике', {
            'fields': ('prac_type', 'module', 'specialization', 'kurs', 'group', 'hours', 'mesto', 'address', 'mdk')  # Добавили mdk
        }),
        ('Период практики', {
            'fields': ('date_begin', 'date_finish')
        }),
        ('Руководство', {
            'fields': ('head1', 'head2', 'ruc_pract', 'year')
        }),
        ('Пользователь', {
            'fields': ('user',)
        }),
    )

class PracTypeAdmin(admin.ModelAdmin):
    list_display = ('id_prac_type', 'type_name')
    search_fields = ('type_name',)

class DocumentTemplateAdmin(admin.ModelAdmin):
    list_display = ('doc_type', 'name', 'uploaded_at', 'updated_at')
    list_filter = ('doc_type', 'uploaded_at')
    search_fields = ('name',)
    fieldsets = (
        (None, {
            'fields': ('doc_type', 'name', 'template_file')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """При сохранении проверяем, что для каждого типа документа только один шаблон"""
        if not change:  # Если создается новый
            # Удаляем старый шаблон того же типа, если он существует
            DocumentTemplate.objects.filter(doc_type=obj.doc_type).delete()
        super().save_model(request, obj, form, change)

class DocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

# Регистрируем модели в админке
admin.site.register(DatasetOtchet, DatasetOtchetAdmin)
admin.site.register(PracType, PracTypeAdmin)
admin.site.register(DocumentTemplate, DocumentTemplateAdmin)
admin.site.register(Document, DocumentAdmin)