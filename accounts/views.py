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
            # Create the user using create_user method
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, 
                                               username=username, email=email, 
                                               password=password)
            user.role = User.CUSTOMER
            user.save()
            messages.success(request, 'Your account has been registered sucessfully!')
            return redirect('registerUser')
        else:
            print("invalide form")
            print(form.errors)
        return render(request, self.template_name, context={'form': form})

# def registerUser(request):
#     return  HttpResponse("This is a user registeration form")