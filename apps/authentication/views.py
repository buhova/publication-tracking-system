# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from .forms import UserUpdateForm

from .forms import LoginForm, SignUpForm


def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = "Invalid credentials"
        else:
            msg = "Error validating the form"

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg = "Account created successfully."
            success = True

            # return redirect("/login/")

        else:
            msg = "Form is not valid"
    else:
        form = SignUpForm()

    return render(
        request,
        "accounts/register.html",
        {"form": form, "msg": msg, "success": success},
    )


@login_required
def update_user_view(request):
    user = request.user
    form = UserUpdateForm(request.POST or None, instance=user)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy("home:redactor-detail", kwargs={"pk": user.pk}))
        # Якщо форма неправильна — лишаємось на сторінці з помилками

    return render(request, "accounts/update_profile.html", {"form": form})

@login_required
def delete_user_view(request):
    user = request.user

    if request.method == "POST":
        try:
            with transaction.atomic():
                logout(request)
                user.delete()
            messages.success(request, "Your account has been successfully deleted.")
            return redirect("home:index")
        except Exception as e:
            messages.error(request, f"An error occurred while deleting your account: {e}")
            return redirect("home:index")

    return render(request, "home/redactor_confirm_delete.html", {"user": user})
