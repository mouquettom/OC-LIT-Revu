from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from accounts.forms import SignupForm, LoginForm


User = get_user_model()


def signup_page(request):
    """Page d'inscription"""
    form = SignupForm()

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('feed', username=user.username)

    return render(request, 'accounts/signup.html', {'form': form})


def login_page(request):
    """Page de connexion"""
    if request.user.is_authenticated:
        return redirect('feed', username=request.user.username)

    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('feed', username=user.username)

            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")

    return render(request, 'accounts/login.html', {'form': form})


def logout_user(request):
    """Déconnexion"""
    logout(request)
    return redirect('index')


@login_required
def people(request):
    """
    Page de gestion des abonnements :
    - champ texte pour suivre quelqu'un par son username
    - liste des utilisateurs suivis
    - liste des autres utilisateurs
    """
    if request.method == 'POST':
        username_to_follow = request.POST.get('username', '').strip()

        if not username_to_follow:
            messages.error(request, "Veuillez saisir un nom d'utilisateur.")
            return redirect('people')

        try:
            other = User.objects.get(username=username_to_follow)
        except User.DoesNotExist:
            messages.error(request, "Cet utilisateur n'existe pas.")
            return redirect('people')

        if other == request.user:
            messages.error(request, "On ne peut pas se suivre soi-même.")
            return redirect('people')

        request.user.follow(other)
        messages.success(request, f"Tu suis maintenant @{other.username}.")
        return redirect('people')

    followed_users = request.user.followings.all().order_by('username')
    other_users = User.objects.exclude(
        pk__in=followed_users.values_list('pk', flat=True)
    ).exclude(pk=request.user.pk).order_by('username')

    context = {
        'followed_users': followed_users,
        'other_users': other_users,
    }
    return render(request, 'accounts/people.html', context)


@login_required
def follow_user(request, username):
    """Abonnement"""
    other = get_object_or_404(User, username=username)

    if other == request.user:
        messages.error(request, "On ne peut pas se suivre soi-même.")
        return redirect('feed', username=request.user.username)

    request.user.follow(other)
    messages.success(request, f"Tu suis maintenant @{other.username}.")
    return redirect('feed', username=other.username)


@login_required
def unfollow_user(request, username):
    """Désabonnement"""
    other = get_object_or_404(User, username=username)

    if other == request.user:
        messages.error(request, "On ne peut pas se désabonner de soi-même.")
        return redirect('feed', username=request.user.username)

    request.user.unfollow(other)
    messages.success(request, f"Tu ne suis plus @{other.username}.")
    return redirect('feed', username=other.username)


@login_required
def search_users(request):
    query = request.GET.get('q', '').strip()

    results = []

    if query:
        users = User.objects.filter(
            username__istartswith=query
        ).exclude(
            pk=request.user.pk
        ).order_by('username')[:8]

        results = [
            {
                'username': user.username,
                'profile_url': reverse('feed', kwargs={'username': user.username}),
            }
            for user in users
        ]

    return JsonResponse({'results': results})