from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView
from shop.models import Category,Products
from unicodedata import category


class Home(ListView):
    model=Category
    template_name="categories.html"
    context_object_name="cat"

class Productview(DetailView):
    model=Category
    template_name="product.html"
    context_object_name="cat"


class Detailview(DetailView):
    model=Products
    template_name = "productdetail.html"
    context_object_name = "pro"

from django.contrib.auth.models import User
from django.urls import reverse_lazy
from shop.forms import Registerform

class Register(CreateView):
    model=User
    # fields=['username','password','email','first_name','last_name']
    form_class = Registerform
    template_name="register.html"
    success_url=reverse_lazy('shop:login')

    def form_valid(self,form):
        u=form.cleaned_data['username']
        p=form.cleaned_data['password']
        e=form.cleaned_data['email']
        f=form.cleaned_data['first_name']
        l=form.cleaned_data['last_name']

        u=User.objects.create_user(username=u,password=p,email=e,first_name=f,last_name=l)
        u.save()
        return redirect('shop:login')

from django.contrib.auth.views import LoginView
class Login(LoginView):
    template_name="login.html"
    success_url = reverse_lazy('shop:home')


from django.contrib.auth import logout
from django.views.generic import View

class Logout(View):
    def get(self,request):
        logout(request)
        return redirect('shop:login')


class Addcategories(CreateView):
    model=Category
    fields=['name','desc','image']
    template_name="addcategory.html"
    success_url=reverse_lazy('shop:home')

class Addproduct(CreateView):
    model=Products
    fields=['name','desc','image','price','stock','category']
    template_name="addproduct.html"
    success_url=reverse_lazy('shop:home')

class Addstock(UpdateView):
    model=Products
    fields=['stock']
    template_name="addstock.html"
    success_url=reverse_lazy('shop:home')






