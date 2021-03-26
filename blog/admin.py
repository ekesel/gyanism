from django.contrib import admin
from .models import *
from django.http import HttpResponse
import decimal, csv

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user','rate',)
    search_fields = ('user','rate',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('comm','post','user',)
    list_filter = ('time','post','user',)
    search_fields = ('user','post','time',)

class ContactAdmin(admin.ModelAdmin):
    list_display = ('name','time',)
    list_filter = ('time',)
    search_fields = ('name','email','time',)

class postAdmin(admin.ModelAdmin):
    list_display = ('title','time_upload','publish','read',)
    list_filter = ('auther','time_upload','publish',)
    search_fields = ('auther','title','categories',)
    list_per_page = 15

class subCommentAdmin(admin.ModelAdmin):
    list_display = ('comment','post','user',)
    list_filter = ('time','post','user',)
    search_fields = ('user','post','time',)

def export_subscribe(modeladmin, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="subscribers.csv"'
        writer = csv.writer(response)
        writer.writerow(['email'])
        books = queryset.values_list('email')
        for book in books:
            writer.writerow(book)
        return response
export_subscribe.short_description = 'Export to csv'

class subscriberadmin(admin.ModelAdmin):
    actions=[export_subscribe]


admin.site.register(Post,postAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Categorie)
admin.site.register(subscribe,subscriberadmin)
admin.site.register(Contact,ContactAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(SubComment,subCommentAdmin)