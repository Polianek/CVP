# Generated by Django 2.2.10 on 2020-04-08 14:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ponytoon', '0004_auto_20200328_0100'),
        ('adminpanel', '0003_auto_20200328_1946'),
    ]

    operations = [
        migrations.AddField(
            model_name='logentry',
            name='relate',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='logentrys_upload', to='ponytoon.Upload'),
        ),
    ]
