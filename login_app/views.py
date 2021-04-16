from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

def index(request):
    request.session.clear()
    return render(request, 'index.html')

def register(request):
    if request.method == "POST":
        errors = User.objects.reg_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request,value)
            return redirect('/')
        else:
            pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()

            newUser = User.objects.create(
                first_name = request.POST['first_name'],
                last_name = request.POST['last_name'],
                email = request.POST['email'],
                password = pw_hash,
                )
            request.session['userID'] = newUser.id

            return redirect('/success')
    return redirect('/')

def success(request):
    if 'userID' not in request.session:
        return redirect('/')
    current_user = User.objects.filter(id=request.session['userID'])
    context = {
        'user': current_user[0],
        'wall_messages': Wall_Message.objects.all()
    }
    return render(request, 'success.html', context) 

def login(request):
    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request,value)
            return redirect('/')
        current_user = User.objects.filter(email=request.POST['email'])
        request.session['userID'] = current_user[0].id
        return redirect('/success') 
    return redirect('/')


def logout(request):
    request.session.clear()
    return redirect('/')

def post_message(request):
    Wall_Message.objects.create(message=request.POST['message'], poster=User.objects.get(id=request.session['userID']))
    return redirect('/success')

def post_comment(request, user_id):
    poster=User.objects.get(id=request.session['userID'])
    message = Wall_Message.objects.get(id=user_id)
    Comment.objects.create(comment=request.POST['comment'], poster=poster, wall_message=message)
    return redirect('/success')

def user_profile(request, user_id):
    context = {
        'user': User.objects.get(id=user_id)
    }
    return render(request, 'user_profile.html', context)

# Create your views here.
