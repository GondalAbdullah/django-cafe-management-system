from django.contrib import messages
from django.contrib.auth import views as auth_views, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, UpdateView

from .forms import UserRegistrationForm, EmailAuthenticationForm
from .models import Profile
# Create your views here.


class RegisterView(FormView):
    template_name = "users/register.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("users:profile")

    def form_valid(self, form):
        user = form.save()
        # auto-login after registration
        login(self.request, user, backend="users.backends.EmailBackend")
        messages.success(self.request, "Registration successful. Welcome!")
        return super().form_valid(form)
    
# Use Django's LoginView but with our custom auth form
class LoginView(auth_views.LoginView):
    authentication_form = EmailAuthenticationForm
    template_name = "users/login.html"


class LogoutView(auth_views.LogoutView):
    next_page = reverse_lazy("menu:menu_list")


class ProfileView(LoginRequiredMixin, UpdateView):
    """
    Simple profile update view. It updates the Profile model fields.
    It ensures a profile exists for the logged-in user.
    """
    model = Profile
    template_name = "users/profile.html"
    fields = ["phone", "address"]

    def get_object(self, queryset=None):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile
    
    def get_success_url(self):
        messages.success(self.request, "Profile updated.")
        return reverse_lazy("users:profile")




# def register(request):
#     if request.method == "POST":
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             messages.success(request, f'Account created for {username}! You can log in now.')
#             return redirect('login')
#     else:
#         form = UserCreationForm()
#     return render(request, 'users/register.html', {'form': form})
