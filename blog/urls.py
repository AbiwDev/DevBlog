 
from django.urls import path 
from . import views

app_name = "blog"

urlpatterns = [
    path("",views.IndexView.as_view(),name="index"),
    path("detail/<int:id>/",views.DetailView.as_view(),name="detail"),
    path("rating/<int:value>/<int:id>/",views.SetRating.as_view(),name="set_rating"),
    path("<category_slug>/posts",views.CategoryList.as_view(),name="category_list"),
    path("search/",views.SearchView.as_view(),name="search"),
    path('comment/add/<int:post_id>/',views.add_comment, name='add_comment'),
    path('about/',views.AboutView.as_view(), name='about'),
    path('contact/',views.ContactView.as_view(), name='contact'),
    path('error/',views.ErrorView.as_view(), name='error'),    
]