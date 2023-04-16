from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify
from django.urls import reverse

# pip install pillow

class subscribe(models.Model):
	email = models.EmailField()

	def __str__(self):
		return self.email

class Author(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	rate = models.IntegerField(default=0)
	def __str__(self):
		return self.user.username

class Categorie(models.Model):
	title = models.CharField(max_length=20)
	def __str__(self):
		return self.title

class Post(models.Model):
	title = models.CharField(max_length = 50)
	overview = models.TextField()
	slug = models.SlugField(null=True, blank=True)
	body_text = RichTextUploadingField(null=True)
	time_upload = models.DateTimeField(auto_now_add = True)
	auther = models.ForeignKey(Author, on_delete=models.CASCADE)
	thumbnail = models.ImageField(upload_to = 'thumbnails')
	publish = models.BooleanField()
	categories = models.ManyToManyField(Categorie)
	read = models.IntegerField(default = 0)
	keywords = models.CharField(max_length=200,blank=True,null=True)

	class Meta:
		ordering = ['-pk']

	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		self.slug = slugify(self.title)
		super(Post, self).save(*args, **kwargs)
	
	#def get_absolute_url(self):
		#return reverse('blog:post',args=[self.id,self.slug,])


class Contact(models.Model):
	name = models.CharField(max_length=100)
	email = models.EmailField()
	mob = models.CharField(max_length=12)
	mess = models.TextField()
	time = models.DateTimeField(auto_now_add = True)

	def __str__(self):
		return self.name


class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	time = models.DateTimeField(auto_now_add=True)
	comm = models.TextField()

	def __str__(self):
		return self.comm

class SubComment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	time = models.DateTimeField(auto_now_add=True)
	comm = models.TextField()
	comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

class UserDetail(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
	email = models.EmailField()
	image = models.ImageField(upload_to='profile_pics',null=True)
