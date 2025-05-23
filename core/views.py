from django.shortcuts import render, redirect
from .models import WordPair
from .forms import WordPairForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

@login_required
def add_word(request):
    if request.method == 'POST':
        form = WordPairForm(request.POST)
        if form.is_valid():
            word = form.save(commit=False)
            word.user = request.user
            word.save()
            return redirect('home')
    else:
        form = WordPairForm()
    return render(request, 'core/add_word.html', {'form': form})

@login_required
def home(request):
    response = None
    if request.method == 'POST':
        query = request.POST.get('query')
        try:
            word = WordPair.objects.get(user=request.user, input_text=query)
            response = word.output_text
        except WordPair.DoesNotExist:
            response = "Topilmadi!"
    return render(request, 'core/home.html', {'response': response})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'core/signup.html', {'form': form})
from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return redirect('home')
