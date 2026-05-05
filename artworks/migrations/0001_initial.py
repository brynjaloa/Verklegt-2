from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Artwork',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('starting_bid_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('width_cm', models.DecimalField(decimal_places=2, max_digits=6)),
                ('height_cm', models.DecimalField(decimal_places=2, max_digits=6)),
                ('year_created', models.IntegerField()),
                ('is_sold', models.BooleanField(default=False)),
                ('main_image', models.ImageField(blank=True, null=True, upload_to='artworks/')),
                ('description', models.TextField(blank=True)),
                ('furniture_material', models.CharField(blank=True, max_length=100, null=True)),
                ('furniture_style', models.CharField(blank=True, max_length=100, null=True)),
                ('jewellery_material', models.CharField(blank=True, max_length=100, null=True)),
                ('jewellery_style', models.CharField(blank=True, max_length=100, null=True)),
                ('painting_medium', models.CharField(blank=True, max_length=100, null=True)),
                ('painting_style', models.CharField(blank=True, max_length=100, null=True)),
                ('photo_style', models.CharField(blank=True, max_length=100, null=True)),
                ('photo_technique', models.CharField(blank=True, max_length=100, null=True)),
                ('sculpture_material', models.CharField(blank=True, max_length=100, null=True)),
                ('sculpture_style', models.CharField(blank=True, max_length=100, null=True)),
            ],
        )
    ]
