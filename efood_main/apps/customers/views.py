from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, ListView, TemplateView

from efood_main.apps.accounts.forms import UserInfoForm, UserProfileForm
from efood_main.apps.accounts.models import UserProfile
from efood_main.apps.workshop.models import Workshop, WorkshopRegistration


class CustomerViewMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        try:
            self.customer = self.request.user.is_customer
            return self.customer
        except ObjectDoesNotExist:
            return False


class CustomerProfileView(CustomerViewMixin, TemplateView):
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


class CustomerWorkshopDetail(CustomerViewMixin, DetailView):
    model = Workshop
    template_name = "customers/customer_workshop_detail.html"

    def get_object(self, queryset=None):
        return get_object_or_404(Workshop, id=self.kwargs["id"])


class WorkshopBookConfirmation(CustomerViewMixin, TemplateView):
    template_name = "customers/booking-confirmation.html"


class CustomerWorkshopBook(CustomerViewMixin, TemplateView):
    def post(self, request, *args, **kwargs):
        workshop_id = self.kwargs.get("workshop_id")
        workshop = get_object_or_404(Workshop, id=workshop_id)

        if WorkshopRegistration.objects.filter(
            customer=request.user, workshop=workshop
        ).exists():
            # Optionally, add a message to be displayed to the user
            messages.add_message(
                request, messages.INFO, "You have already booked a workshop."
            )
            return redirect("customer_workshop")  # Redirect to a suitable page

        if workshop.capacity > 0:
            # Decrease the capacity
            workshop.capacity -= 1
            workshop.save()

            # Register the user for the workshop
            WorkshopRegistration.objects.create(
                customer=request.user, workshop=workshop
            )
            # Send confirmation emails
            send_mail(
                "Workshop Booking Confirmation",
                f"You have successfully booked {workshop.title} \
                    . On {workshop.date}{workshop.time}",
                settings.EMAIL_HOST_USER,
                [
                    request.user.email,
                    workshop.chef.user.email,
                ],
                fail_silently=False,
            )
            return redirect("workshop-confirmation")
        else:
            return redirect("customer_workshop")


class CustomerWorkshopCancel(CustomerViewMixin, TemplateView):
    def post(self, request, *args, **kwargs):
        workshop_id = self.kwargs.get("workshop_id")
        workshop = get_object_or_404(Workshop, id=workshop_id)

        # Check if the user has a registration for this specific workshop
        registration = WorkshopRegistration.objects.filter(
            customer=request.user, workshop=workshop
        ).first()
        if registration:
            # Delete the registration
            registration.delete()

            # Increase the workshop capacity
            workshop.capacity += 1
            workshop.save()

            # Optionally, add a message to be displayed to the user
            messages.add_message(
                request,
                messages.INFO,
                "Your registration has been cancelled successfully.",
            )
        else:
            # If no registration is found, inform the user
            messages.add_message(
                request,
                messages.WARNING,
                "You do not have a registration for this workshop to cancel.",
            )

        return redirect("customer_workshop")


class CustomerBookedWorkshopsView(CustomerViewMixin, ListView):
    model = WorkshopRegistration
    template_name = "customers/customer_workshop.html"
    context_object_name = "booked_workshops"

    def get_queryset(self):
        # Get unique workshop IDs for the current user's non-canceled workshop
        workshop_ids = (
            WorkshopRegistration.objects.filter(
                customer=self.request.user, is_canceled=False
            )
            .values_list("workshop_id", flat=True)
            .distinct()
        )

        # Query Workshop model for those unique IDs
        return Workshop.objects.filter(id__in=workshop_ids).distinct()
