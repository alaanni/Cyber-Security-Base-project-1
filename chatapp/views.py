from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from .models import Message
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic



def index(request):
    message_list = Message.objects
    context = {'message_list': message_list}
    return render(request, 'chatapp/index.html', context)

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