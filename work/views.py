from typing import Any
from django.shortcuts import render,redirect
from django.views.generic import View
from work.forms import *
from work.models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.utils.decorators import method_decorator


def signin_required(fn):
    def wrapper(request,**kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        else:
            return fn(request,**kwargs)
    
    return wrapper


def mylogin(fn):
    def wrapper(request,**kwargs):
        id = kwargs.get("pk")
        obj = taskmodel.objects.get(id=id)
        if obj.user != request.user:
            return redirect("login")
        else:
            return fn(request,**kwargs)
    
    return wrapper


class Registration(View):

    def get(self,request,**kwargs):
        form = Register()

        return render(request,"register.html",{"form":form})
    
    def post(self,request,**kwargs):
        form = Register(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)

            return redirect("login")
        else:
            form = Register()
            return render(request,"register.html",{"form":form})
        

class Signin(View):

    def get(self,request,**kwargs):
        form = LoginForm()

        return render(request,"login.html",{"form":form})
    
    def post(self,request,**kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            # getting username and password from cleaned_data
            u_name = form.cleaned_data.get("username")
            pwd = form.cleaned_data.get("password")

            user_obj = authenticate(username=u_name,password=pwd)           # only authenticate encrypted password
            
            # checking if username password are valid in the table auth_user
            if user_obj:
                print("valid credentials")
                # if true passing the user_obj to login function
                login(request,user_obj)
                # form = Register()
                return redirect("index")
            else:
                form = LoginForm()
                return render(request,"login.html",{"form":form})
            

@method_decorator(signin_required,name="dispatch")
class Add_task(View):

    def get(self,request,**kwargs):
        form = TaskForm()
        data = taskmodel.objects.filter(user=request.user).order_by('completed')

        return render(request,"index.html",{"form":form,"data":data})
    
    def post(self,request,**kwargs):
        form = TaskForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user           # request.user -> details of user that loginned
            form.save()
            messages.success(request,"Task added successfully")

        form = TaskForm()
        data = taskmodel.objects.filter(user=request.user).order_by('completed')
        return render(request,"index.html",{"form":form,"data":data})


@method_decorator(signin_required,name="dispatch")
@method_decorator(mylogin,name="dispatch")
class Delete_task(View):

    def get(self,request,**kwargs):
        id = kwargs.get("pk")
        taskmodel.objects.get(id=id).delete()
        messages.success(request,"Task deleted successfully")

        return redirect("index")
    

@method_decorator(signin_required,name="dispatch")
@method_decorator(mylogin,name="dispatch")
class Task_edit(View):

    def get(self,request,*args,**kwargs):
        id = kwargs.get("pk")
        data = taskmodel.objects.get(id=id)

        if data.completed==False:
            data.completed=True
            data.save()
        else:
            data.completed=False
            data.save()

        return redirect("index")
    

class Signout(View):

    def get(self,request):
        logout(request)

        return redirect("login")
    

class Delete_user(View):

    def get(self,request,**kwargs):
        id = kwargs.get("pk")
        User.objects.get(id=id).delete()

        return redirect("login")
    

class Update_user(View):

    def get(self,request,**kwargs):
        id = kwargs.get("pk")
        data = User.objects.get(id=id)
        form = Register(instance=data)

        return render(request,"register.html",{"form":form})