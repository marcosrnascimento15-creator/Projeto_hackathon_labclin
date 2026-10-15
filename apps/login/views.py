from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render


def login(request):
    """Autentica o usuário."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect(request.GET.get('next') or 'home')

        return render(request, 'login.html', {
            'error': 'Nome de usuário ou senha inválidos.',
        })

    return render(request, 'login.html')


def cadastrar(request):
    """Cadastra um novo usuário do sistema."""
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        dados = {'username': username, 'email': email}

        if password != confirm_password:
            return render(request, 'cadastrar.html', {
                'error': 'As senhas não coincidem.', **dados})

        if User.objects.filter(username=username).exists():
            return render(request, 'cadastrar.html', {
                'error': 'Este nome de usuário já está cadastrado.', **dados})

        try:
            validate_password(password)
        except ValidationError as e:
            return render(request, 'cadastrar.html', {
                'error': ' '.join(e.messages), **dados})

        User.objects.create_user(username=username, email=email, password=password)
        return redirect('login')

    return render(request, 'cadastrar.html')


def logout(request):
    """Encerra a sessão do usuário."""
    auth_logout(request)
    return redirect('login')
