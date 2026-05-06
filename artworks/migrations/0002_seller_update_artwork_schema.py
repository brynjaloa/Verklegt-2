from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("artworks", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Seller",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255)),
                (
                    "seller_type",
                    models.CharField(
                        choices=[("Individual", "Individual"), ("Gallery", "Gallery")],
                        max_length=20,
                    ),
                ),
                ("bio", models.TextField(blank=True)),
                ("logo", models.ImageField(blank=True, null=True, upload_to="sellers/logos/")),
                ("cover_image", models.ImageField(blank=True, null=True, upload_to="sellers/covers/")),
                ("street_name", models.CharField(blank=True, max_length=255, null=True)),
                ("city", models.CharField(blank=True, max_length=255, null=True)),
                ("postal_code", models.CharField(blank=True, max_length=20, null=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="artwork",
            name="category",
            field=models.CharField(
                choices=[
                    ("Furniture", "Furniture"),
                    ("Paintings", "Paintings"),
                    ("Sculptures", "Sculptures"),
                    ("Photos", "Photos"),
                    ("Jewellery", "Jewellery"),
                ],
                default="Paintings",
                max_length=50,
            ),
        ),
        migrations.AddField(
            model_name="artwork",
            name="created_at",
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="artwork",
            name="material",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="artwork",
            name="seller",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="artworks",
                to="artworks.seller",
            ),
        ),
        migrations.AddField(
            model_name="artwork",
            name="style",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="artwork",
            name="technique_or_medium",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.RemoveField(
            model_name="artwork",
            name="furniture_material",
        ),
        migrations.RemoveField(
            model_name="artwork",
            name="furniture_style",
        ),
        migrations.RemoveField(
            model_name="artwork",
            name="jewellery_material",
        ),
        migrations.RemoveField(
            model_name="artwork",
            name="jewellery_style",
        ),
        migrations.RemoveField(
            model_name="artwork",
            name="painting_medium",
        ),
        migrations.RemoveField(
            model_name="artwork",
            name="painting_style",
        ),
        migrations.RemoveField(
            model_name="artwork",
            name="photo_style",
        ),
        migrations.RemoveField(
            model_name="artwork",
            name="photo_technique",
        ),
        migrations.RemoveField(
            model_name="artwork",
            name="sculpture_material",
        ),
        migrations.RemoveField(
            model_name="artwork",
            name="sculpture_style",
        ),
    ]
