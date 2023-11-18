from django.shortcuts import redirect, render

from django.views.generic import CreateView
from .forms import UserForm
from chef.forms import ChefForm
from .models import User, UserProfile
from django.contrib import messages, auth
from django.contrib.auth import login
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import TemplateView


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
        login(self.request, user)
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
            return redirect("home")

        messages.error(self.request, "Invalid chef form")
        return redirect("registerChef")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["v_form"] = self.chef_form_class()
        return context


class LoginView(View):
    template_name = "accounts/login.html"
    success_customer_url = reverse_lazy("customerDashboard")
    success_chef_url = reverse_lazy("chefDashboard")

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(request, "You are already logged in!")
            return self._redirect_to_dashboard(request.user.role)
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(request, "You are already logged in!")
            return self._redirect_to_dashboard(request.user.role)

        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "You are now logged in.")
            return self._redirect_to_dashboard(user.role)
        else:
            messages.error(request, "Invalid login credentials")
            return redirect("login")

    def _redirect_to_dashboard(self, role):
        if role == 1:  # Chef role
            return redirect(self.success_chef_url)
        elif role == 2:  # Customer role
            return redirect(self.success_customer_url)


class LogoutView(TemplateView):
    def get(self, request):
        auth.logout(request)
        messages.info(request, "You are logged out.")
        return redirect("login")


class CustomerDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "accounts/Customerdashboard.html"
    login_url = reverse_lazy("login")

    def test_func(self):
        return self.request.user.role == 2

    def handle_no_permission(self):
        if self.request.user.role == 1:
            return redirect("chefDashboard")
        return super().handle_no_permission()


class ChefDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "accounts/Chefdashboard.html"
    login_url = reverse_lazy("login")

    def test_func(self):
        return self.request.user.role == 1

    def handle_no_permission(self):
        if self.request.user.role == 2:
            return redirect("customerDashboard")
        return super().handle_no_permission()
