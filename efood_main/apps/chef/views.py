from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView
from .forms import ChefForm
from efood_main.apps.accounts.forms import UserProfileForm
from .models import Chef
from efood_main.apps.accounts.models import UserProfile
from django.contrib import messages


class ChefProfileView(TemplateView):
    template_name = "chef/chef_profile.html"

    def get(self, request, *args, **kwargs):
        profile = get_object_or_404(UserProfile, user=request.user)
        chef = get_object_or_404(Chef, user=request.user)
        profile_form = UserProfileForm(instance=profile)
        chef_form = ChefForm(instance=chef)

        context = {
            "profile_form": profile_form,
            "chef_form": chef_form,
            "profile": profile,
            "chef": chef,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        profile = get_object_or_404(UserProfile, user=request.user)
        chef = get_object_or_404(Chef, user=request.user)

        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        chef_form = ChefForm(request.POST, request.FILES, instance=chef)

        if profile_form.is_valid() and chef_form.is_valid():
            profile_form.save()
            chef_form.save()
            messages.success(request, "Settings updated.")
            return redirect("vprofile")
        else:
            print(profile_form.errors)
            print(chef_form.errors)

        context = {
            "profile_form": profile_form,
            "chef_form": chef_form,
            "profile": profile,
            "chef": chef,
        }
        return render(request, self.template_name, context)
