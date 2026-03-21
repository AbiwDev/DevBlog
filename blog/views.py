from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.views import View
from .models import Category,Post,Tag,Comment,Rating,Contact
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages 
from .utils import check_read_articles

    
class IndexView(View):    
    def get(self, request):
        categories = Category.objects.all()
        posts = Post.objects.all()

        paginator = Paginator(posts, 3)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        last_comments = Comment.objects.order_by("-id")[:10]
        tags = Tag.objects.all()

        return render(request, "index.html", {
            "categories": categories,
            "page_obj": page_obj,
            "tags": tags,
            "last_comments": last_comments,
        })
    
        return render(request=request, template_name="index.html",context=data)

class DetailView(View):
    def get(self, request, id):
        tags = Tag.objects.all()
        categories = Category.objects.all()
        post = Post.objects.filter(id=id).first()

        if not post:
            return redirect("blog:error")

        posts_count = []
        for cat in categories:
            posts_count.append({
                "name": cat.name,
                "count": Post.objects.filter(category=cat).count()
            })

        read_articles = check_read_articles(request)
        if post.id not in read_articles:
            read_articles.append(post.id)
            post.views += 1
            post.save()

        return render(request, "detail.html", {
            "post": post,
            "categories": categories,
            "tags": tags,
            "posts": posts_count
        })

    def post(self, request, id):
        post = Post.objects.filter(id=id).first()
        if not post:
            return redirect("blog:error")

        name = request.POST.get("name")
        comment = request.POST.get("comment")

        if name and comment:
            Comment.objects.create(
                author=name,
                comment=comment,
                post=post
            )
            messages.success(request, "Successful !")
        else:
            messages.error(request, "Error completed !")

        return redirect("blog:detail", id)
        
                                
class SetRating(View):
    def get(self, request, value, id):
        post = Post.objects.get(id=id)
        value = int(value)
        if all([post,value]):
            Rating.objects.create(post=post)
     
        return HttpResponseRedirect(request.META.get("HTTP_REFERER","/"))


class CategoryList(View):      
    def get(self, request, category_slug):
        category = Category.objects.filter(slug=category_slug).first()
        posts = Post.objects.filter(category=category)
        categories = Category.objects.all()
        last_comments = Comment.objects.order_by("-id")[:10]

        paginator = Paginator(posts, 3)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(request, "index.html", {
            "category":category,
            "page_obj": page_obj,
            "categories": categories,
            "last_comments": last_comments,
        })

                
class SearchView(View):           
    def get(self, request):
        query = request.GET.get("query","")
        posts = Post.objects.filter(title__icontains=query)
        last_comments = Comment.objects.all().order_by("-id")[:10]
    
        paginator = Paginator(posts,2)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number) 
    
        return render(request,"index.html", context={
            "page_obj":page_obj,
            "last_comments": last_comments,
            "query": query
        })  
        

@login_required(login_url='login')
def add_comment(request, post_id):
    post = Post.objects.filter(id=post_id).first()
                
    if request.method == "POST":
        Comment.objects.create(
            post=post,
            user=request.user,
            comment=request.POST.get("comment")
        )
        
    return redirect('blog:detail', post.id) 


class AboutView(View):
    def get(self, request):
        team = [
            {
                "telegram": "https://t.me/Ab1w_dev",
                "instagram": "https://www.instagram.com/ab1w.dev?igsh=Z3BpZDh6cHVqajF6",
                "youtube": "https://www.youtube.com/@Ab1wDev"
            },
 
        ]
        context = {
            "title": "About Us",
            "description": "Programming and techlogiya news",
            "team": team
        }
        
        return render(request, "about.html", context)

        
class ContactView(View):
    def get(self, request):
        return render(request, "contact.html")
 
    def post(self, request):
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")
        contact = Contact.objects.create (
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        messages.success(request,"✔️ Successful")
        return redirect("blog:index")                    
  
class ErrorView(View):
    def get(self, request):
        return render(request, "error.html")
                                 