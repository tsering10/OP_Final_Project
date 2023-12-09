from django.shortcuts import redirect, render

from django.views.generic import CreateView, TemplateView
from .forms import UserForm
from efood_main.apps.chef.forms import ChefForm
from .models import User, UserProfile
from django.contrib import messages, auth
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings


def send_verification_email(request, user, mail_subject, email_template):
    from_email = settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)
    message = render_to_string(
        email_template,
        {
            "user": user,
            "domain": current_site,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": default_token_generator.make_token(user),
        },
    )
    to_email = user.email
    mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
    mail.content_subtype = "html"
    mail.send()


class RegisterUserView(CreateView):
    form_class = UserForm
    template_name = "accounts/registerUser.html"

    def form_valid(self, form):
        messages.success(
            self.request,
            "Your account has been\
                          registered sucessfully!",
        )
        user = form.save()
        # Send the verification email
        mail_subject = "Email Verification"
        email_template = "accounts/emails/account_verification_email.html"
        send_verification_email(self.request, user, mail_subject, email_template)
        return redirect("home")


class RegisterChefView(CreateView):
    form_class = UserForm
    chef_form_class = ChefForm
    template_name = "accounts/registerChef.html"
    success_url = "registerChef"

    def form_valid(self, form):
        user = form.save(commit=False)
        user.role = User.CHEF
        user.set_password(form.cleaned_data["password"])
        user.save()

        chef_form = self.chef_form_class(self.request.POST, self.request.FILES)
        if chef_form.is_valid():
            chef = chef_form.save(commit=False)
            chef.user = user
            chef.chef_name = chef_form.cleaned_data["chef_name"]
            user_profile = UserProfile.objects.get(user=user)
            chef.user_profile = user_profile
            chef.save()
            messages.success(
                self.request,
                "Chef account has been\
                          registered sucessfully!",
            )
            # Send verification email
            mail_subject = "Please activate your account"
            email_template = "accounts/emails/account_verification_email.html"
            send_verification_email(self.request, user, mail_subject, email_template)
            messages.success(
                self.request,
                "Your account has been registered sucessfully!\
                      Please wait for the approval.",
            )
            # return redirect("registerVendor")
            return redirect("home")

        messages.error(self.request, "Invalid chef form")
        return redirect("registerChef")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["v_form"] = self.chef_form_class()
        return context


class LoginView(TemplateView):
    template_name = "accounts/login.html"
    success_customer_url = reverse_lazy("customerDashboard")
    success_chef_url = reverse_lazy("chefDashboard")

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(request, "You are already logged in!")
            return self._redirect_to_dashboard(request.user)
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(request, "You are already logged in!")
            return self._redirect_to_dashboard(request.user)

        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "You are now logged in.")
            return self._redirect_to_dashboard(user)
        else:
            messages.error(request, "Invalid login credentials")
            return redirect("login")

    def _redirect_to_dashboard(self, user):
        if user.is_chef:
            return redirect(self.success_chef_url)
        elif user.is_customer:
            return redirect(self.success_customer_url)


class LogoutView(TemplateView):
    def get(self, request):
        auth.logout(request)
        messages.info(request, "You are logged out.")
        return redirect("home")


class ActivateView(TemplateView):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            myuser = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            myuser = None

        if myuser is not None and default_token_generator.check_token(myuser, token):
            myuser.is_active = True
            myuser.save()
            messages.success(request, "Your account has been activated!")
            return redirect("login")
        else:
            messages.error(request, "Invalid activation link")
            return redirect("login")


class ForgotPasswordView(TemplateView):
    template_name = "accounts/forgot_password.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST["email"]
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)
            # send reset password email
            mail_subject = "Reset Your Password"
            email_template = "accounts/emails/reset_password_email.html"
            send_verification_email(self.request, user, mail_subject, email_template)
            messages.success(
                self.request, "Password reset link has been sent to your email address."
            )
            return redirect("login")
        else:
            messages.error(self, request, "Account does not exist")
            return redirect("forgot_password")


class ResetPasswordValidateView(TemplateView):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            myuser = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            myuser = None

        if myuser is not None and default_token_generator.check_token(myuser, token):
            request.session["uid"] = uid
            messages.success(request, "Please reset your password")
            return redirect("reset_password")
        else:
            messages.error(request, "This link has been expired!")
            return redirect("forgot_password")


class ResetPasswordView(TemplateView):
    template_name = "accounts/reset_password.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]
        if password == confirm_password:
            pk = request.session.get("uid")
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, "Password reset successful")
            return redirect("login")
        else:
            messages.error(request, "Password do not match!")
            return redirect("reset_password")


class ChefView(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_chef

    def handle_no_permission(self):
        if self.request.user.is_customer:
            return redirect("customerDashboard")
        return super().handle_no_permission()


class CustomerView(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_customer

    def handle_no_permission(self):
        if self.request.user.is_chef:
            return redirect("chefDashboard")
        return super().handle_no_permission()


class CustDashboardView(CustomerView, TemplateView):
    template_name = "accounts/Customerdashboard.html"


class ChefDashboardView(ChefView, TemplateView):
    template_name = "accounts/Chefdashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["chef"] = self.request.user.chef
        return context
