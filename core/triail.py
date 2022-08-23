#models.py File

from django.db import models


class Post(models.Model):
    title= models.CharField(max_length=300, unique=True)
    content= models.TextField()


<html>
<head>
<title>Create a Post </title>
</head>

<body>
<h1>Create a Post </h1>
<form action="" method="POST">
{% csrf_token %}
Title: <input type="text" name="title"/><br/>
Content: <br/>
<textarea cols="35" rows="8" name="content">
</textarea><br/>
<input type="submit" value="Post"/>
</form>
</body>

</html>



from django.shortcuts import render
from .models import Post


def createpost(request):
        if request.method == 'POST':
            if request.POST.get('title') and request.POST.get('content'):
                post=Post()
                post.title= request.POST.get('title')
                post.content= request.POST.get('content')
                post.save()
                
                return render(request, 'posts/create.html')  

        else:
                return render(request,'posts/create.html')


