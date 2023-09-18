import json

from django.shortcuts import render, redirect
from admin_volt.forms import RegistrationForm, LoginForm, UserPasswordResetForm, UserPasswordChangeForm, \
    UserSetPasswordForm
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView, PasswordResetConfirmView
from django.contrib.auth import logout

from django.contrib.auth.decorators import login_required


# Index
def index(request):
    return render(request, 'pages/index.html')


# Dashboard
def dashboard(request):
    with open("data/40_man_roster.json", "r") as file:
        roster_text = ''.join(file.readlines())

    roster_json = json.loads(roster_text)

    context = {
        'segment': 'dashboard',
        'players': roster_json
    }

    return render(request, 'pages/dashboard/dashboard.html', context)


# Top Recruits
def recruits(request):
    with open("data/prospects.json", "r") as file:
        roster_text = ''.join(file.readlines())

    roster_json = json.loads(roster_text)

    context = {
        'segment': 'recruits',
        'players': roster_json
    }

    return render(request, 'pages/recruits/recruits.html', context)


# Roster Updates
def roster_updates(request):
    with open("data/roster_updates.json", "r") as file:
        updates_text = ''.join(file.readlines())

    updates_json = json.loads(updates_text)

    context = {
        'segment': 'roster_updates',
        'updates': updates_json
    }

    return render(request, 'pages/roster_updates/roster_updates.html', context)


# Pages
@login_required(login_url="/accounts/login/")
def transaction(request):
    context = {
        'segment': 'transactions'
    }
    return render(request, 'pages/transactions.html', context)


@login_required(login_url="/accounts/login/")
def settings(request):
    context = {
        'segment': 'settings'
    }
    return render(request, 'pages/settings.html', context)


# Tables
@login_required(login_url="/accounts/login/")
def bs_tables(request):
    context = {
        'parent': 'tables',
        'segment': 'bs_tables',
    }
    return render(request, 'pages/tables/bootstrap-tables.html', context)


# Components
@login_required(login_url="/accounts/login/")
def buttons(request):
    context = {
        'parent': 'components',
        'segment': 'buttons',
    }
    return render(request, 'pages/components/buttons.html', context)


@login_required(login_url="/accounts/login/")
def notifications(request):
    context = {
        'parent': 'components',
        'segment': 'notifications',
    }
    return render(request, 'pages/components/notifications.html', context)


@login_required(login_url="/accounts/login/")
def forms(request):
    context = {
        'parent': 'components',
        'segment': 'forms',
    }
    return render(request, 'pages/components/forms.html', context)


@login_required(login_url="/accounts/login/")
def modals(request):
    context = {
        'parent': 'components',
        'segment': 'modals',
    }
    return render(request, 'pages/components/modals.html', context)


@login_required(login_url="/accounts/login/")
def typography(request):
    context = {
        'parent': 'components',
        'segment': 'typography',
    }
    return render(request, 'pages/components/typography.html', context)


# Authentication
def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            print("Account created successfully!")
            form.save()
            return redirect('/accounts/login/')
        else:
            print("Registration failed!")
    else:
        form = RegistrationForm()

    context = {'form': form}
    return render(request, 'accounts/sign-up.html', context)


class UserLoginView(LoginView):
    form_class = LoginForm
    template_name = 'accounts/sign-in.html'


class UserPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/password-change.html'
    form_class = UserPasswordChangeForm


class UserPasswordResetView(PasswordResetView):
    template_name = 'accounts/forgot-password.html'
    form_class = UserPasswordResetForm


class UserPasswrodResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/reset-password.html'
    form_class = UserSetPasswordForm


def logout_view(request):
    logout(request)
    return redirect('/accounts/login/')


def lock(request):
    return render(request, 'accounts/lock.html')


# Errors
def error_404(request):
    return render(request, 'pages/examples/404.html')


def error_500(request):
    return render(request, 'pages/examples/500.html')


# Extra
def upgrade_to_pro(request):
    return render(request, 'pages/upgrade-to-pro.html')