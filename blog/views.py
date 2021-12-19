
from django. http . response import HttpResponse
from django. shortcuts import render, redirect

from django.contrib import messages
from blog.models import Post, BlogComment
from blog.templatetags import extras
# Create your views here


def blogHome(request):
    # all object will automatically pull by this message
    allPosts = Post.objects.all()
    print(allPosts)
    context = {'allPosts': allPosts}

    return render(request, 'blog/blogHome.html', context)


def blogPost(request, slug):
    # or you can write as :  post = Post.objects.filter(slug=slug).first()
    post = Post.objects.filter(slug=slug).first()
    post.views = post.views + 1
    post.save()
    # to show the original comment , not replies in place of original comment .
    comments = BlogComment.objects.filter(post=post, parent=None)
    # to exclude the original comment ,only replies are considered.
    replies = BlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict = {}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno] = [reply]
        else:
            replyDict[reply.parent.sno].append(reply)

    context = {'post': post, 'comments': comments,
               'user': request.user, 'replyDict': replyDict}
    return render(request, "blog/blogPost.html", context)
    # return HttpResponse(f'This is blogpost : {slug}')


def postComment(request):
    if request.method == "POST":
        comment = request.POST.get('comment')
        user = request.user
        postSno = request.POST.get('postSno')
        post = Post.objects.get(sno=postSno)
        timeStamp = request.POST.get('timeStamp')
        parentSno = request.POST.get('parentSno')
        if parentSno == "":
            comment = BlogComment(comment=comment, user=user, post=post)
            comment.save()
            messages.success(
                request, "Your comment has been posted successfully")
        else:
            parent = BlogComment.objects.get(sno=parentSno)
            comment = BlogComment(
                comment=comment, user=user, post=post, parent=parent)
            comment.save()
            messages.success(
                request, "Your reply has been posted successfully")
    return redirect(f"/blog/{post.slug}")
