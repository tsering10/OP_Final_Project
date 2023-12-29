from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView
from .forms import ChefForm
from efood_main.apps.accounts.forms import UserProfileForm
from .models import Chef
from efood_main.apps.accounts.models import UserProfile
from efood_main.apps.recipe.models import Category, RecipeItem
from efood_main.apps.recipe.forms import CategoryForm

from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.text import slugify

from django.contrib.auth.mixins import LoginRequiredMixin


class ChefProfileView(LoginRequiredMixin, TemplateView):
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
            return redirect("chef_profile")
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


class ChefRecipeBuilder(LoginRequiredMixin, TemplateView):
    model = Category
    template_name = "chef/recipe_builder.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chef = Chef.objects.get(user=self.request.user)
        context["categories"] = Category.objects.filter(chef=chef)
        return context


class RecipeItemsByCategoryView(LoginRequiredMixin, ListView):
    template_name = "chef/recipe_items_by_category.html"
    context_object_name = "recipeitems"

    def get_queryset(self):
        chef = Chef.objects.get(user=self.request.user)
        category = get_object_or_404(Category, pk=self.kwargs["pk"])
        return RecipeItem.objects.filter(chef=chef, category=category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(Category, pk=self.kwargs["pk"])
        context["category"] = category
        return context


class AddCategoryView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = "chef/add_category.html"
    model = Category
    form_class = CategoryForm
    template_name = "chef/add_category.html"
    success_url = reverse_lazy("recipe_builder")
    success_message = "Category added successfully!"

    def form_valid(self, form):
        category = form.save(commit=False)
        category.chef = self.request.user.chef
        category.slug = slugify(category.category_name) + "-" + str(category.id)
        return super().form_valid(form)
