from itertools import chain
from django.contrib.auth.decorators import login_required
from django.db.models import Q


from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404

from . import forms
from review.models import UserFollows, Ticket, Review


@login_required
def follow_users(request):
    print(f'follow_users:request={request}')
    # form = forms.FollowUsersForm(instance=request.user)
    form = forms.FollowUsersForm()

    # following_list1 = UserFollows.objects.filter(user=request.user).order_by('-user')
    # print(f'following_list1={following_list1}')
    # following_list2 = UserFollows.objects.filter(user=request.user).order_by('user')
    # print(f'following_list2={following_list2}')
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
    # return render(request, 'review/stream.html')

    # reviews = Review.objects.select_related("ticket").filter(
    #     Q(user__in=UserFollows.objects.filter(user=request.user).values("followed_user")) | Q(user=request.user)
    # )
    reviews = Review.objects.filter(Q(user__in=UserFollows.objects.filter(user=request.user).values("followed_user")) | Q(user=request.user))

    # ticket w/o reviews
    tickets = Ticket.objects.filter(
        Q(user__in=UserFollows.objects.filter(user=request.user).values("followed_user")) | Q(user=request.user)
    ).exclude(id__in=reviews.values("ticket_id"))

    # prepare the mixed posts
    posts = sorted(chain(reviews, tickets), key=lambda post: post.time_created, reverse=True)
    stars = [0, 1, 2, 3, 4, 5]
    context = {"posts": posts, "stars": stars}

    # print(f'context={context}')

    return render(request, "review/stream.html", context=context)


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
def create_ticket_review(request):
    print(f'create_ticket_review:request={request}')

    if request.method == 'POST':

        form_ticket = forms.TicketForm(request.POST, request.FILES)
        form_review = forms.ReviewForm(request.POST)
        print(f'create_ticket_review:form_ticket.is_valid()={form_ticket.is_valid()}')
        print(f'create_ticket_review:form_review.is_valid()={form_review.is_valid()}')

        if all([form_ticket.is_valid(), form_review.is_valid()]):
            title = form_ticket.cleaned_data.get("title")
            description = form_ticket.cleaned_data.get("description")
            user = request.user
            image = form_ticket.cleaned_data.get("image")
            ticket_to_review = Ticket.objects.create(title=title, description=description, user=user, image=image)

            rating = form_review.cleaned_data.get("rating")
            headline = form_review.cleaned_data.get("headline")
            body = form_review.cleaned_data.get("body")
            Review.objects.create(
                ticket=ticket_to_review, rating=rating, user=request.user, headline=headline, body=body
            )
            return redirect("stream")

        context = {
            "form_ticket": form_ticket,
            "form_review": form_review,
        }
        return render(request, "review/create_ticket_review.html", context=context)

    if request.method == 'GET':

        form_ticket = forms.TicketForm()
        form_review = forms.ReviewForm()

        context = {
            "form_ticket": form_ticket,
            "form_review": form_review,
        }
        return render(request, "review/create_ticket_review.html", context=context)


@login_required()
def my_posts(request):
    print(f'posts:request={request}')

    if request.method == 'GET':
        # reviews = Review.objects.select_related("ticket").filter(Q(user=request.user))
        reviews = Review.objects.filter(Q(user=request.user))
        # reviews = reviews.annotate(content_type=Value("REVIEW", CharField()))

        tickets = Ticket.objects.filter(Q(user=request.user)).exclude(id__in=reviews.values("ticket_id"))
        # tickets = tickets.annotate(content_type=Value("TICKET", CharField()))

        my_posts = sorted(chain(reviews, tickets), key=lambda post: post.time_created, reverse=True)
        stars = [0, 1, 2, 3, 4, 5]
        context = {"my_posts": my_posts, "stars": stars}
        print(f'posts:context={context}')

        return render(request, "review/my_posts.html", context=context)


@login_required
def update_ticket(request, ticket_id):
    print(f'update_ticket:request={request}')
    context = {"ticket_id": ticket_id}
    return render(request, "review/update_ticket.html", context=context)


@login_required
def delete_ticket(request, ticket_id):
    print(f'delete_ticket:request={request}')
    print(f'ticket_id={ticket_id}')

    ticket = Ticket.objects.filter(id=ticket_id)

    print(f'ticket={ticket}')
    # ticket.delete()

    # if request.method == 'POST':
    #     form = forms.FollowUsersForm(request.POST)
    #     if form.is_valid():
    #         print("redirect('my_posts')")
    #         return redirect('my_posts')

    return redirect('my_posts')
    # context = {"ticket_id": ticket_id}
    # return render(request, "review/delete_ticket.html", context=context)


@login_required
def create_review(request, ticket_id):
    print(f'create_review:request={request}')
    print(f'ticket_id={ticket_id}')
    # ticket_to_review = Ticket.objects.filter(id=ticket_id)
    ticket_to_review = get_object_or_404(Ticket, id=ticket_id)
    print(f'ticket_to_review={ticket_to_review}')
    # if request.method == 'POST':
    #     form_review = forms.ReviewForm(request.POST)
    #
    #     print(f'create_review:form_review.is_valid()={form_review.is_valid()}')
    #     if form_review.is_valid():
    #         rating = form_review.cleaned_data.get("rating")
    #         headline = form_review.cleaned_data.get("headline")
    #         body = form_review.cleaned_data.get("body")
    #         Review.objects.create(ticket=ticket_to_review, rating=rating, user=request.user, headline=headline, body=body)
    #         return redirect("stream")
    if request.method == 'POST':

        form_review = forms.ReviewForm(request.POST)

        print(f'create_ticket_review:form_review.is_valid()={form_review.is_valid()}')

        if form_review.is_valid():
            rating = form_review.cleaned_data.get("rating")
            headline = form_review.cleaned_data.get("headline")
            body = form_review.cleaned_data.get("body")
            Review.objects.create(
                ticket=ticket_to_review, rating=rating, user=request.user, headline=headline, body=body
            )

            return redirect('stream')

    if request.method == 'GET':
        form_review = forms.ReviewForm()

        context = {
            "ticket_to_review": ticket_to_review,
            "form_review": form_review,
        }
        return render(request, "review/create_review.html", context=context)


@login_required
def update_review(request, ticket_id, review_id):
    print(f'update_review:request={request}')
    context = {"review_id": review_id}
    form_review = forms.ReviewForm(request.POST)
    print(f'create_ticket_review:form_review.is_valid()={form_review.is_valid()}')

    ticket_to_review = Ticket.objects.filter(id=ticket_id)
    if form_review.is_valid():

        rating = form_review.cleaned_data.get("rating")
        headline = form_review.cleaned_data.get("headline")
        body = form_review.cleaned_data.get("body")
        Review.objects.update(ticket=ticket_to_review, rating=rating, user=request.user, headline=headline, body=body)
        return redirect("posts")

        context = {
            "form_ticket": form_ticket,
            "form_review": form_review,
        }
    return render(request, "review/update_review.html", context=context)


@login_required
def delete_review(request, ticket_id, review_id):
    print(f'delete_review:request={request}')
    context = {"review_id": review_id}
    return redirect('my_posts')
    # return render(request, "review/update_ticket.html", context=context)
