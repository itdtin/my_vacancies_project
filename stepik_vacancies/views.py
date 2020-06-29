from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from .forms import MyUserCreationForm


class MySignupView(CreateView):
    form_class = MyUserCreationForm
    template_name = 'signup.html'

    for field in form_class.base_fields:
        form_class.base_fields[field].widget.attrs = {'class': 'form-control'}

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = MyUserCreationForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data.get('email')
                username = form.cleaned_data.get('username')
                if email and User.objects.filter(email=email).exclude(username=username).exists():
                    form.add_error('email', 'Данный email уже зарегистрирован')
                    return render(request, self.template_name, {'form': form})
                form.save()
                user = authenticate(username=username, password=form.cleaned_data.get('password1'))
                login(request, user)
                return redirect('/')
            elif 'email' not in form.cleaned_data:
                form.add_error('email', 'Неверный формат email')
            elif 'username' not in form.cleaned_data:
                form.errors['username'][0] = 'Пользователь уже существует'
            return render(request, self.template_name, {'form': form})
        else:
            form = MyUserCreationForm()
            return render(request, self.template_name, {'form': form})


class MyLoginView(LoginView):
    form_class = AuthenticationForm
    form_class.base_fields['username'].widget.attrs = {'class': 'form-control'}
    form_class.base_fields['password'].widget.attrs = {'class': 'form-control'}

    redirect_authenticated_user = True
    template_name = 'login.html'
