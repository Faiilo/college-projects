from django.db import models
from django.contrib.auth.models import User

class Document(models.Model):
    name = models.TextField()

    class Meta:
        managed = False
        db_table = 'document'
    
    def __str__(self):
        return self.name

class PracType(models.Model):
    id_prac_type = models.AutoField(primary_key=True)
    type_name = models.TextField(unique=True)

    class Meta:
        managed = False
        db_table = 'prac_type'
    
    def __str__(self):
        return self.type_name

class DatasetOtchet(models.Model):
    id_dataset = models.AutoField(primary_key=True)
    familia = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    otchestvo = models.TextField(blank=True, null=True)
    prac_type = models.ForeignKey(PracType, on_delete=models.SET_NULL, 
                                   db_column='prac_type_id', null=True, blank=True)
    module = models.TextField(blank=True, null=True)
    specialization = models.TextField(blank=True, null=True)
    kurs = models.IntegerField(blank=True, null=True)
    group = models.TextField(blank=True, null=True)
    date_begin = models.TextField(blank=True, null=True)
    date_finish = models.TextField(blank=True, null=True)
    head1 = models.TextField(blank=True, null=True)
    head2 = models.TextField(blank=True, null=True)
    ruc_pract = models.TextField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    hours = models.IntegerField(blank=True, null=True, default=36)
    mesto = models.TextField(blank=True, null=True, verbose_name='Место прохождения практики')
    address = models.TextField(blank=True, null=True, verbose_name='Адрес прохождения практики')
    mdk = models.TextField(blank=True, null=True, verbose_name='МДК')  # НОВОЕ ПОЛЕ
    user = models.ForeignKey(User, on_delete=models.SET_NULL, 
                              db_column='user_id', null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'dataset_otchet'
    
    def __str__(self):
        return f"{self.familia} {self.name} {self.otchestvo} - {self.group}"

# Новая модель для хранения шаблонов документов
class DocumentTemplate(models.Model):
    DOCUMENT_TYPES = [
        ('title', 'Титульный лист'),
        ('assignment', 'Задание'),
        ('diary', 'Дневник'),
    ]
    
    doc_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES, unique=True, verbose_name='Тип документа')
    name = models.CharField(max_length=200, verbose_name='Название шаблона')
    template_file = models.FileField(upload_to='templates/', verbose_name='Файл шаблона')
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата загрузки')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    class Meta:
        verbose_name = 'Шаблон документа'
        verbose_name_plural = 'Шаблоны документов'
    
    def __str__(self):
        return f"{self.get_doc_type_display()} - {self.name}"