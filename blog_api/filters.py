from typing import Optional

from django.db.models import QuerySet
from blog import models

# Это вариант для случая, когда отображаются записи только текущего пользователя
#def note_by_author_id_filter(queryset: QuerySet, author_id: int):
    #return queryset.filter(author_id=author_id)

# Это вариант для случая любого пользователя
def note_by_author_id_filter(queryset: QuerySet, author_id: Optional[int]):
    if author_id is not None:
        return queryset.filter(author_id=author_id)
    else:
        return queryset
#def note_by_author_filter(queryset: QuerySet, user): # Так не работает
    #return queryset.filter(author=user)
