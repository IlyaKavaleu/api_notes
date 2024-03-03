from django.db.models import (Model, CharField, TextField, DateTimeField, ForeignKey, SET_NULL)
from django.conf import settings


User = settings.AUTH_USER_MODEL


class Notes(Model):
    author = ForeignKey(User, null=True, blank=False, on_delete=SET_NULL)
    title = CharField(max_length=255)
    text = TextField(blank=True)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title}, {self.text}, {self.created}, {self.updated}'

    class Meta:
        ordering = ['-updated']
        verbose_name = 'Note'
        verbose_name_plural = 'Notes'
