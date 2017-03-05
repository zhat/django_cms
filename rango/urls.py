#coding=utf-8
from django.conf.urls import patterns,url
from rango import views

urlpatterns=patterns('',
		url(r'^$',views.index,name='index'),	#首页
		url(r'^about/$',views.about,name='about'),	#about页面
		url(r'^add_category/$',views.add_category,name='add_category'), #添加栏目
		url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$',views.add_page,name='add_page'),#添加页面
		url(r'^category/(?P<category_name_slug>[\w\-]+)$',views.category,name='category'), #栏目页面
	#	url(r'^register/$',views.register,name='register'),#注册
	#	url(r'^login/$',views.user_login,name='login'), #登录
		url(r'^restricted/',views.restricted,name='restricted'),#登录后可以看到
		url(r'^search/',views.search,name='search'),#登录后可以看到
	#	url(r'^logout/$',views.user_logout,name='logout'),#退出登录
		)
		
