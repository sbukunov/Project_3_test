from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from blog.models import Note
from . import serializers

class NoteListCreateAPIView(APIView):
    """Представление, которое позволяет вывести весь список и добавить новую запись"""
    def get(self, request: Request):
        objects = Note.objects.all()
        return Response([serializers.note_to_json(obj)
                         for obj in objects])

    def post(self, request: Request):
        data = request.data #Получаем данные из запроса
        note = Note(**data) #Формируем python-объект с помощью конструктора класса Note
        note.save(force_insert=True) #Сохраняем наш объект в БД (force_insert - только для вновь создаваемого объекта)
        return Response(serializers.note_created(note),
                        status=status.HTTP_201_CREATED)

class NoteDetailAPIView(APIView):
    """Представление, которое позволяет вывести отдельную запись"""
    def get(self, request, pk):
        #try: #Так обычно не делают
            #note = Note.objects.get(pk=pk)
        #except Note.DoesNotExist:
            #return Response(..., status=status.HTTP_404_NOT_FOUND)
        #note = Note.objects.get(pk=pk)
        note = get_object_or_404(Note, pk=pk) #Обычно делают так
        return Response(serializers.note_to_json(note))

    def put(self, request, pk):
        data = request.data  # Получаем данные из запроса
	#note = Note.objects.get(pk=pk) #Получаем python-объект из базы данных по pk
        note = get_object_or_404(Note, pk=pk) #Получаем python-объект из базы данных по pk (так правильнее)
        note.title = data["title"] #Изменяем все обязательные поля
        note.message = data["message"]
        note.public = data["public"]
        note.save()  # Сохраняем наш объект в БД
        return Response(serializers.note_created(note),
                        status=status.HTTP_200_OK)

    def putch(self, request):
        ...