from django import forms
from django.contrib.auth import get_user_model, password_validation, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserRegistrationForm(forms.ModelForm):
    """
    Simple registration form that asks for email and password twice.
    """

    password1 = forms.CharField(
        label= _("Password"),
        strip = False,
        widget= forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text= password_validation.password_validators_help_text_html(),
    )

    password2 = forms.CharField(
        label = _("Password confirmation"),
        widget = forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip = False,
    )

    class Meta:
        model = User
        fields = ("email", "username", "first_name", "last_name")
    

    def clean_password(self):

        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if not password1 or not password2:
            raise forms.ValidationError(_("Please confirm your password"))
        
        if password1 != password2:
            raise forms.ValidationError(_("Passwords didn't match"))
        
        password_validation.validate_password(password2, self.instance)

        return password2
    
    
    def clean_email(self):
        
        email = self.cleaned_data.get("email")
        
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(_("A user with that email already exitsts."))
        return email.lower()
    

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    

class EmailAuthenticationForm(AuthenticationForm):
    """
    AuthenticationForm that uses 'email' as the username field.
    Keeps the same validation flow but labels the 'username' input as 'Email'.
    """
    username = forms.EmailField(label=_("Email"), widget=forms.EmailInput(attrs={"autfocus": True}))
