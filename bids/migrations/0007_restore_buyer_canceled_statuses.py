from django.db import migrations


def restore_buyer_canceled_statuses(apps, schema_editor):
    Bid = apps.get_model("bids", "Bid")

    Bid.objects.filter(
        buyer_canceled=True,
    ).exclude(
        status__in=["Canceled", "Finalized"],
    ).update(
        status="Canceled",
        buyer_reject_notification_seen=True,
    )


class Migration(migrations.Migration):

    dependencies = [
        ("bids", "0006_bid_buyer_canceled"),
    ]

    operations = [
        migrations.RunPython(
            restore_buyer_canceled_statuses,
            migrations.RunPython.noop,
        ),
    ]
