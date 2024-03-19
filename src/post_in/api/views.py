from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from notes.models import Notes
from api.serializers import NoteSerializer, ThinNoteSerializer, UserSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.mixins import (ListModelMixin, CreateModelMixin, RetrieveModelMixin,
                                   UpdateModelMixin, DestroyModelMixin)
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from .permissions import IsAuthor_Or_ReadOnly
from accounts.models import User
from rest_framework.renderers import JSONRenderer


class UserViewList(ListModelMixin, CreateModelMixin, UpdateModelMixin, GenericAPIView):
    model = get_user_model()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser, )

    def get_queryset(self):
        return self.model.objects.all()

    def get(self, request):
        users = self.get_queryset()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError:
            return Response({"detail": "This email is already in use."}, status=status.HTTP_400_BAD_REQUEST)


class UserViewDetail(RetrieveModelMixin, UpdateModelMixin, GenericAPIView, DestroyModelMixin):
    queryset = get_user_model()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if request.user.admin:
            return self.destroy(request, *args, **kwargs)
        else:
            return Response('You can\'t delete users. You haven\'t permissions!', status=status.HTTP_403_FORBIDDEN)


class NoteListView(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = Notes.objects.all()
    serializer_class = NoteSerializer
    permission_classes = (IsAuthor_Or_ReadOnly, )

    # def get(self, request, *args, **kwargs):
    #     notes = self.queryset.filter(author=self.request.user)
    #     thin_serializer_class = ThinNoteSerializer
    #     context = {'request': request}
    #     serializer = thin_serializer_class(notes, many=True, context=context)
    #     return Response(serializer.data)

    def get_queryset(self):
        if self.request.user.admin:
            return self.queryset.all()
        return self.queryset.filter(author=self.request.user)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class NoteDetailView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    queryset = Notes.objects.all()
    serializer_class = NoteSerializer
    permission_classes = (IsAuthor_Or_ReadOnly, )

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    def delete(self, request, pk):
        note = get_object_or_404(Notes, pk=pk)
        if note.author == self.request.user:
            self.destroy(request, pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response('Is not yr entry!')

# class NoteViewSet(ModelViewSet):
#     queryset = Notes.objects.all()
#     serializer_class = NoteSerializer
#
#     def list(self, request, *args, **kwargs):
#         notes = Notes.objects.all()
#         context = {'request': request}
#         serializer = ThinNoteSerializer(notes, many=True, context=context)
#         return Response(serializer.data)


# class NoteListView(ListCreateAPIView):
#     queryset = Notes.objects.all()
#     serializer_class = NoteSerializer
#
#     def list(self, request, *args, **kwargs):
#         context = {'request': request}
#         notes = Notes.objects.all()
#         serializer = ThinNoteSerializer(notes, many=True, context=context)
#         return Response(serializer.data)
#
#
# class NoteDetailView(RetrieveUpdateDestroyAPIView):
#     queryset = Notes.objects.all()
#     serializer_class = NoteSerializer




# class NoteListView(APIView):
#     def get(self, request, format=None):
#         notes = Notes.objects.all()  # queryset
#         context = {'request': request}
#         serializer = ThinNoteSerializer(notes, many=True, context=context)  # queryset give away to NoteSerializer
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def post(self, request, format=None):
#         context = {'request': request}
#         serializer = NoteSerializer(data=request.data, context=context)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class NoteDetailView(APIView):
#     def get_object(self, pk):
#         try:
#            return Notes.objects.get(pk=pk)
#         except Notes.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#
#     def get(self, request, pk, format=None):
#         note = self.get_object(pk)
#         context = {'request': request}
#         serializer = NoteSerializer(note, context=context)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def put(self, request, pk, format=None):
#         note = self.get_object(pk)
#         context = {'request': request}
#         serializer = NoteSerializer(note, data=request.data, context=context)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk, format=None):
#         note = self.get_object(pk)
#         note.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)




# @api_view(['GET', 'POST'])
# def notes_list(request, format=None):
#     if request.method == 'GET':
#         notes = Notes.objects.all()   # queryset
#         serializer = NoteSerializer(notes, many=True)   # queryset give away to NoteSerializer
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     elif request.method == 'POST':
#         serializer = NoteSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def note_detail(request, pk, format=None):
#     try:
#         note = Notes.objects.get(pk=pk)
#     except Notes.DoesNotExist:
#         return Response(status=[status.HTTP_400_BAD_REQUEST or status.HTTP_500_INTERNAL_SERVER_ERROR])
#
#     if request.method == 'GET':
#         serializer = NoteSerializer(note)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     if request.method == 'PUT':
#         serializer = NoteSerializer(note, data=request.data)
#         if serializer.is_valid:
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     if request.method == 'DELETE':
#         note.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
