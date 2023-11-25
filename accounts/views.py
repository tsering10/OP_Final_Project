from django.shortcuts import redirect, render

from django.views.generic import CreateView, TemplateView
from .forms import UserForm
from chef.forms import ChefForm
from .models import User, UserProfile
from django.contrib import messages, auth
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


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
        if user.is_chef:  # Chef role
            return redirect(self.success_chef_url)
        elif user.is_customer:  # Customer role
            return redirect(self.success_customer_url)


class LogoutView(TemplateView):
    def get(self, request):
        auth.logout(request)
        messages.info(request, "You are logged out.")
        return redirect("login")


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
