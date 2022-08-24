from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    name = models.OneToOneField(User, on_delete=models.CASCADE)
    rate = models.IntegerField(default=0)

    def update_rating(self, id):
        amount = 0
        for i in Post.objects.filter(author_id=id).values('rate'):
            amount += i.get('rate') * 3
        for i in Comment.objects.filter(user_id=id).values('rate'):
            amount += i.get('rate')
        for i in Post.objects.filter(author_id=id):
            for j in Comment.objects.filter(post=i).values('rate'):
                amount += j.get('rate')
        self.rate = amount
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)


class Post(models.Model):
    head = models.CharField(max_length=255, unique=True)
    text = models.TextField()
    rate = models.IntegerField(default=0)
    type = models.BooleanField(default=False)  # False - новость, True - статья
    time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.rate += 1
        self.save()

    def dislike(self):
        self.rate -= 1
        self.save()

    def preview(self):
        prew = self.text[:123] + '...'
        return prew


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    text = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    rate = models.IntegerField(default=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.rate += 1
        self.save()

    def dislike(self):
        self.rate -= 1
        self.save()
