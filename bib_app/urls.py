from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("api/",include('bib_app.api.urls')),
    #path("api/livres",views.livre_list_api,name="liste_livres_api"),
    #path("api/livres/<int:pk>",views.livre_detail_api,name="detail_livre_api"),
    path('',views.HomePageView.as_view(), name='home'),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/signup/', views.signup, name='signup'),
    path('livres/', views.liste_livres, name='liste_livres'),
    path('livres/<int:livre_id>/', views.detail_livre, name='detail_livre'),
    path('auteurs/', views.liste_auteurs, name='liste_auteurs'),
    path('auteurs/<int:auteur_id>/', views.detail_auteur, name='detail_auteur'),
    path('categories/', views.liste_categories, name='liste_categories'),
    path('categories/<int:categorie_id>/', views.detail_categorie, name='detail_categorie'),
    path('utilisateurs/', views.liste_utilisateurs, name='liste_utilisateurs'),
    path('utilisateurs/<int:utilisateur_id>/', views.detail_utilisateur, name='detail_utilisateur'),
]