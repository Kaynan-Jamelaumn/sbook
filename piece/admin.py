from django.contrib import admin
from .models import  Publisher, Genre#, Piece, Chapter, PageContent, TextContent, ImageContent, Page, Comment

class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)

class PublisherAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'created_at', 'updated_at')

class PieceAdmin(admin.ModelAdmin):
    list_display = ('name', 'isbn', 'published_at', 'type', 'status', 'created_at', 'updated_at')
    list_filter = ('type', 'status', 'genre', 'author')
    search_fields = ('name', 'isbn')
    date_hierarchy = 'published_at'

class ChapterAdmin(admin.ModelAdmin):
    list_display = ('name', 'piece', 'created_at', 'updated_at')
    list_filter = ('piece',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'user', 'created_at', 'updated_at')
    list_filter = ('user', 'piece', 'chapter', 'page')
    search_fields = ('content',)

admin.site.register(Genre, GenreAdmin)
admin.site.register(Publisher, PublisherAdmin)
#admin.site.register(Piece, PieceAdmin)
#admin.site.register(Chapter, ChapterAdmin)
#admin.site.register(Comment, CommentAdmin)
