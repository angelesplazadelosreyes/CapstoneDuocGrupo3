from .forms import CustomAuthenticationForm

def login_form(request):
    return {'login_form': CustomAuthenticationForm()}

