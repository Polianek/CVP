# Generated by Django 3.0.5 on 2020-07-26 22:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ponytoon', '0004_auto_20200328_0100'),
        ('adminpanel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='votes',
            name='comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='ponytoon.Comment'),
        ),
        migrations.AlterField(
            model_name='votes',
            name='post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='ponytoon.Upload'),
        ),
    ]
