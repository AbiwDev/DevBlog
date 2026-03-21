from django.contrib import admin
from .models import Category,Tag,Post,Comment,Rating,Contact 


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name","slug"]
    
    prepopulated_fields = {"slug":("name",)}
    
admin.site.register(Comment)    

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name","slug"]
    
    prepopulated_fields = {"slug":("name",)}

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ["name","email","subject","message"]
    
    prepopulated_fields = {"name":("name","email","subject","message")}
            
admin.site.register(Post)
admin.site.register(Rating)
