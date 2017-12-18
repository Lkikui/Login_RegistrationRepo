from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NAME_REGEX = re.compile(r'^[A-Za-z]\w+$')


class UserManager(models.Manager):
    def validate_registration(self, postData):
        errors = []
        if len(postData['first_name']) <= 2 or len(postData['last_name']) <=2:
            errors.append("Name fields must be at least 3 characters")
        if not NAME_REGEX.match(postData['first_name']) or not NAME_REGEX.match(postData['last_name']):
            errors.append("Name fields can only include letters")
        if not EMAIL_REGEX.match(postData['email']):
            errors.append("Invalid email address")
        if User.objects.filter(email=postData['email']).exists():
            errors.append("email already exists")
        if len(postData['password']) <= 7:
            errors.append("Password must be at least 8 characters")
        if postData['pw_confirm'] != postData['password']:
            errors.append("Passwords do not match")
        print postData['password'], postData['pw_confirm']
        print postData['first_name'], postData['last_name']
        print errors
        
        if not errors:
            hash = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            
            user = User.objects.create(
            first_name = postData['first_name'],
            last_name = postData['last_name'],
            email = postData['email'].lower(),
            password = hash
            )
            return user
        return errors
    
    def validate_login(self, postData):
        errors = []
        login_email = postData['login_email']
        if not User.objects.filter(email=postData['login_email']).exists():
            errors.append("email does not exist")
            return errors
        else:
            current_user = User.objects.get(email=postData['login_email'])
        if not bcrypt.checkpw(postData['login_password'].encode(), current_user.password.encode()):
            errors.append("incorrect password")
            return errors
        else:
            return current_user



class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()
    def __str__(self):
        return "<object: {}, {}, {}, {}>".format(self.first_name, self.last_name, self.email, self.password)