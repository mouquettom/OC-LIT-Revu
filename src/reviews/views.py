from itertools import chain

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404

from accounts.models import Follow
from reviews.forms import ReviewForm
from reviews.models import Review
from tickets.forms import TicketForm
from tickets.models import Ticket


User = get_user_model()


def index(request):
    if request.user.is_authenticated:
        return redirect('feed', username=request.user.username)

    return render(request, 'reviews/index.html')


@login_required
def feed(request, username=None):
    is_own_feed = (username is None) or (username == request.user.username)

    if is_own_feed:
        profile_user = request.user
        followed_users = request.user.followings.all()

        tickets_qs = Ticket.objects.filter(
            Q(user=request.user) | Q(user__in=followed_users)
        ).select_related('user')

        reviews_qs = Review.objects.filter(
            Q(user=request.user) |
            Q(user__in=followed_users) |
            Q(ticket__user=request.user)
        ).select_related('user', 'ticket', 'ticket__user').distinct()

    else:
        profile_user = get_object_or_404(User, username=username)

        tickets_qs = Ticket.objects.filter(user=profile_user).select_related('user')
        reviews_qs = Review.objects.filter(user=profile_user).select_related(
            'user', 'ticket', 'ticket__user'
        )

    items = sorted(
        chain(tickets_qs, reviews_qs),
        key=lambda item: item.created_at,
        reverse=True,
    )

    reviewed_ids = set(
        Review.objects.filter(user=request.user).values_list('ticket_id', flat=True)
    )

    is_followed = False
    if not is_own_feed:
        is_followed = Follow.objects.filter(
            follower=request.user,
            following=profile_user,
        ).exists()

    context = {
        'items': items,
        'profile_user': profile_user,
        'is_own_feed': is_own_feed,
        'is_followed': is_followed,
        'reviewed_ids': reviewed_ids,
    }

    return render(request, 'reviews/feed.html', context)


@login_required
def review_pick_ticket(request):
    followed_users = request.user.followings.all()

    tickets = Ticket.objects.filter(
        user__in=followed_users
    ).exclude(
        review__user=request.user
    ).select_related('user').distinct().order_by('-created_at')

    return render(request, 'reviews/review_pick_ticket.html', {'tickets': tickets})


@login_required
def review_create_for_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket.objects.select_related('user'), id=ticket_id)

    if ticket.user == request.user:
        messages.error(request, "Tu ne peux pas critiquer ton propre billet.")
        return redirect('ticket_detail', ticket_id=ticket.id)

    if Review.objects.filter(ticket=ticket, user=request.user).exists():
        messages.error(request, "Tu as déjà publié une critique sur ce billet.")
        return redirect('ticket_detail', ticket_id=ticket.id)

    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            return redirect('feed', username=request.user.username)

    return render(
        request,
        'reviews/review_create_for_ticket.html',
        {
            'form': form,
            'ticket': ticket,
        }
    )


@login_required
def review_create_with_ticket(request):
    ticket_form = TicketForm(prefix='ticket')
    review_form = ReviewForm(prefix='review')

    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES, prefix='ticket')
        review_form = ReviewForm(request.POST, prefix='review')

        if ticket_form.is_valid() and review_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()

            review = review_form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()

            return redirect('feed', username=request.user.username)

    context = {
        'ticket_form': ticket_form,
        'review_form': review_form,
    }
    return render(request, 'reviews/review_create_with_ticket.html', context)


@login_required
def review_edit(request, review_id):
    review = get_object_or_404(
        Review.objects.select_related('ticket', 'user'),
        id=review_id,
    )

    if review.user != request.user:
        return HttpResponseForbidden("Tu ne peux pas modifier cette critique.")

    form = ReviewForm(instance=review)

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('ticket_detail', ticket_id=review.ticket.id)

    return render(
        request,
        'reviews/review_edit.html',
        {
            'form': form,
            'review': review,
        }
    )


@login_required
def review_delete(request, review_id):
    review = get_object_or_404(
        Review.objects.select_related('ticket', 'user'),
        id=review_id,
    )

    if review.user != request.user:
        return HttpResponseForbidden("Tu ne peux pas supprimer cette critique.")

    ticket_id = review.ticket.id

    if request.method == 'POST':
        review.delete()
        return redirect('ticket_detail', ticket_id=ticket_id)

    return render(
        request,
        'reviews/review_confirm_delete.html',
        {
            'review': review,
        }
    )