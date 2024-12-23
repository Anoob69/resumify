from django.contrib import admin
from django.urls import path, include
from resumesite import views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls), 
    path('', views.landing_page, name='landing_page'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('edit/<int:resume_id>/', views.edit_resume, name='edit_resume'),
    path('delete/<int:resume_id>/', views.delete_resume, name='delete_resume'),
    path('info/', views.info, name='info'),
    path('download-resume/<int:resume_id>/', views.download_resume, name='download_resume'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)