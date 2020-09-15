from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    # dùng hàm này để lấy URL cho khi create hoặc update data xong nó sẽ chuyển hướng đến URL này
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})