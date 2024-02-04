from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import UpdateView

from efood_main.apps.accounts.forms import UserInfoForm, UserProfileForm
from efood_main.apps.accounts.models import UserProfile


class ChefViewMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        try:
            self.customer = self.request.user.is_customer
            return self.customer
        except ObjectDoesNotExist:
            return False


class CustomerProfileView(ChefViewMixin, TemplateView):
    template_name = "customers/customer_profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Fetch UserProfile and Chef objects or return a 404 response
        profile = get_object_or_404(UserProfile, user=self.request.user)

        # Create a combined form with both UserProfileForm and ChefForm
        combined_form = self.get_combined_form(profile)

        context["combined_form"] = combined_form
        context["profile"] = profile
        return context

    def get_combined_form(self, profile):
        profile_form = UserProfileForm(instance=profile)
        user_form = UserInfoForm(instance=self.request.user)

        # Combine both forms into a single form
        combined_form = {
            "profile_form": profile_form,
            "user_form": user_form,
        }
        return combined_form

    def form_valid(self, form):
        form["profile_form"].save()
        form["user_form"].save()
        messages.success(self.request, "Profile updated.")
        return redirect("customer")

    def post(self, request, *args, **kwargs):
        profile = get_object_or_404(UserProfile, user=request.user)

        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        user_form = UserInfoForm(
            request.POST, request.FILES, instance=self.request.user
        )

        combined_form = {
            "profile_form": profile_form,
            "user_form": user_form,
        }

        if profile_form.is_valid():
            return self.form_valid(combined_form)


class CustomerWorkshopsView(ChefViewMixin, TemplateView):
    template_name = "customers/customer_workshop.html"
