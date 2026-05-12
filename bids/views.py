from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect

from .models import Bid


@login_required
def cancel_bid(request, bid_id):

    bid = get_object_or_404(
        Bid,
        id=bid_id,
        user=request.user
    )

    artwork_id = bid.artwork.id

    bid.delete()

    return redirect(
        'artwork_detail',
        pk=artwork_id
    )

@login_required
def accept_bid(request, bid_id):

    bid = get_object_or_404(Bid, id=bid_id)

    if bid.artwork.seller != request.user.seller:
        return HttpResponseForbidden()

    bid.status = "Accepted"
    bid.save()

    return redirect("artwork_detail", pk=bid.artwork.id)


@login_required
def reject_bid(request, bid_id):
    bid = get_object_or_404(Bid, id=bid_id)

    if bid.artwork.seller != request.user.seller:
        return HttpResponseForbidden()

    bid.status = "Rejected"
    bid.save()

    return redirect('artwork_detail', pk=bid.artwork.id)


@login_required
def contingent_bid(request, bid_id):
    bid = get_object_or_404(Bid, id=bid_id)

    if bid.artwork.seller != request.user.seller:
        return HttpResponseForbidden()

    bid.status = "Contingent"
    bid.save()

    return redirect('artwork_detail', pk=bid.artwork.id)
