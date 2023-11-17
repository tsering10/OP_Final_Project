from django.shortcuts import redirect

from django.views.generic import CreateView
from .forms import UserForm
from django.contrib import messages
from django.contrib.auth import login
from chef.forms import ChefForm
from .models import User, UserProfile


# Create your views here.
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


# def registerChef(request):
#    return render(request, "accounts/registerChef.html")
