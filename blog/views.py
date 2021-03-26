from django.shortcuts import render
from django.http import Http404
from .models import Post, Author, subscribe, Contact, Comment, SubComment
import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

def index(request):

	if request.method == 'GET':
		email = request.GET.get('email')
		if email:
			subscribe(email=email).save()

	week_ago = datetime.date.today() - datetime.timedelta(days = 7)
	trends = Post.objects.filter(time_upload__gte = week_ago).order_by('-read')
	TopAuthors =Author.objects.order_by('-rate')[:2]
	AuthorsPost = [Post.objects.filter(auther = author).first() for author in TopAuthors]

	all_post = Paginator(Post.objects.filter(publish = True),7)
	page = request.GET.get('page')
	try:
		posts = all_post.page(page)
	except PageNotAnInteger:
		posts = all_post.page(1)
	except EmptyPage:
		posts = all_post.page(all_post.num_pages)

	parms = {
		'posts': posts,
		'trends': trends[:2],
		'author_post':AuthorsPost,
		'pop_post': Post.objects.order_by('-read')[:2],
	}
	return render(request, 'index.html', parms)

def profile(request):
	return render(request, 'profile.html')

def about(request):
	parms = {
		'title': 'About | Gyanism',
		'pop_post': Post.objects.order_by('-read')[:2],
		}
	return render(request, 'about.html', parms)

def post(request, id, slug):
	try:
		post = Post.objects.get(pk=id, slug=slug)
	except:
		raise Http404("Post Does Not Exist")	

	post.read+=1
	post.save()

	if request.method == 'POST':
		comm = request.POST.get('comm')
		comm_id = request.POST.get('comm_id') #None

		if comm_id:
			SubComment(post=post,
					user = request.user,
					comm = comm,
					comment = Comment.objects.get(id=int(comm_id))
				).save()
		else:
			Comment(post=post, user=request.user, comm=comm).save()


	comments = []
	for c in Comment.objects.filter(post=post):
		comments.append([c, SubComment.objects.filter(comment=c)])
	
	post_author = post.auther
	if str(post_author) == 'Nisha':
	    post_para = 'Hello! I’m NS , a Bihari who fluently speaks Bhojpuri apart from this , a front end Developer and a blogger.'
	    author_image = '/static/images/person_2.jpg'
	elif str(post_author) == 'Ekesel':
	    post_para = "I am Ekaansh Sahni, You can google me as ekesel. I don't write blogs, I created this! xD"
	    author_image = '/static/images/person_1.jpg'
	elif str(post_author) == 'Shruti':
	    post_para = 'I am Shruti Singh. Currently I am pursuing b.tech CSE. I like writing blogs on social issues in hope that it might bring some changes :P'
	    author_image = '/static/images/person_4.jpg'
	elif str(post_author) == 'Siddharth':
	    post_para = 'I like writing blogs about geopolitical national issues of importance. Further I sketch  imagination and depths of the heart in ensnaring lines! :D'
	    author_image = '/static/images/person_6.jpg'
	elif str(post_author) == 'Astha':
	    post_para = 'Hey! I’m Astha Singh. I’ll be blogging as a mental health blogger. The only demon which really exist is in our head. For that we need a strong mental health. Which we can achieve by keeping a safe distance from negative thoughts. Being a law student I’m very aware of our surroundings. And the only need I see from my vision is a healthy and a strong mental health.'
	    author_image = '/static/images/person_5.jpg'
	elif str(post_author) == 'Malya':
	    post_para = 'Hey I’m Malya Pandey. Being an avid reader and writer, I have always used literature to express myself. I seek therapy in art. Being a patriot and responsible citizen, I love to pen down my views on the latest issues of our country. Besides a writer, I am a dancer and an engineer in the making who loves to travel and wishes to see the entire world someday.'
	    author_image = '/static/images/person_3.jpg'
	elif str(post_author) == 'Aradhana':
	    post_para = 'Sorry, I like to stay anonymous. Read the blog and enjoy'
	    author_image = '/static/images/profile.png'
	else:
	    post_para = 'Sorry, I like to stay anonymous. Read the blog and enjoy'
	    author_image = '/static/images/profile.png'

	parms = {
		'comments':comments,
		'post_author':post_author,
		'post':post,
		'post_para':post_para,
		'author_image':author_image,
		'pop_post': Post.objects.order_by('-read')[:2],
		}
	return render(request, 'blog-single.html', parms)

def contact(request):
	if request.method == 'POST':
		name = request.POST.get('name')
		email = request.POST.get('email')
		mob = request.POST.get('mob')
		mess = request.POST.get('mess','default')
		Contact(name=name,email=email,mob=mob,mess=mess).save()
	parms = {
		'title': 'Contact | Gyanism',
		'pop_post': Post.objects.order_by('-read')[:2],
		}
	return render(request, 'contact.html', parms)

def search(request):
	q = request.GET.get('q')
	if q is None:
		q = ' '
	posts = Post.objects.filter(
		Q(title__icontains = q) |
		Q(overview__icontains = q)
		).distinct()

	parms = {
		'posts':posts,
		'title':'Search Results',
		}

	return render(request, 'search.html', parms)

