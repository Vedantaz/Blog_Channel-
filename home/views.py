from django.db.models import query
from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact
from django.contrib.auth.models import User
from django.contrib import messages
from blog.models import Post
from django.contrib.auth import authenticate, login, logout

# from django.contrib.auth.models import
# Create your views here.

#   This is HTML pages .


def home(request):
    # //fetch top 3 posts based on number of views
    context = {}
    return render(request, 'home/home.html', context)


def about(request):
    return render(request, 'home/about.html')


def contact(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        if len(name) < 2 or len(email) < 3 or len(phone) < 10 or len(content) < 4:
            messages.error(request, "Please fill the form correctly")
        else:
            contact = Contact(name=name, email=email,
                              phone=phone, content=content)
            contact.save()
            messages.success(
                request, "Your message has been successfully sent")
    return render(request, "home/contact.html")


def search(request):
    # for line no. 37:  query  the request did by the user or client server
    query = request.GET["query"]
    if len(query) > 57:
        allPosts = Post.objects.none()
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent)

    if allPosts.count() == 0:
        messages.warning(
            request, "No search result found , search correctly as per requirement.  .")
    params = {'allPosts': allPosts, 'query': query}
    return render(request, "home/search.html", params)
    # return HttpResponse("This is search ")

#             Authentication THIS IS API'S


def handleSignup(request):
    if request.method == "POST":
        # Get the post parameters

        # it is dict , in which class ==username  as corrresponding  ad will store in username == class

        username = request.POST['username']
        email = request.POST['email']
        fname = request.POST['fname']
        lname = request.POST['lname']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # check for errorneous input

        # username sholud be under 10 characters
        if len(username) > 10:
            messages.error(request, "Username must be under 10 characters")
            return redirect('home')

            # username sholud be alphanumeric
        if not username.isalnum():
            messages.error(
                request, "Username should only contain letters and numbers ")
            return redirect('home')

            # passwords should be matched
        if (pass1 != pass2):
            messages.error(request, "Passwords are not matching ")
            return redirect('home')

        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, " Your iCoder has been successfully created")
        return redirect('home')

    else:
        return HttpResponse("404 - Not found")


def handleLogin(request):
    if request.method == "POST":
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']
        user = authenticate(username=loginusername, password=loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully logged In .")
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials, Please try again .")
            return redirect("home")

    return HttpResponse("404 - Not found")


def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out .")
    return redirect('home')
