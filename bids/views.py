from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

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