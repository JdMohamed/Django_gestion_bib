from django.urls import include,path
from .views import UpdateView, UsersView,LogoutView,UserView,LoginView,RegisterView,LivresViewSet, AuteursViewSet, CategoriesViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("livre",LivresViewSet,basename="livre")
router.register("auteur",AuteursViewSet,basename="auteur")
router.register("categorie",CategoriesViewSet,basename="categorie")


urlpatterns = [
    path("", include(router.urls)),
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('user', UserView.as_view()),
    path('users', UsersView.as_view()),
    path('logout', LogoutView.as_view()),
    path('updateUserPriv',UpdateView.as_view())
]