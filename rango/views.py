#_*_coding:utf-8_*_
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from rango.models import Category,Page
from rango.forms import CategoryForm,PageForm,UserForm,UserProfileForm
from rango.bing_search import run_query
# Create your views here.

def index(request):
	category_list=Category.objects.order_by('-likes')[:5]
	context_dict={'categories':category_list}
	return render(request,'rango/index.html',context_dict)

def category(request,category_name_slug):
#create a context dictionary which we can pass to the template rendering engine
	context_dict={}
	try:
	#Can we find a category name slug with given name?
	#If we can't,the get() method raises a DoseNotExist exception
	#So the get() method returns one model instance or raises an exception.
		category=Category.objects.get(slug=category_name_slug)
		context_dict['category_name']=category.name
	
		#Retrieve all of the associated pages
		#Note that filter returns>=1 model instance.
		pages=Page.objects.filter(category=category)
		#Add our results list to the template context under name pages
		context_dict['pages']=pages
		#We also add the category object from the datebase to the context dictionary
		#We will use this in the template to verify that the category exist
		context_dict['category']=category
		context_dict['category_name_slug']=category_name_slug
	except Category.DoesNotExist:
		#we get here if we didn't find the specified category
		#Don't do anything the template displays the "no category" message for us
		pass

	#Go render the response and return it to the client.

	return render(request,'rango/category.html',context_dict)
#about页面
def about(request):
	about_dict={'aboutText':"This is About context"}
	return render(request,'rango/about.html',about_dict)
#添加栏目
def add_category(request):
	if request.method=='POST':
		form=CategoryForm(request.POST)

		#Have we been provided with a valid form?
		if form.is_valid():
			#Save the new category to the database
			form.save(commit=True)
			#now call the index() view
			#the user will be shown the homepage
			return index(request)
		else:
			#the supplied form contained error just print them to the terminal
			print form.errors
	else:
		form=CategoryForm()
		
		#Bad form (or form details) no form supplied..
		#Render the form with error messages(if any)
	return render(request,'rango/add_category.html',{'form':form})

#添加页面
def add_page(request,category_name_slug):
	try:
		cat=Category.objects.get(slug=category_name_slug)
	except Category.DoesNotExist:
		cat=None

	if request.method=='POST':
		form=PageForm(request.POST)

		if form.is_valid():
			if cat:
				page=form.save(commit=False)
				page.category=cat
				page.views=0
				page.save()	
				return category(request,category_name_slug)
		else:
			print form.errors
	else:
		form=PageForm()
	
	context_dict={'form':form,'category':cat}
	return render(request,'rango/add_page.html',context_dict)

#注册
def register(request):
	registered=False

	if request.method=='POST':
		user_form=UserForm(data=request.POST)
		profile_form=UserProfileForm(data=request.POST)
		
		if user_form.is_valid() and profile_form.is_valid():
			user=user_form.save()

			user.set_password(user.password)
			user.save()
			profile=profile_form.save(commit=False)
			profile.user=user

			if 'picture' in request.FILES:
				profile.picture=request.FILES['picture']

			profile.save()
			registered=True
		else:
			print user_form.errors,profile_form.errors
	else:
		user_form=UserForm()
		profile_form=UserProfileForm()

	context_dict={'user_form':user_form,'profile_form':profile_form,'registered':registered}
	return render(request,'rango/register.html',context_dict)

#登陆
def user_login(request):
	if request.method=='POST':
		username=request.POST.get('username')
		password=request.POST.get('password')

		user=authenticate(username=username,password=password)

		if user:
			if user.is_active:
				login(request,user)
				return HttpResponseRedirect('/rango/')
			else:
				return HttpResponse("Your Rango accout is disable.")
		else:
			print "Invalid login dtails:{0},{1}".format(username,password)
			return HttpResponse("Invalid login details supplied.")
	else:
		return render(request,'rango/login.html',{})
#登录后看到页面
@login_required
def restricted(request):
	return render(request,'rango/restricted.html',{})
#退出登录
@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/rango/')

def search(request):
	result_list=[]

	if request.method=='POST':
		query=request.POST['query'].strip()

		if query:
			result_list=run_query(query)
	return render(request,'rango/search.html',{'result_list':result_list})
