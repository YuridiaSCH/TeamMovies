from django.contrib import admin

from movies.models import Movie, Genre, Job, Person, MovieCredit, MovieReview 

class MovieCreditInline(admin.StackedInline):
    model=MovieCredit
    
class MovieAdmin(admin.ModelAdmin):
    filter_horizontal=('credits',)
    inlines=(MovieCreditInline,)

class MovieCreditAdmin(admin.ModelAdmin):
    search_files=("person__name","movie__title")

admin.site.register(Movie, MovieAdmin)
admin.site.register(Genre)
admin.site.register(Job)
admin.site.register(Person)
admin.site.register(MovieCredit, MovieCreditAdmin)
admin.site.register(MovieReview)
