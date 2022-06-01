from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from blog.models import Note
from . import serializers, filters

class NoteListCreateAPIView(APIView):
    """Представление, которое позволяет вывести весь список и добавить новую запись"""
    def get(self, request: Request):
        objects = Note.objects.all()
        serializer = serializers.NoteSerializer(
            instance = objects,
            many = True
        )
        return Response(serializer.data)
        #return Response([serializers.note_to_json(obj) # "Ручной" Response
                         #for obj in objects])

    def post(self, request: Request):
        #Передаем в сериалайзер данные из запроса
        serializer = serializers.NoteSerializer(data = request.data)

        # Проверка параметров
        if not serializer.is_valid(): # Проверяем "сырые" данные на валидность,
            # поскольку данные пришли от пользователя, а не из БД
            return Response(
                serializer.errors, # Здесь будут все ошибки - отдаем их пользователю
                status = status.HTTP_400_BAD_REQUEST
            )
        #Записываем новую запись в БД и добавляем в качестве автора пользователя из request
        serializer.save(author = request.user) # Передаем в БД пользователя из request
        return Response(
            serializer.data,
            status = status.HTTP_201_CREATED
        )

        #data = request.data #Получаем данные из запроса
        #note = Note(**data) #Формируем python-объект с помощью конструктора класса Note
        #note.save(force_insert=True) #Сохраняем наш объект в БД (force_insert - только для вновь создаваемого объекта)
        #return Response(serializers.note_created(note),
                        #status=status.HTTP_201_CREATED) # "Ручной" Response

class NoteDetailAPIView(APIView):
    """Представление, которое позволяет вывести отдельную запись"""
    def get(self, request, pk):
        note = get_object_or_404(Note, pk=pk) # Получаем ORM-объект по pk
        serializer = serializers.NoteDetailSerializer( # Новый сериализатор
            instance=note, # Здесь не указываем many = True, потому что объект один
        )
        #serializer = serializers.NoteSerializer(  # Старый сериализатор
            #instance=note,  # Здесь не указываем many = True, потому что объект один
        #)
        return Response(serializer.data) #Возвращаем сериализованный JSON-объект
        #try: #Так обычно не делают
            #note = Note.objects.get(pk=pk)
        #except Note.DoesNotExist:
            #return Response(..., status=status.HTTP_404_NOT_FOUND)
        #note = Note.objects.get(pk=pk)
        #note = get_object_or_404(Note, pk=pk) #Обычно делают так
        #return Response(serializers.note_to_json(note))

    def put(self, request, pk):
        note = get_object_or_404(Note, pk=pk) #Получаем python-объект из базы данных по pk
        serializer = serializers.NoteSerializer(
            instance = note, data = request.data
        )
        serializer.is_valid(raise_exception=True) # Проверяем на наличие ошибок
        serializer.save() # Сохраняем обновленный объект в БД
        return Response(serializer.data)
        # data = request.data  # Получаем данные из запроса
        # note = Note.objects.get(pk=pk) #Получаем python-объект из базы данных по pk
        #note.title = data["title"] #Изменяем все обязательные поля
        #note.message = data["message"]
        #note.public = data["public"]
        #note.save()  # Сохраняем наш объект в БД
        #return Response(serializers.note_created(note),
                       #status=status.HTTP_200_OK)

    def patch(self, request, pk):
        note = get_object_or_404(Note, pk=pk)  # Получаем python-объект из базы данных по pk
        serializer = serializers.NoteSerializer(
            instance=note, data=request.data, partial = True
        )
        serializer.is_valid(raise_exception=True)  # Проверяем на наличие ошибок
        serializer.save()  # Сохраняем обновленный объект в БД
        return Response(serializer.data)

    def delete(self, request, pk):
        note = get_object_or_404(Note, pk=pk)  # Получаем python-объект из базы данных по pk
        note.delete() # Удаляем объект из БД
        return Response(status = status.HTTP_204_NO_CONTENT) # Возвращаем сообщение "нет содержимого"


class PublicNoteListAPIView(ListAPIView):
    queryset = Note.objects.all()
    serializer_class = serializers.NoteDetailSerializer # Используем уже существующий сериализатор

    def get_queryset(self):
        queryset = super().get_queryset()
        # user = self.request.user
        return queryset.filter(public=True)

    # Фильтрация
    def filter_queryset(self, queryset):
        queryset = filters.note_by_author_id_filter(
            queryset,
            author_id=self.request.query_params.get("author_id") # Получаем id автора из GET-параметров
            # author_id = self.request.user.id # Получаем id автора из запроса
        )
        return queryset

        # Сортируем записи по убыванию id автора
        def ordering(self, queryset):
            return queryset.order_by("-id")

class UserNoteListAPIView(ListAPIView):
    queryset = Note.objects.all()
    serializer_class = serializers.NoteDetailSerializer # Используем уже существующий сериализатор

    def get_queryset(self, pk):
        queryset = super().get_queryset()
        user = self.request.user
        return queryset.filter(author=user)
        #user = self.request.user
        #return queryset.filter(author = user)