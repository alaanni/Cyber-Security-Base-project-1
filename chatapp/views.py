from cgi import print_arguments
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from .models import Message, User
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.db import connection
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return render(request, 'chatapp/index.html')

def home(request):
    context = {}

    context["users"] = User.objects.all()

    if 'username' in request.session:
        username = request.session['username']
        # user_id = User.objects.filter(username=filter_username)[0].id
        user_id = User.objects.raw(f"SELECT id, username FROM auth_user WHERE username='{str(username)}' ORDER BY id")[0].id
        messages = Message.objects.filter(user_id=user_id)
    else:
        messages = Message.objects.all()

    context["messages"] = messages

    return render(request, 'home.html', context)

def send(request):
    form = request.POST
    new_content = form["content"]
    current_user = request.user
    new_message = Message(content=new_content, user=current_user)
    new_message.save()
    return redirect("/")


class SignIn(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signin.html"

@csrf_exempt
def filter(request):
    if request.method == 'POST':
        form = request.POST
        username = form["username"]
        request.session['username'] = username
        return redirect("/")