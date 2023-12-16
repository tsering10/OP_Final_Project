from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from .forms import ChefForm
from efood_main.apps.accounts.forms import UserProfileForm
from .models import Chef
from efood_main.apps.accounts.models import UserProfile

# Create your views here.


class ChefProfileView(TemplateView):
    template_name = "chef/chef_profile.html"

    def get(self, request):
        chef_form = ChefForm()
        profile_form = UserProfileForm()
        chef = get_object_or_404(Chef, user=request.user)
        profile = get_object_or_404(UserProfile, user=request.user)
        context = {
            "chef_form": chef_form,
            "profile_form": profile_form,
            "chef": chef,
            "profile": profile,
        }
        return render(request, self.template_name, context)
