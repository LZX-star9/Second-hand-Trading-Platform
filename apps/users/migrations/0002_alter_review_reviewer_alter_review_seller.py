# Generated by Django 4.2.18 on 2025-03-10 15:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='reviewer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='given_reviews', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='review',
            name='seller',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='received_reviews', to=settings.AUTH_USER_MODEL),
        ),
    ]
