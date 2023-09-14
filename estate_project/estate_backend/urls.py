from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import (post_list, post_detail, about_company, faq_list, privacy_policy, contacts, promo_code, reviews,
                    vacancies, register, CustomLoginView, review_list, add_review)
from django.contrib.auth import views as auth_views

app_name = 'blog'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),
    path('api/', include('estate_backend.api.urls', namespace='api')),
    path('api/drf-auth/', include('rest_framework.urls')),
    path('posts/', post_list, name='post_list'),
    path('posts/<int:id>/', post_detail, name='post_detail'),
    path('about_company/', about_company, name='about_company'),
    path('faq/', faq_list, name='faq_list'),
    path('privacy_policy/', privacy_policy, name='privacy_policy'),
    path('contacts/', contacts, name='contacts'),
    path('promocode/', promo_code, name='promocode'),
    path('reviews/', reviews, name='reviews'),
    path('vacancies/', vacancies, name='vacancies'),
    path('reviews/', review_list, name='review_list'),
    path('reviews/add/', add_review, name='add_review')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
