from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"

class DreamVacation(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='vacation_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    @property
    def total_interactions(self):
        comments_count = self.comments.count()
        total_upvotes = sum(comment.upvotes for comment in self.comments.all())
        return comments_count + total_upvotes
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    vacation = models.ForeignKey(DreamVacation, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    upvotes = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-upvotes', '-created_at']