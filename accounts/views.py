from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomLoginForm

# Handles user registration
def register(request):
    if request.method == 'POST':
        # Bind submitted POST data to the registration form
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Save the new user to the database
            form.save()
            # Redirect to login page after successful registration
            return redirect('login')
    else:
        # If GET request, instantiate an empty registration form
        form = CustomUserCreationForm()
    
    # Render the registration page with the form
    return render(request, 'accounts/register.html', {'form': form})


# Handles user login
def login_view(request):
    # Redirect authenticated users directly to home
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        # Bind submitted POST data to the login form
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            # Extract email and password from form data
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Authenticate user using email as username
            user = authenticate(request, username=email, password=password)
            if user is not None:
                # Log in the user and redirect to home
                login(request, user)
                return redirect('home')
            else:
                # Show error message for invalid credentials
                messages.error(request, 'Invalid email or password')
    else:
        # If GET request, show an empty login form
        form = CustomLoginForm()
    
    # Render the login page with the form
    return render(request, 'accounts/login.html', {'form': form})


# Renders the home page (accessible after login)
def home_view(request):
    return render(request, 'accounts/home.html', {'user': request.user})
