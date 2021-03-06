from rest_framework import serializers, viewsets
from .models import Note
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class NoteSerializer(serializers.HyperlinkedModelSerializer):

    def create(self, validated_data):
        user = self.context['request'].user

        note = Note.objects.create(user=user, **validated_data)
        return note


    class Meta:
        model = Note
        fields = ('title', 'content')

class NoteViewSet(viewsets.ModelViewSet):
    serializer_class = NoteSerializer
    queryset = Note.objects.all()

    def get_queryset(self):
        user = self.request.user
        
        if user.is_anonymous:
            return Note.objects.none()
        else:
            return Note.objects.filter(user=user)

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password' : {'write_only' : True}}

    def create(self, validated_data):
        user = User(username = validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user

