from django.contrib import admin
from .models import Note, Comment

#admin.site.register(Note)
@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    # Поля для отображения в админке
    list_display = ['title', 'public', 'author', 'create_at', 'update_at']
    # Группировка полей в режиме редактирования
    fields = ('create_at',('title', 'public'), 'message', 'update_at', 'author')
    # Поля только для чтения в режиме редактирования
    readonly_fields = ('create_at', 'update_at')
    # Поиск по выбранным полям
    search_fields = ['title', 'message']
    # Фильтры
    list_filter = ['public', 'author']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    # Поля для отображения в админке
    list_display = ['note', 'author', 'rating']
    list_filter = ['rating', 'author']
    ...

