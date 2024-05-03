from rest_framework import serializers
from bib_app.models import Auteur, Livre, Categorie, User


class AuteurSerializers(serializers.ModelSerializer):
    class Meta:
        model = Auteur
        fields = ['id', 'nom', 'bio']



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','name','email','password','is_superuser']
        extra_kwargs = {
            'password':{'write_only':True}
        }

    def create(self,validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
class CategorieSerializers(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = ['id', 'nom']


class LivreSerializers(serializers.ModelSerializer):
    class Meta:
        model = Livre
        fields = ['id', 'titre','auteurs','categories', 'isbn', 'synopsis']
        depth = 1


    def create(self, validated_data):
        auteurs_data = validated_data.pop('auteurs', [])
        categories_data = validated_data.pop('categories', [])
        livre = Livre.objects.create(**validated_data)
        for auteur_data in auteurs_data:
            auteur, _ = Auteur.objects.get_or_create(**auteur_data)
            livre.auteurs.add(auteur)
        for categorie_data in categories_data:
            categorie, _ = Categorie.objects.get_or_create(**categorie_data)
            livre.categories.add(categorie)
        livre.save()
        return livre


    def update(self, instance, validated_data):
        instance.titre = validated_data.get('titre',instance.titre)
        instance.auteurs = validated_data.get('auteurs', instance.auteurs)
        instance.categories = validated_data.get('categories', instance.categories)
        instance.isbn = validated_data.get('isbn', instance.isbn)
        instance.synopsis = validated_data.get('synopsis', instance.synopsis)
        instance.save()
        return instance