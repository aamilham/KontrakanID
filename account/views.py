from django.shortcuts import render
from django.views import View
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView


class MyRegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'account/register.html', {'form': form})
    
    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid(): 
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account {username} created successfully. Please log in.')
            return redirect('account:login')
        return render(request, 'account/register.html', {'form': form})
    

class MyLoginView(LoginView):
    authentication_form = AuthenticationForm
    template_name = 'account/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('forum:index')
    
    def form_invalid(self, form):
        messages.warning(self.request,'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))
