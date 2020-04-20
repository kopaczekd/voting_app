from django.contrib import admin
from .models import Question, Choice


class ChoiceAdmin(admin.TabularInline):
    model = Choice
    extra = 1


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):

    list_display = ('question_text', 'pub_date', 'is_recent')
    list_display_links = ('question_text', 'pub_date')
    fieldsets = [
        (None, {'fields': ['question_text']}),
        (None, {'fields': ['pub_date']})
    ]
    inlines = [ChoiceAdmin]
    search_fields = ['question_text']


# It works the same as: "@admin.register(Question)" before changed class
# admin.site.register(Question, QuestionAdmin)





