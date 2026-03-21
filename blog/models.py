from django.db import models


class Category(models.Model):
    name = models.CharField(verbose_name="Category name",max_length=200)
    slug = models.SlugField(max_length=200,unique=True)
    
    def __str__(self):
        return str(self.name) 

class Tag(models.Model):
    name = models.CharField(verbose_name="Tag name",max_length=200)
    slug = models.SlugField(max_length=200,unique=True)
                           
    def __str__(self):
        return str(self.name) 

class Post(models.Model):
    title = models.CharField(verbose_name="Post title",max_length=500)
    body = models.TextField(verbose_name="Post body")
    author = models.CharField(verbose_name="Post author",default="Admin",max_length=100)
    category = models.ForeignKey(Category, on_delete=models.PROTECT,related_name="categories")
    image = models.ImageField(upload_to="post_images/", verbose_name="Post Image", blank=True, null=True)
    tag = models.ManyToManyField(Tag)
    views = models.PositiveIntegerField(default=0)
    published_date = models.DateTimeField(verbose_name="Pulished time",auto_now_add=True)
    published = models.BooleanField(default=0)
    on_top = models.BooleanField(default=0)
    
    def get_avg_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            avg = sum([r.value for r in ratings]) / ratings.count()
            return round(avg, 2)
        return 0

    def __str__(self):
        return str(self.title)


class Comment(models.Model):
    author = models.CharField(verbose_name="Post author",default="Admin",max_length=100)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="comments")
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.created_at)

                
class Rating(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name="ratings")
    value = models.PositiveSmallIntegerField(verbose_name="Post rating",default=0)

    def __str__(self):
        return str(self.value)


class Contact(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=30, blank=True, null=True)  
    subject = models.CharField(max_length=20, blank=True, null=True)
    message = models.TextField() 