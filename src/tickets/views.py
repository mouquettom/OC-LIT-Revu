from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect

from .forms import TicketForm
from .models import Ticket


@login_required
def ticket_create(request):
    form = TicketForm()

    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('ticket_detail', ticket_id=ticket.id)

    return render(request, 'tickets/ticket_create.html', {'form': form})


@login_required
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket.objects.select_related('user'), id=ticket_id)
    reviews = ticket.review.select_related('user').order_by('-created_at')

    return render(
        request,
        'tickets/ticket_detail.html',
        {
            'ticket': ticket,
            'reviews': reviews,
        }
    )


@login_required
def ticket_edit(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if ticket.user != request.user:
        return HttpResponseForbidden("Tu ne peux pas modifier ce billet.")

    form = TicketForm(instance=ticket)

    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('ticket_detail', ticket_id=ticket.id)

    return render(
        request,
        'tickets/ticket_edit.html',
        {
            'form': form,
            'ticket': ticket,
        }
    )


@login_required
def ticket_delete(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if ticket.user != request.user:
        return HttpResponseForbidden("Tu ne peux pas supprimer ce billet.")

    if request.method == 'POST':
        ticket.delete()
        return redirect('feed', username=request.user.username)

    return render(
        request,
        'tickets/ticket_confirm_delete.html',
        {
            'ticket': ticket,
        }
    )