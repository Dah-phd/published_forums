from django.contrib import admin
from .models import book, contact
from forum.models import discussion


@admin.register(book)
class BookAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        base_discs = [
            (obj.book, 'General'),
            ('Reviews', 'A place to set your opinion about the topic.'),
            ('Discussion', 'Free talk,centered on the subject at hand.'),
            ('Recomendations',
             'What could be better with the topic and your vision of the next one.'),
            ('Lost and found', 'Random comunity talk.'),
        ]
        for disc in base_discs:
            if not discussion.objects.filter(
                    book__pk=obj.pk, discussion=disc[0]):
                discussion.objects.create(
                    book=obj, discussion=disc[0], description=disc[1])


@admin.register(contact)
class ContactsAdmin(admin.ModelAdmin):
    search_fields = ("email__startswith",)
