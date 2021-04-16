from django.db import models
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class UserManager(models.Manager):
        def reg_validator(self, postData):
            errors = {}
            if len(postData['first_name']) < 2: 
                errors["first_name"] = "First Name should be at least 2 characters"
            if len(postData['last_name']) < 2:
                errors["last_name"] = "Last Name should be at least 2 characters"
            if len(postData['email']) < 2:
                errors["email"] = "Email should be at least 2 characters"
            if not EMAIL_REGEX.match(postData['email']):
                errors['email'] = ("Invalid email address!")    

            if len(postData['password']) < 8:
                errors["password"] = "Password should be at least 8 characters"
                
            users = User.objects.filter(email = postData['email'])
            if len(users) > 0:
                errors['dup'] = "Email already exist"

            if postData['password']!=postData['confirmpw']:
                errors['noMatch'] = "Passwords does not Match"
            return errors

        def login_validator(self, postData):
            errors = {}
            existing_user = User.objects.filter(email = postData['email'])

            if len(postData['email']) == 0:
                errors['email'] = "Please enter valid email"

            if len(postData['password']) < 8:
                errors['password'] = "Password should be at least 8 characters"
            
            elif len(existing_user) == 0:
                errors['noMatchEmail'] = "Invalid Email or Password"

            elif bcrypt.checkpw(postData['password'].encode(), existing_user[0].password.encode()) !=True:
                errors['password'] = "Invalid Email or Password"

            return errors


class User(models.Model):
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    email = models.CharField(max_length = 50)
    password = models.CharField(max_length = 50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Wall_Message(models.Model):
    message = models.CharField(max_length=255)
    poster = models.ForeignKey(User, related_name='user_messages', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    comment = models.TextField()
    poster = models.ForeignKey(User, related_name='user_comments', on_delete=models.CASCADE)
    wall_message = models.ForeignKey(Wall_Message, related_name="post_comments", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# Create your models here.
