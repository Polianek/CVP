# Generated by Django 3.0.5 on 2020-07-14 16:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ponytoon', '0004_auto_20200328_0100'),
        ('adminpanel', '0005_report_reportcategory'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='relate_comment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reports_comment', to='ponytoon.Comment'),
        ),
    ]