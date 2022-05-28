from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.generic import View
from django.conf import settings

from . import forms


@login_required
def home(request):
    # logout(request)
    # return redirect('login')
    return render(request, 'review/home.html')


@login_required
def open_ticket(request):
    print(f'open_ticket:request={request}')
    form = forms.TicketForm()
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            print("form is valid")
            ticket = form.save(commit=False)
            # set the uploader to the user before saving the model
            ticket.user = request.user
            print(ticket)
            # now we can save
            ticket.save()
            return redirect('home')
    return render(request, 'review/open_ticket.html', context={'form': form})


@login_required
def follow_users(request):
    print(f'follow_users:request={request}')
    # form = forms.FollowUsersForm(instance=request.user)
    form = forms.FollowUsersForm()
    if request.method == 'POST':
        # form = forms.FollowUsersForm(request.POST, instance=request.user)
        form = forms.FollowUsersForm(request.POST)
        if form.is_valid():
            print("form is valid")
            print(f'cleaned_data={form.cleaned_data}')
            # print(f"followed_user={form.cleaned_data['followed_user']}")
            followed_users = form.save(commit=False)
            followed_users.user = request.user
            followed_users.followed_user = form.cleaned_data['followed_user']
            print(followed_users)
            followed_users.save()

            return redirect('home')
    return render(request, 'review/follow_users.html', context={'form': form})
