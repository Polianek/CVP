# Generated by Django 2.2.10 on 2020-03-28 18:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('adminpanel', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='logentry',
            name='user_id',
        ),
        migrations.AddField(
            model_name='logentry',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='logentrys_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='logentry',
            name='action',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logentrys_action', to='adminpanel.LogAction'),
        ),
        migrations.AlterField(
            model_name='logentry',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logentrys_category', to='adminpanel.LogCategory'),
        ),
    ]
