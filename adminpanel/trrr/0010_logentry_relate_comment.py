# Generated by Django 3.0.5 on 2020-07-25 20:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ponytoon', '0004_auto_20200328_0100'),
        ('adminpanel', '0009_suggestions'),
    ]

    operations = [
        migrations.AddField(
            model_name='logentry',
            name='relate_comment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='logentrys_comment', to='ponytoon.Comment'),
        ),
    ]
