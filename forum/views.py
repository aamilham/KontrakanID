from typing import Optional
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .forms import RentForm, CommentForm, ConfirmationForm
from .models import Rent, Comment


def index(request):
    return render(request, 'forum/index.html')


class Forum(ListView):
    model = Rent
    template_name = 'forum/forum.html'
    queryset = Rent.objects.filter(is_closed=False)
    ordering = ['-date_posted']
    context_object_name = 'rents'


class RentDetail(DetailView):
    model = Rent
    template_name = 'forum/rent.html'
    context_object_name = 'rent'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = context['rent'].comment.all()
        context['occupants'] = context['rent'].occupant.all()
        context['remainder'] = context['rent'].get_remainder_quota()
        context['user_already_in'] = context['rent'].is_already_in(self.request.user)
        return context
    

class CreateRent(LoginRequiredMixin, CreateView):
    model = Rent
    form_class = RentForm
    template_name = 'forum/create_rent.html'
    success_url = reverse_lazy('forum:forum') 

    def form_valid(self, form):
        rent = form.save(commit=False)
        rent.owner = self.request.user
        rent.save()
        response = super().form_valid(form)
        if 'photo' in self.request.FILES:
            uploaded_file = self.request.FILES['photo']
            rent.photo = uploaded_file
            rent.save()
        return response
    
    def form_invalid(self, form):
        messages.warning(self.request, 'Terdapat kesalahan pada formulir.')
        return super().form_invalid(form)


class CreateComment(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'forum/create_comment.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.rent = Rent.objects.get(pk=self.kwargs.get("pk"))
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('forum:rent', args=[self.kwargs.get("pk")])


class UpdateRent(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Rent
    form_class = RentForm
    template_name = 'forum/update_rent.html'

    def test_func(self):
        rent = self.get_object()
        return self.request.user.pk == rent.owner.pk
    
    def form_valid(self, form):
        response = super().form_valid(form)
        rent = self.get_object()
        rent.close_if_full()
        rent.open_if_not_full()
        return response

    
    def get_success_url(self):
        return reverse_lazy('forum:rent', args=[self.kwargs.get("pk")])
    

class UpdateComment(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'forum/update_comment.html'

    def test_func(self):
        comment = self.get_object()
        return self.request.user.pk == comment.author.pk
    
    def get_success_url(self):
        comment = self.get_object()
        return reverse_lazy('forum:rent', args=[comment.rent.pk])


class JoinRent(View):
    def get(self, request, pk, *args, **kwargs):
        context = {
            'form': ConfirmationForm(),
            'pk': pk
        }
        return render(request, 'forum/join_rent.html', context)
    
    def post(self, request, pk, *args, **kwargs):
        form = ConfirmationForm(request.POST)
        if form.is_valid():
            rent = Rent.objects.get(pk=pk)
            new_occupant = request.user
            if rent.add_occupant(new_occupant):
                messages.success(request, "Berhasil mendaftar ke kontrakan")
            else:
                messages.warning(request, "Gagal mendaftar ke kontrakan, kontrakan penuh atau anda sudah terdaftar")
            return redirect(reverse_lazy('forum:rent', args=[self.kwargs.get("pk")]))
        return redirect(reverse_lazy('forum:rent', args=[self.kwargs.get("pk")]))
    

class UndoRent(View):
    def get(self, request, pk, *args, **kwargs):
        context = {
            'form': ConfirmationForm(),
            'pk': pk
        }
        return render(request, 'forum/undo_rent.html', context)
    
    def post(self, request, pk, *args, **kwargs):
        form = ConfirmationForm(request.POST)
        if form.is_valid():
            rent = Rent.objects.get(pk=pk)
            occupant = request.user
            if rent.is_already_in(occupant):
                rent.delete_occupant(occupant)
                messages.success(request, "Berhasil mengeluarkan anda dari kontrakan")
            else:
                messages.warning(request, "Gagal mengeluarkan anda dari kontrakan")
            return redirect(reverse_lazy('forum:rent', args=[self.kwargs.get("pk")]))
        return redirect(reverse_lazy('forum:rent', args=[self.kwargs.get("pk")]))