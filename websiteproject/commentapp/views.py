from django.shortcuts import render,redirect
from indexapp.models import MovieDetail
from myaccount.models import Account
from .models import Comment

# Create your views here.

def add_comment(request,id):
    if request.method=='POST':
        comment_text=request.POST['comment']
        movie=MovieDetail.objects.get(id=id)
        user=request.user
        CommentData=Comment.objects.create(comment_text=comment_text,User=user,Movie=movie)
        CommentData.save()

        return redirect("details",slug=movie.slug)