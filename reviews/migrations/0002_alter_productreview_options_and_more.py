# Generated by Django 4.2.17 on 2025-03-03 11:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_delete_review'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productreview',
            options={'ordering': ['-created_at'], 'verbose_name': 'Product Review', 'verbose_name_plural': 'Product Reviews'},
        ),
        migrations.AlterField(
            model_name='productreview',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, help_text='When the review was created'),
        ),
        migrations.AlterField(
            model_name='productreview',
            name='product',
            field=models.ForeignKey(help_text='The product being reviewed', on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='products.product'),
        ),
        migrations.AlterField(
            model_name='productreview',
            name='rating',
            field=models.IntegerField(choices=[(1, '1 - Poor'), (2, '2 - Fair'), (3, '3 - Good'), (4, '4 - Very Good'), (5, '5 - Excellent')], help_text='Rating from 1 (Poor) to 5 (Excellent)'),
        ),
        migrations.AlterField(
            model_name='productreview',
            name='review_text',
            field=models.TextField(help_text='The actual review text'),
        ),
        migrations.AlterField(
            model_name='productreview',
            name='user',
            field=models.ForeignKey(help_text='The user who wrote the review', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
