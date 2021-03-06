from rest_framework import serializers
from django.contrib.auth.models import User
from items.models import Item, FavoriteItem


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        new_user = User(username=username, first_name=first_name, last_name=last_name)
        new_user.set_password(password)
        new_user.save()
        return validated_data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [ 'first_name', 'last_name']


class FavouritedSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteItem
        fields = ['user']


class ItemListSerializer(serializers.ModelSerializer):
    added_by = UserSerializer()
    detail = serializers.HyperlinkedIdentityField(
        view_name = "api-detail",
        lookup_field = "id",
        lookup_url_kwarg = "item_id"
        )
    favourited = serializers.SerializerMethodField()
    class Meta:
        model = Item
        fields = ['name', 'detail', 'added_by', 'favourited']

    def get_favourited(self, obj):
        return len(obj.who_faved.all())


class ItemDetailSerializer(serializers.ModelSerializer):
    favourited_by = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = ['name', 'description', 'added_by', 'favourited_by', 'image']


    def get_favourited_by(self, obj):
        users = obj.who_faved.all()
        user_json = FavouritedSerializer(users, many=True).data
        return user_json
