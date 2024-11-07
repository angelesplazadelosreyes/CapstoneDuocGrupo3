from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserLoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
import re

def home(request):
    login_form = UserLoginForm()
    return render(request, 'home.html', {'form': login_form})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created! You can now log in using the modal.')
            return redirect('home')  # Redirigir a la página de inicio
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})



def login_view(request):
    form = UserLoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Welcome back!')
                return redirect('dashboard')  # Redirige a la vista para usuarios registrados
            else:
                messages.error(request, 'Invalid username or password')
    return render(request, 'users/login.html', {'form': form})



@login_required
def dashboard(request):
    return render(request, 'users/dashboard.html')



def logout_view(request):
    logout(request)
    return redirect('home')



def custom_password_reset(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        username = request.POST.get('username')
        try:
            user = User.objects.get(username=username)
            email = user.email
            masked_email = re.sub(r'(?<=.).(?=.*@)', '*', email)

            # Generar el enlace de restablecimiento de contraseña
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            domain = request.get_host()
            protocol = 'https' if request.is_secure() else 'http'

            # Renderizar la plantilla del correo
            email_body = render_to_string('registration/password_reset_email.html', {
                'protocol': protocol,
                'domain': domain,
                'uid': uid,
                'token': token,
            })

            # Enviar el correo
            send_mail(
                'Recuperación de Contraseña',
                email_body,
                'from@example.com',
                [email],
                fail_silently=False,
            )

            return JsonResponse({'success': True, 'email': masked_email})
        except User.DoesNotExist:
            return JsonResponse({'success': False})
    return JsonResponse({'success': False})
