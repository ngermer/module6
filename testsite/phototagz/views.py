from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.template import RequestContext
from django.utils import timezone
from django import forms
from phototagz.models import Image, Tag, ImgTagRel
# Create your views here.

def index(request):
  tags = Tag.objects.all().order_by('-count')
  return render_to_response('phototagz/index.html',
      {'tags': tags,
       'user': request.user})

class ImageAddForm(forms.Form):
  url = forms.CharField(label="Image URL", max_length=200)
  tag = forms.CharField(label="Tag", max_length=50)

def imageaddformview(request):
  if request.method == 'POST':
    form = ImageAddForm(request.POST)
    if form.is_valid():
      url = form.cleaned_data['url']
      tag = form.cleaned_data['tag']
      pub_date = timezone.now()

      current_image = Image(url=url, pub_date=pub_date)
      current_image.save()

      if Tag.objects.filter(name=tag):
        t = Tag.objects.get(name=tag)
      else:
        t = Tag(name=tag, count=0)
        t.save()

      #create relationship, if it doesn't exist
      if not ImgTagRel.objects.filter(image=current_image, tag=t):
        itr = ImgTagRel(image=current_image, tag=t)
        itr.save()
        t.count += 1
        t.save()

      return redirect('/photo/tag/'+str(t.pk)+'/0')
  else:
    form = ImageAddForm()
  
  return render_to_response('phototagz/addimage.html',
      {'form':form},
      RequestContext(request))

class TagAddForm(forms.Form):
  tag = forms.CharField(label="Tag", max_length=50)

def tagview(request, tag_id, image_id):
  current_tag = Tag.objects.get(pk=tag_id)
  relationships = ImgTagRel.objects.filter(tag=current_tag)

  if (int(image_id) == current_tag.count-1):
    nextimage = '/photo/tag/'+tag_id+'/0'
  else:
    nextimage = '/photo/tag/'+str(tag_id)+'/'+str((1+int(image_id)))

  current_image = relationships[current_tag.count-int(image_id)-1].image

  #handle posted form:
  if request.method == 'POST':
   tag_form = TagAddForm(request.POST)
   if tag_form.is_valid():
    tag = tag_form.cleaned_data['tag']
    if Tag.objects.filter(name=tag):
      t = Tag.objects.get(name=tag)
    else:
      t = Tag(name=tag, count=0)
      t.save()

    #create relationship, if it doesn't exist
    if not ImgTagRel.objects.filter(image=current_image, tag=t):
      itr = ImgTagRel(image=current_image, tag=t)
      itr.save()
      t.count += 1
      t.save()

  else:
    tag_form = TagAddForm()

  image_tags = ImgTagRel.objects.filter(image=current_image)
  
  return render_to_response('phototagz/photoview.html',
      {'current_tag': current_tag,
       'next': nextimage,
       'image': current_image.url,
       'tags': image_tags,
       'user': request.user,
       'tag_form': tag_form},
      RequestContext(request)) 

#
# Registration form!
#

class RegisterForm(UserCreationForm):
  email = forms.EmailField(label="Email")

  class Meta:
    model = User
    fields = ("username","email",)

def register_user_form(request, *args, **kwargs):
  user_form=RegisterForm(request.POST)
  if user_form.is_valid():
    username = user_form.clean_username()
    password = user_form.clean_password2()
    user_form.save()
    user=authenticate(username=username, password=password)
    login(request, user)
    return redirect("/photo/")
  return render_to_response('phototagz/register.html', {'form':user_form}, RequestContext(request))

