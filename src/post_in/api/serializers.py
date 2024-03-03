from rest_framework.serializers import (IntegerField, CharField, Serializer,
                                        ModelSerializer, HyperlinkedIdentityField, SerializerMethodField, EmailField)
from notes.models import Notes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from django.contrib.auth import get_user_model


class UserSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        queryset = model.objects.all()
        fields = ('id', 'email', 'password', 'name', 'admin')
        extra_kwargs = {'password': {
            'write_only': True
            }
        }

    def create(self, validated_data):
        user = self.Meta.model(**validated_data)
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.set_password(validated_data.pop('password', ''))
        return super().update(instance, validated_data)


class NoteSerializer(ModelSerializer):
    author = SerializerMethodField(read_only=True)

    def get_author(self, obj):
        return str(obj.author.email)

    class Meta:
        model = Notes
        fields = '__all__'


class ThinNoteSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='note_detail')
    author_email = EmailField(source='author.email')

    class Meta:
        model = Notes
        fields = ('id', 'author_email', 'title', 'url')

