from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('my-rent/', views.get_my_rent, name='my_rent'),
    path('my-rent/update/<int:pk>/', views.CustomUserUpdateView.as_view(), name='my_rent_update'),
    path('boxes/', views.get_boxes, name='boxes'),
    path('faq/', views.get_faq, name='faq')
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
