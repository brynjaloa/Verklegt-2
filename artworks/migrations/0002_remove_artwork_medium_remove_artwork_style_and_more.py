# This migration belongs to an older branch. The current artwork schema is
# represented by 0002_seller_update_artwork_schema and later migrations, so
# keep this applied migration as a no-op for graph compatibility.
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('artworks', '0001_initial'),
    ]

    operations = []
