# Generated by Django 2.2.10 on 2020-03-23 16:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ponytoon', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='upload',
            name='reputation',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='upload',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='uploads', to='ponytoon.Tag'),
        ),
        migrations.AlterField(
            model_name='upload',
            name='visible',
            field=models.BooleanField(default=True),
        ),
    ]
