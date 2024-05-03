from django.contrib.auth.decorators import login_required
from django import forms
from django.shortcuts import render, get_object_or_404, redirect
from .models import Livre, Auteur, Categorie
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.core.paginator import Paginator
from django.views.generic import TemplateView
from django.contrib.auth.models import User


# API SECTION
def livre_list_api(request):
    livres = Livre.objects.all()
    data = {"livres": list(livres.values())}
    response = JsonResponse(data)
    return response


def livre_detail_api(request, pk):
    try:
        livre = Livre.objects.get(pk=pk)
        auteurs = livre.auteurs.all()
        data = {"livre": {
                        "title":livre.titre,
                        "auteurs":list(auteurs.values("id","nom")),
                        "isbn":livre.isbn}}
        response = JsonResponse(data)
    except Livre.DoesNotExist:
        response = JsonResponse({
            "error":{
                "code": 404,
                "message": "Livre does not exist"
             },
            "status":404})
    return response



class HomePageView(TemplateView):
    template_name = 'home.html'


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form = LoginForm()
                message = "Nom d'utilisateur ou mot de passe incorrect."
                return render(request, 'registration/login.html', {'form': form, 'message': message})
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST' or request.method == 'GET':
        logout(request)
        return redirect('home')


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')  # Rediriger vers la page d'accueil après l'inscription
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def liste_livres(request):
    livres_liste = Livre.objects.all()
    paginator = Paginator(livres_liste, 2)
    page_number = request.GET.get('page')
    livres_page = paginator.get_page(page_number)
    return render(request, 'liste_livres.html', {'livres': livres_page})


@login_required
def detail_livre(request, livre_id):
    livre = get_object_or_404(Livre, pk=livre_id)
    return render(request, 'detail_livre.html', {'livre': livre})


def liste_auteurs(request):
    auteurs = Auteur.objects.all()
    return render(request, 'liste_auteurs.html', {'auteurs': auteurs})


def detail_auteur(request, auteur_id):
    auteur = get_object_or_404(Auteur, pk=auteur_id)
    return render(request, 'detail_auteur.html', {'auteur': auteur})


def liste_categories(request):
    categories = Categorie.objects.all()
    return render(request, 'liste_categories.html', {'categories': categories})


def detail_categorie(request, categorie_id):
    categorie = get_object_or_404(Categorie, pk=categorie_id)
    return render(request, 'detail_categorie.html', {'categorie': categorie})


def liste_utilisateurs(request):
    utilisateurs = Utilisateur.objects.all()
    return render(request, 'liste_utilisateurs.html', {'utilisateurs': utilisateurs})


def detail_utilisateur(request, utilisateur_id):
    utilisateur = get_object_or_404(Utilisateur, pk=utilisateur_id)
    return render(request, 'detail_utilisateur.html', {'utilisateur': utilisateur})
