from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.views.generic import ListView, TemplateView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from efood_main.apps.accounts.forms import UserProfileForm
from efood_main.apps.accounts.models import UserProfile
from efood_main.apps.recipe.forms import CategoryForm, RecipeItemForm
from efood_main.apps.recipe.models import Category, RecipeItem
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import ObjectDoesNotExist
from .forms import ChefForm
from .models import Chef


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


class ChefViewMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        try:
            self.chef = self.request.user.chef
            return self.chef
        except ObjectDoesNotExist:
            return False


class ChefRecipeBuilder(ChefViewMixin, TemplateView):
    model = Category
    template_name = "chef/recipe_builder.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.filter(chef=self.chef)
        return context


class RecipeItemsByCategoryView(ChefViewMixin, ListView):
    template_name = "chef/recipe_items_by_category.html"
    context_object_name = "recipeitems"

    def get_queryset(self):
        category = get_object_or_404(Category, pk=self.kwargs["pk"])
        return RecipeItem.objects.filter(chef=self.chef, category=category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(Category, pk=self.kwargs["pk"], chef=self.chef)
        context["category"] = category
        return context


class AddCategoryView(ChefViewMixin, SuccessMessageMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "chef/add_category.html"
    success_url = reverse_lazy("recipe_builder")
    success_message = "Category added successfully!"

    def form_valid(self, form):
        category = form.save(commit=False)
        category.chef = self.chef
        category.slug = slugify(category.category_name)
        return super().form_valid(form)

    def get_object(self, queryset=None):
        return get_object_or_404(Category, pk=self.kwargs["pk"], chef=self.chef)


class EditCategoryView(ChefViewMixin, SuccessMessageMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "chef/edit_category.html"
    success_url = reverse_lazy("recipe_builder")
    success_message = "Category updated successfully!"

    def get_object(self, queryset=None):
        return get_object_or_404(Category, pk=self.kwargs["pk"], chef=self.chef)

    def form_valid(self, form):
        category = form.save(commit=False)
        category.slug = slugify(category.category_name)
        category.chef = self.chef
        return super().form_valid(form)


class CategoryDeleteView(ChefViewMixin, DeleteView):
    model = Category
    template_name = "chef/category_confirm_delete.html"
    success_url = reverse_lazy("recipe_builder")

    def get_object(self, queryset=None):
        return get_object_or_404(Category, pk=self.kwargs["pk"], chef=self.chef)


class AddRecipeView(ChefViewMixin, SuccessMessageMixin, CreateView):
    model = RecipeItem
    form_class = RecipeItemForm
    template_name = "chef/add_recipe.html"
    success_message = "Recipe Item added successfully!"

    def form_valid(self, form):
        form.instance.chef = self.chef
        form.instance.slug = slugify(form.cleaned_data["recipe_title"])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("recipeitems_by_category", args=(self.object.category.id,))

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["chef"] = self.chef
        return kwargs


class EditRecipeView(ChefViewMixin, SuccessMessageMixin, UpdateView):
    model = RecipeItem
    form_class = RecipeItemForm
    template_name = "chef/edit_recipe.html"
    context_object_name = "recipe"
    success_message = "Recipe Item updated successfully!"

    def get_queryset(self):
        return RecipeItem.objects.filter(chef=self.chef)

    def get_success_url(self):
        return reverse_lazy("recipeitems_by_category", args=[self.object.category.id])

    def form_valid(self, form):
        recipe_title = form.cleaned_data["recipe_title"]
        form.instance.chef = self.chef
        form.instance.slug = slugify(recipe_title)
        return super().form_valid(form)


class RecipeDeleteView(ChefViewMixin, DeleteView):
    model = RecipeItem
    template_name = "chef/recipe_confirm_delete.html"

    def get_object(self, queryset=None):
        return get_object_or_404(RecipeItem, pk=self.kwargs["pk"], chef=self.chef)

    def get_success_url(self):
        return reverse_lazy("recipeitems_by_category", args=[self.object.category.id])


class RecipeDetailView(ChefViewMixin, DetailView):
    model = RecipeItem
    template_name = "chef/recipe_detail.html"
    context_object_name = "recipe"

    def get_queryset(self):
        slug = self.kwargs["slug"]
        recipe_id = self.kwargs["id"]
        return RecipeItem.objects.filter(slug=slug, id=recipe_id)

    def get_object(self, queryset=None):
        slug = self.kwargs["slug"]
        chef = self.chef
        recipe_id = self.kwargs["id"]
        return get_object_or_404(RecipeItem, slug=slug, id=recipe_id, chef=chef)
