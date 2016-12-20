#_*_coding:utf-8_*_
from django import forms
from rango.models import Page,Category,UserProfile
from django.contrib.auth.models import User
#栏目表单
class CategoryForm(forms.ModelForm):
	name=forms.CharField(max_length=128,help_text="Please enter the category name.")
	views=forms.IntegerField(widget=forms.HiddenInput(),initial=0)
	links=forms.IntegerField(widget=forms.HiddenInput(),initial=0)
	slug=forms.CharField(widget=forms.HiddenInput(),required=False)
	#An inline class to provide additional information on the form
	class Meta:
		#provide an association between the ModelForm and a model
		model=Category
		fields=('name',)
#页面表单
class PageForm(forms.ModelForm):
	title=forms.CharField(max_length=128,help_text="Please enter the title of the page.")
	url=forms.URLField(max_length=200,help_text="Please enter the URL of the page.")
	views=forms.IntegerField(widget=forms.HiddenInput(),initial=0)

	class Meta:
		#provide an association between the ModelForm and model
		model=Page
		
		#What fields do we want to include in our form?
		#This way we don't need every field in the model present
		#Some fields may allow NULL values so we may not want include them
		#Here,we are hiding the foreign key
		#We can either exclude the category field from the form
		exclude=('category',)
		#or specify the fields to include (i.e. not include the category field)
		#field=('title','url','views')
	def clean(self):
		cleaned_data=self.cleaned_data
		url=cleaned_data.get('url')
		
		if url and not url.startswith('https://'):
			url='https://'+url
			cleaned_data['url']=url
		return cleaned_data		
#用户表单
class UserForm(forms.ModelForm):
	password=forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model=User
		fields=('username','email','password')

class UserProfileForm(forms.ModelForm):
	class Meta:
		model=UserProfile
		fields=('website','picture')
