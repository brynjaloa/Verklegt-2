from django.db import migrations, models


def add_buyer_canceled_if_missing(apps, schema_editor):
    table_name = "bids_bid"
    existing_columns = {
        column.name
        for column in schema_editor.connection.introspection.get_table_description(
            schema_editor.connection.cursor(),
            table_name,
        )
    }

    if "buyer_canceled" in existing_columns:
        return

    Bid = apps.get_model("bids", "Bid")
    field = models.BooleanField(default=False)
    field.set_attributes_from_name("buyer_canceled")
    schema_editor.add_field(Bid, field)


def remove_buyer_canceled_if_present(apps, schema_editor):
    table_name = "bids_bid"
    existing_columns = {
        column.name
        for column in schema_editor.connection.introspection.get_table_description(
            schema_editor.connection.cursor(),
            table_name,
        )
    }

    if "buyer_canceled" not in existing_columns:
        return

    Bid = apps.get_model("bids", "Bid")
    field = Bid._meta.get_field("buyer_canceled")
    schema_editor.remove_field(Bid, field)


class Migration(migrations.Migration):

    dependencies = [
        ("bids", "0005_bid_buyer_reject_notification_seen"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunPython(
                    add_buyer_canceled_if_missing,
                    remove_buyer_canceled_if_present,
                ),
            ],
            state_operations=[
                migrations.AddField(
                    model_name="bid",
                    name="buyer_canceled",
                    field=models.BooleanField(default=False),
                ),
            ],
        ),
    ]
