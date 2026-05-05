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
                ('medium', models.CharField(blank=True, choices=[('Oil', 'Oil'), ('Water', 'Water'), ('Acrylic', 'Acrylic')], max_length=50, null=True)),
                ('style', models.CharField(blank=True, choices=[('Impressionism', 'Impressionism'), ('Modernism', 'Modernism'), ('Surrealism', 'Surrealism'), ('Realism', 'Realism')], max_length=50, null=True)),
                ('starting_bid_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('width_cm', models.DecimalField(decimal_places=2, max_digits=6)),
                ('height_cm', models.DecimalField(decimal_places=2, max_digits=6)),
                ('year_created', models.IntegerField()),
                ('is_sold', models.BooleanField(default=False)),
                ('main_image', models.ImageField(blank=True, null=True, upload_to='artworks/')),
                ('description', models.TextField(blank=True)),
            ],
        )
    ]
