from itertools import chain
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from . import forms
from review.models import UserFollows, Ticket, Review
from django.utils import timezone


@login_required
def follow_users(request):
    form = forms.FollowUsersForm()

    following_list = UserFollows.objects.filter(user=request.user).order_by('-id')
    follower_list = UserFollows.objects.filter(followed_user=request.user).order_by('-id')

    if request.method == 'POST':
        form = forms.FollowUsersForm(request.POST)
        if form.is_valid():
            followed_users = form.save(commit=False)
            followed_users.user = request.user
            followed_users.followed_user = form.cleaned_data['followed_user']
            followed_users.save()

            return redirect('follow_users')

        return render(request, 'review/follow_users.html', context={'form': form})

    if request.method == 'GET':

        context = {
            "form": form,
            "form_follower": follower_list,
            "form_following": following_list,
        }

        return render(request, 'review/follow_users.html', context=context)


@login_required
def unfollow_user(request, user_follows_id):
    xid = user_follows_id

    user_follows = UserFollows.objects.filter(id=xid)
    user_follows.delete()

    if request.method == 'POST':
        form = forms.FollowUsersForm(request.POST)
        if form.is_valid():
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
    return render(request, 'review/home.html')


@login_required
def stream(request):

    reviews = Review.objects.filter(Q(user__in=UserFollows.objects.filter(user=request.user).values("followed_user")))

    tickets = Ticket.objects.filter(
        Q(user__in=UserFollows.objects.filter(user=request.user).values("followed_user"))
    ).exclude(id__in=reviews.values("ticket_id"))

    # prepare the mixed posts
    posts = sorted(chain(reviews, tickets), key=lambda post: post.time_created, reverse=True)
    stars = [0, 1, 2, 3, 4, 5]
    context = {"posts": posts, "stars": stars}

    return render(request, "review/stream.html", context=context)


@login_required
def create_ticket(request):
    form = forms.TicketForm()
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('stream')
    return render(request, 'review/create_ticket.html', context={'form': form})


@login_required
def create_ticket_review(request):

    if request.method == 'POST':

        form_ticket = forms.TicketForm(request.POST, request.FILES)
        form_review = forms.ReviewForm(request.POST)

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

    if request.method == 'GET':
        reviews = Review.objects.filter(Q(user=request.user))
        # reviews = reviews.annotate(content_type=Value("REVIEW", CharField()))

        tickets = Ticket.objects.filter(Q(user=request.user)).exclude(id__in=reviews.values("ticket_id"))
        # tickets = tickets.annotate(content_type=Value("TICKET", CharField()))

        my_posts = sorted(chain(reviews, tickets), key=lambda post: post.time_created, reverse=True)
        stars = [0, 1, 2, 3, 4, 5]
        context = {"my_posts": my_posts, "stars": stars}

        return render(request, "review/my_posts.html", context=context)


@login_required
def update_ticket(request, ticket_id):
    ticket_to_review = get_object_or_404(Ticket, id=ticket_id)

    if request.method == 'POST':
        form_ticket = forms.TicketForm(request.POST, request.FILES)

        if form_ticket.is_valid():
            title = form_ticket.cleaned_data.get("title")
            description = form_ticket.cleaned_data.get("description")
            image = form_ticket.cleaned_data.get("image")

            Ticket.objects.filter(id=ticket_id).update(
                title=title, description=description, user=request.user, image=image,
                time_created=timezone.now()
            )
            return redirect("my_posts")

    if request.method == 'GET':
        form_ticket = forms.TicketForm()
        context = {
            "ticket_to_review": ticket_to_review,
            "form_ticket": form_ticket,
        }
    return render(request, "review/update_ticket.html", context=context)


@login_required
def delete_ticket(request, ticket_id):

    if request.method == 'POST':
        Ticket.objects.filter(id=ticket_id).delete()
        return redirect("my_posts")


@login_required
def create_review(request, ticket_id):
    ticket_to_review = get_object_or_404(Ticket, id=ticket_id)

    if request.method == 'POST':
        form_review = forms.ReviewForm(request.POST)

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
    context = {"review_id": review_id}

    ticket_of_review = get_object_or_404(Ticket, id=ticket_id)

    if request.method == 'POST':
        form_review = forms.ReviewForm(request.POST)
        if form_review.is_valid():
            rating = form_review.cleaned_data.get("rating")
            headline = form_review.cleaned_data.get("headline")
            body = form_review.cleaned_data.get("body")
            Review.objects.filter(id=review_id).update(
                ticket=ticket_of_review, rating=rating, user=request.user, headline=headline, body=body,
                time_created=timezone.now()
            )
            return redirect("my_posts")

    if request.method == 'GET':
        form_review = forms.ReviewForm()
        context = {
            "ticket_of_review": ticket_of_review,
            "form_review": form_review,
        }
    return render(request, "review/update_review.html", context=context)


@login_required
def delete_review(request, ticket_id, review_id):

    if request.method == 'POST':
        Review.objects.filter(id=review_id).delete()
        return redirect("my_posts")
