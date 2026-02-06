from django.db import models
from django.urls import reverse
from django.utils import timezone

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="分类名称")

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.CharField(max_length=50, verbose_name="昵称")
    content = models.TextField(verbose_name="留言内容")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}: {self.content[:20]}"


class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="文章标题")
    content = models.TextField(verbose_name="正文")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="创建时间（全球标准时间）"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="文章分类",
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post-detail", args=[str(self.id)])

    @property
    def beijing_created_at(self):
        return timezone.localtime(self.created_at)
