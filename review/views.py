from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, reverse
from django.views.generic import View
from django.conf import settings

from . import forms
from review.models import UserFollows


@login_required
def follow_users(request):
    print(f'follow_users:request={request}')
    # form = forms.FollowUsersForm(instance=request.user)
    form = forms.FollowUsersForm()

    following_list1 = UserFollows.objects.filter(user=request.user).order_by('-user')
    print(f'following_list1={following_list1}')
    following_list2 = UserFollows.objects.filter(user=request.user).order_by('user')
    print(f'following_list2={following_list2}')
    following_list = UserFollows.objects.filter(user=request.user).order_by('-id')
    follower_list = UserFollows.objects.filter(followed_user=request.user).order_by('-id')

    print(f'following_list={following_list}')
    print(f'follower_list={follower_list}')
    # form = self.form_class(request_user=self.request.user, former_followed_user=subscription_list)

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

            return redirect('follow_users')

        return render(request, 'review/follow_users.html', context={'form': form})

    if request.method == 'GET':
        print("form is GET")

        context = {
            "form": form,
            "form_follower": follower_list,
            "form_following": following_list,
        }

        print(f'context={context}')
        return render(request, 'review/follow_users.html', context=context)


@login_required
def unfollow_user(request, user_follows_id):
    print(f'unfollow_user:request={request}')
    print(f'user_follows_id={user_follows_id}')
    xid = user_follows_id
    print(f'id={xid} {type(xid)}')

    user_follows = UserFollows.objects.filter(id=xid)
    print(f'id={user_follows} {type(user_follows)}')
    user_follows.delete()

    if request.method == 'POST':
        form = forms.FollowUsersForm(request.POST)
        if form.is_valid():
            print("redirect('follow_users')")
            return redirect('follow_users')

    form = forms.FollowUsersForm()
    following_list = UserFollows.objects.filter(user=request.user)
    follower_list = UserFollows.objects.filter(followed_user=request.user)

    context = {
        "form": form,
        "form_follower": follower_list,
        "form_following": following_list,
    }

    return render(request, 'review/follow_users.html', context=context)


@login_required
def home(request):
    # logout(request)
    # return redirect('login')
    return render(request, 'review/home.html')


@login_required
def stream(request):
    # logout(request)
    # return redirect('login')
    return render(request, 'review/stream.html')


@login_required
def create_ticket(request):
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
            return redirect('stream')
    return render(request, 'review/create_ticket.html', context={'form': form})


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
            return redirect('streams')
    return render(request, 'review/create_ticket.html', context={'form': form})


@login_required
def create_ticket_review(request):
    print(f'open_ticket:request={request}')
