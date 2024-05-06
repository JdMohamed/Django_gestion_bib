import datetime
import jwt
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from bib_app.models import Livre, Auteur, Categorie, User
from .serializers import UserSerializer, LivreSerializers, AuteurSerializers, CategorieSerializers

from rest_framework.exceptions import AuthenticationFailed


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class UpdateView(APIView):
    def put(self, request):
        email = request.data['email']
        user = User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('User not found')
        if(user.is_superuser):
            user.is_superuser=False
        else:
            user.is_superuser=True
        user.save();
        serializer = UserSerializer(user)
        return Response(serializer.data)


class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')

        payload = {
            'id': user.id,
            'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat':datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret' , algorithm='HS256')

        response = Response()
        response.set_cookie(key='myToken', value=token, httponly=True, samesite="none", secure= True)
        serializer = UserSerializer(user)
        response.data = {
            'myToken': token,
            'user':serializer.data
        }

        return response




class UserView(APIView):
    def get(self,request):
        data= request.COOKIES
        token = request.COOKIES.get('myToken')
        print(data)
        print(token)
        if not token:
            raise AuthenticationFailed('Unanthorized')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unanauthencated')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class LogoutView(APIView):
    def post(self,request):
        response = Response()
        response.delete_cookie('myToken')
        response.delete_cookie('jwt')
        response.delete_cookie('csrftoken')
        response.data = {
            'message': 'success'
        }
        return response

class UsersView(APIView):
    def get(self,request):
        users=User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class AuteursViewSet(viewsets.ModelViewSet):
    serializer_class = AuteurSerializers

    def get_queryset(self):
        auteur = Auteur.objects.all()
        return auteur


class CategoriesViewSet(viewsets.ModelViewSet):
    serializer_class = CategorieSerializers

    def get_queryset(self):
        categorie = Categorie.objects.all()
        return categorie


class LivresViewSet(viewsets.ModelViewSet):
    serializer_class = LivreSerializers


    def get_queryset(self):
        livre = Livre.objects.all()
        print(livre)
        return livre

    def create(self, request, *args, **kwargs):
        data = request.data
        new_livre = Livre.objects.create(titre=data["titre"], isbn=data["isbn"], synopsis=data["synopsis"])
        new_livre.save()
        for auteur in data["auteurs"]:
            auteur_obj = Auteur.objects.get(nom=auteur["nom"])
            new_livre.auteurs.add(auteur_obj)
        for categorie in data["categories"]:
            cat_obj = Categorie.objects.get(nom=categorie["nom"])
            new_livre.categories.add(cat_obj)

        serializer = LivreSerializers(new_livre)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        livre_object = self.get_object()
        data = request.data
        livre_object.auteurs.clear()
        livre_object.categories.clear()
        for auteur in data["auteurs"]:
            auteur_obj = Auteur.objects.get(nom=auteur["nom"])
            livre_object.auteurs.add(auteur_obj)
        for categorie in data["categories"]:
            cat_obj = Categorie.objects.get(nom=categorie["nom"])
            livre_object.categories.add(cat_obj)
        livre_object.titre = data["titre"]
        livre_object.isbn = data["titre"]
        livre_object.synopsis = data["titre"]
        livre_object.save()
        serializer = LivreSerializers(livre_object)
        return Response(serializer.data)


"""
@api_view(["GET", "POST"])
def livre_list_create_api_view(request):
    if request.method == "GET":
        livres = Livre.objects.all()
        serializer = LivreSerializers(livres, many = True)
        #json = JSONRenderer().render(serializer.data)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = LivreSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
"""
