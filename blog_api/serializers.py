from rest_framework import serializers
from blog.models import Note, Comment
import datetime, time

def note_to_json(note) -> dict:
    return {
        "id": note.id,
        "title": note.title,
        "message": note.message,
        "public": note.public
    }

def note_created(note) -> dict:
    return {
        "id": note.id,
        "title": note.title,
        "message": note.message,
        "public": note.public,
        "create_at": note.create_at,
        "update_at": note.update_at
    }

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        #fields = "__all__" # Так выбираем все поля модели
        #fields = ("title", "message", "author") # Так выбираем только нужные поля
        exclude = ("public",) # Так выбираем все поля, кроме перечисленных
        read_only_fields = ("author",) #Делаем поле доступным только для чтения

    def to_representation(self, instance):
        """Переформатирование вывода даты в ответе"""
        ret = super().to_representation(instance)
        # Конвертируем строки в старом формате в даты
        date_str_create = time.strptime(ret['create_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
        date_str_update = time.strptime(ret['update_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
        # Конвертируем даты обратно в строки, но уже по новому формату
        str_date_create = time.strftime('%d %B %Y %H:%M:%S', date_str_create)
        str_date_update = time.strftime('%d %B %Y %H:%M:%S', date_str_update)
        #Записываем в наши поля значения дат в новом формате
        ret['create_at'] = str_date_create
        ret['update_at'] = str_date_update
        return ret

class CommentSerializer(serializers.ModelSerializer):

    rating = serializers.SerializerMethodField('get_rating')

    def get_rating(self, obj: Comment):
        return {
            "value": obj.rating,
            "display": obj.get_rating_display()
        }

    class Meta:
        model = Comment
        fields = "__all__" # Так выбираем все поля модели

class NoteDetailSerializer(serializers.ModelSerializer):
    """Сериалайзер для одного сообщения блога"""
    author = serializers.SlugRelatedField(
        slug_field="username", # Создаем новое поле для отображения
        read_only = True # Поле только для чтения
    )

    comments = CommentSerializer(many = True, read_only = True)

    class Meta:
        model = Note
        fields = ("title", "message", "create_at", "update_at", "public", # Эти поля берем из модели
                  "author", "comments") # Эти поля берем из сериализатора

    def to_representation(self, instance):
        """Переформатирование вывода даты в ответе"""
        ret = super().to_representation(instance)
        # Конвертируем строки в старом формате в даты
        date_str_create = time.strptime(ret['create_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
        date_str_update = time.strptime(ret['update_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
        # Конвертируем даты обратно в строки, но уже по новому формату
        str_date_create = time.strftime('%d %B %Y %H:%M:%S', date_str_create)
        str_date_update = time.strftime('%d %B %Y %H:%M:%S', date_str_update)
        #Записываем в наши поля значения дат в новом формате
        ret['create_at'] = str_date_create
        ret['update_at'] = str_date_update
        return ret
