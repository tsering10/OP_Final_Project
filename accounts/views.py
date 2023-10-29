from django.shortcuts import render,redirect
from django.views.generic import CreateView
from .forms import UserForm
from .models import User
from django.contrib import messages

# Create your views here.
class RegisterUserView(CreateView):
    form_class = UserForm
    template_name = "accounts/registerUser.html"
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            # Create the user using the form
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.role = User.CUSTOMER
            user.save()
            messages.success(request, 'Your account has been registered sucessfully!')
            return redirect('registerUser')
        else:
            print("invalide form")
            print(form.errors)
        return render(request, self.template_name, context={'form': form})

