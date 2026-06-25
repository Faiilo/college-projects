"""
URL configuration for SiteIAC project.
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from mainFDV import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('profile/', views.profile),
    path('', views.register),
    path('login/', views.loginf),
    path('logout/', views.logoutf),
    # URL для генерации всех документов сразу
    path('generate_all/', views.generate_all_documents, name='generate_all'),
]

# Добавляем URL для медиафайлов (шаблонов)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)