from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ContactInformationForm, PaymentInformationForm
from .models import Bid


FINALIZE_STEPS = ["contact", "payment", "review", "confirmation"]
PAYMENT_LABELS = {
    "credit_card": "Credit card",
    "bank_transfer": "Bank transfer",
    "wire_transfer": "Wire transfer",
}


def get_finalize_session_key(bid):
    return f"finalize_bid_{bid.id}"


def form_data_for_session(form):
    return {
        field_name: str(value)
        for field_name, value in form.cleaned_data.items()
        if value not in (None, "")
    }


@login_required
def cancel_bid(request, bid_id):

    bid = get_object_or_404(
        Bid,
        id=bid_id,
        user=request.user
    )

    artwork_id = bid.artwork.id

    if bid.status in {Bid.Status.ACCEPTED, Bid.Status.CONTINGENT}:
        bid.status = Bid.Status.CANCELED
        bid.seller_cancel_notification_seen = False
        bid.save(update_fields=["status", "seller_cancel_notification_seen"])

        has_active_accepted_bid = Bid.objects.filter(
            artwork=bid.artwork,
            status__in=[Bid.Status.ACCEPTED, Bid.Status.FINALIZED],
        ).exists()

        if not has_active_accepted_bid:
            bid.artwork.is_sold = False
            bid.artwork.save(update_fields=["is_sold"])
    else:
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

    if Bid.objects.filter(
        artwork=bid.artwork,
        status__in=[Bid.Status.ACCEPTED, Bid.Status.FINALIZED],
    ).exclude(id=bid.id).exists():
        return redirect("artwork_detail", pk=bid.artwork.id)

    Bid.objects.filter(artwork=bid.artwork).exclude(id=bid.id).update(
        status=Bid.Status.REJECTED
    )

    bid.status = "Accepted"
    bid.buyer_accept_notification_seen = False
    bid.save(update_fields=["status", "buyer_accept_notification_seen"])
    bid.artwork.is_sold = True
    bid.artwork.save(update_fields=["is_sold"])

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


@login_required
def finalize_bid(request, bid_id, step="contact"):
    bid = get_object_or_404(
        Bid.objects.select_related("artwork", "artwork__seller", "user"),
        id=bid_id,
        user=request.user,
    )

    if bid.status not in {Bid.Status.ACCEPTED, Bid.Status.CONTINGENT, Bid.Status.FINALIZED}:
        return HttpResponseForbidden("Only accepted or contingent bids can be finalized.")

    if step not in FINALIZE_STEPS:
        return redirect("finalize_bid", bid_id=bid.id)

    session_key = get_finalize_session_key(bid)
    finalize_data = request.session.get(session_key, {})

    if step == "confirmation":
        if bid.status != Bid.Status.FINALIZED:
            return redirect("finalize_bid_step", bid_id=bid.id, step="review")

        return render(request, "bids/finalize_bid.html", {
            "bid": bid,
            "step": step,
            "steps": FINALIZE_STEPS,
        })

    contact_data = finalize_data.get("contact", {})
    payment_data = finalize_data.get("payment", {})

    if step == "contact":
        if request.method == "POST":
            form = ContactInformationForm(request.POST)

            if form.is_valid():
                finalize_data["contact"] = form_data_for_session(form)
                request.session[session_key] = finalize_data
                request.session.modified = True
                return redirect("finalize_bid_step", bid_id=bid.id, step="payment")
        else:
            form = ContactInformationForm(initial=contact_data)

        return render(request, "bids/finalize_bid.html", {
            "bid": bid,
            "step": step,
            "steps": FINALIZE_STEPS,
            "form": form,
        })

    if step == "payment":
        if not contact_data:
            return redirect("finalize_bid", bid_id=bid.id)

        if request.method == "POST" and request.POST.get("direction") == "back":
            return redirect("finalize_bid", bid_id=bid.id)

        if request.method == "POST":
            form = PaymentInformationForm(request.POST)

            if form.is_valid():
                finalize_data["payment"] = form_data_for_session(form)
                request.session[session_key] = finalize_data
                request.session.modified = True
                return redirect("finalize_bid_step", bid_id=bid.id, step="review")
        else:
            initial_data = {"payment_option": "credit_card"}
            initial_data.update(payment_data)
            form = PaymentInformationForm(initial=initial_data)

        return render(request, "bids/finalize_bid.html", {
            "bid": bid,
            "step": step,
            "steps": FINALIZE_STEPS,
            "form": form,
        })

    if step == "review":
        if not contact_data:
            return redirect("finalize_bid", bid_id=bid.id)
        if not payment_data:
            return redirect("finalize_bid_step", bid_id=bid.id, step="payment")

        if request.method == "POST":
            if request.POST.get("direction") == "back":
                return redirect("finalize_bid_step", bid_id=bid.id, step="payment")

            bid.status = Bid.Status.FINALIZED
            bid.save()
            Bid.objects.filter(artwork=bid.artwork).exclude(id=bid.id).update(
                status=Bid.Status.REJECTED
            )
            bid.artwork.is_sold = True
            bid.artwork.save(update_fields=["is_sold"])

            if session_key in request.session:
                del request.session[session_key]

            return redirect("finalize_bid_step", bid_id=bid.id, step="confirmation")

        return render(request, "bids/finalize_bid.html", {
            "bid": bid,
            "step": step,
            "steps": FINALIZE_STEPS,
            "contact_data": contact_data,
            "payment_data": payment_data,
            "payment_label": PAYMENT_LABELS.get(payment_data.get("payment_option")),
        })

    return redirect("finalize_bid", bid_id=bid.id)
