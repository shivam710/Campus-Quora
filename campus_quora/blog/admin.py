from django.contrib import admin
from .models import Question, Answer

# class PostAdmin(admin.ModelAdmin):
#     list_display = ('title', 'slug', 'status','created_on')
#     list_filter = ("status",)
#     search_fields = ['title', 'content']
#     prepopulated_fields = {'slug': ('title',)}

admin.site.register(Question)
admin.site.register(Answer)