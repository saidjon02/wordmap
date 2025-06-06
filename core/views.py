# core/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import WordPair
from .forms import WordPairForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth import views as auth_views
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.db.models import Q

# ============================
# So‘z qo‘shish (login talab qilinadi)
# ============================
@login_required
def add_word(request):
    error_message = None
    if request.method == 'POST':
        form = WordPairForm(request.POST)
        if form.is_valid():
            input_text = form.cleaned_data['input_text']
            # Duplicate tekshirish (case-insensitive)
            exists = WordPair.objects.filter(
                user=request.user,
                input_text__iexact=input_text
            ).exists()
            if exists:
                error_message = "You already have this word in your list."
            else:
                word = form.save(commit=False)
                word.user = request.user
                word.save()
                return redirect('home')
    else:
        form = WordPairForm()

    return render(
        request, 
        'core/add_word.html', 
        {'form': form, 'error_message': error_message}
    )

# ============================
# Asosiy sahifa (POST → qidiruv, GET → natija)
# ============================
@login_required
def home(request):
    # 1) Sessiyadan welcome_username’ni olish (bir martalik)
    welcome = request.session.pop('welcome_username', None)

    response = None
    query = ''

    if request.method == 'POST':
        # POST so‘rov: form’dan kelgan inputni qidirib, javobni sessiyaga yozish
        query = request.POST.get('query', '')
        try:
            word = WordPair.objects.get(user=request.user, input_text=query)
            response = word.output_text
        except WordPair.DoesNotExist:
            response = "Not Found!"
        # sessiyaga saqlash, keyin redirect
        request.session['response'] = response
        request.session['query'] = query
        return redirect('home')

    else:
        # GET so‘rov: sessiyanidagi response va query’ni olish
        response = request.session.pop('response', None)
        query = request.session.pop('query', '')

    # Template’ga yuboriladigan kontekst
    context = {
        'response': response,
        'query': query,
        'welcome_username': welcome,
    }
    return render(request, 'core/home.html', context)

# ============================
# Signup (ro‘yxatdan o‘tish)
# ============================
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

# ============================
# Logout (agar custom logout_view kerak bo‘lsa)
# ============================
def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return redirect('login')  # logout bo‘lgach login sahifasiga yuboradi

# ============================
# Qidiruv takliflari (AJAX)
# ============================
@login_required
def search_suggestions(request):
    query = request.GET.get('term', '')
    suggestions = []
    if query:
        words = WordPair.objects.filter(
            Q(input_text__icontains=query),
            user=request.user
        )[:10]
        suggestions = [w.input_text for w in words]
    return JsonResponse(suggestions, safe=False)

# ============================
# So‘z natijasini olish (AJAX POST)
# ============================
@login_required
def get_word_output(request):
    if request.method == 'POST':
        query = request.POST.get('query')
        try:
            word = WordPair.objects.get(user=request.user, input_text=query)
            return JsonResponse({'result': word.output_text})
        except WordPair.DoesNotExist:
            return JsonResponse({'result': "Not Found!"})
    return JsonResponse({'result': ''})

# ============================
# So‘z o‘chirish
# ============================
@login_required
def delete_word(request, word_id):
    try:
        word = WordPair.objects.get(id=word_id, user=request.user)
        if request.method == 'POST':
            word.delete()
            messages.success(request, 'So‘z muvaffaqiyatli o‘chirildi.')
            return redirect('home')
    except WordPair.DoesNotExist:
        messages.error(request, 'So‘z topilmadi.')
    return redirect('home')

# ============================
# So‘z tahrirlash
# ============================
@login_required
def edit_word(request, word_id):
    word = get_object_or_404(WordPair, id=word_id, user=request.user)

    if request.method == "POST":
        form = WordPairForm(request.POST, instance=word)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = WordPairForm(instance=word)

    return render(request, 'core/edit_word.html', {'form': form, 'word': word})

# ============================
# Parol o‘zgartirish (username & password)
# ============================
@login_required
def change_password_view(request):
    user = request.user
    words = WordPair.objects.filter(user=user)

    if request.method == 'POST':
        # Username o‘zgartirish
        new_username = request.POST.get('username')
        if new_username and new_username != user.username:
            user.username = new_username
            user.save()
            messages.success(request, 'Username o‘zgartirildi.')

        # Password o‘zgartirish
        password_form = PasswordChangeForm(user, request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  # logout qilmaslik uchun
            messages.success(request, 'Parol muvaffaqiyatli o‘zgartirildi.')
        else:
            # xatoliklarni message’ga chiqarish
            for err in password_form.errors.values():
                messages.error(request, err)

        return redirect('home')
    else:
        password_form = PasswordChangeForm(user)

    context = {
        'words': words,
        'password_form': password_form,
    }
    return render(request, 'core/change_password.html', context)

# ============================
# Products (o‘xshash change_password_view, lekin boshqa template)
# ============================
@login_required
def change_products_view(request):
    user = request.user
    words = WordPair.objects.filter(user=user)

    if request.method == 'POST':
        # Username o‘zgartirish
        new_username = request.POST.get('username')
        if new_username and new_username != user.username:
            user.username = new_username
            user.save()
            messages.success(request, 'Username o‘zgartirildi.')

        # Password o‘zgartirish
        password_form = PasswordChangeForm(user, request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Parol muvaffaqiyatli o‘zgartirildi.')
        else:
            for err in password_form.errors.values():
                messages.error(request, err)

        return redirect('home')
    else:
        password_form = PasswordChangeForm(user)

    context = {
        'words': words,
        'password_form': password_form,
    }
    # Template nomini 'change_products.html' deb o‘zgartirdim (ilgari yozilgan 'change_product.html' xatolik beradi)
    return render(request, 'core/change_products.html', context)


# ============================
# DRF ViewSet (WordPairViewSet)
# ============================
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, permissions
from .serializers import PostSerializer

class WordPairViewSet(viewsets.ModelViewSet):
    queryset = WordPair.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            # Foydalanuvchiga tegishli yoki public bo‘lganlarni qaytarish
            return WordPair.objects.filter(
                Q(is_public=True) | Q(user=user)
            )
        return WordPair.objects.filter(is_public=True)

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        if user in post.likes.all():
            post.likes.remove(user)
        else:
            post.likes.add(user)
        return Response({'status': 'like toggled'})

    @action(detail=True, methods=['post'])
    def save(self, request, pk=None):
        post = self.get_object()
        user = request.user
        if user in post.saved_by.all():
            post.saved_by.remove(user)
        else:
            post.saved_by.add(user)
        return Response({'status': 'save toggled'})
