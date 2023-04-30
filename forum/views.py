from django.shortcuts import render
from django.views.generic import View, ListView, DetailView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages

from .forms import RentForm, CommentForm
from .models import Rent, Comment


def index(request):
    return render(request, 'forum/index.html')


class Forum(ListView):
    model = Rent
    template_name = 'forum/forum.html'
    ordering = ['-date_posted']
    context_object_name = 'rents'


class RentDetail(DetailView):
    model = Rent
    template_name = 'forum/rent.html'
    context_object_name = 'rent'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = context['rent'].comment.all()
        return context