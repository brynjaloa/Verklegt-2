from bids.models import Bid


def accepted_bid_notifications(request):
    if not request.user.is_authenticated:
        return {
            "accepted_bid_count": 0,
        }

    seller = getattr(request.user, "seller", None)
    canceled_bid_count = 0

    if seller is not None:
        canceled_bid_count = Bid.objects.filter(
            artwork__seller=seller,
            status=Bid.Status.CANCELED,
            seller_cancel_notification_seen=False,
        ).count()

    return {
        "accepted_bid_count": (
            Bid.objects.filter(
                user=request.user,
                status=Bid.Status.ACCEPTED,
                buyer_accept_notification_seen=False,
            ).count()
            + canceled_bid_count
        ),
    }
