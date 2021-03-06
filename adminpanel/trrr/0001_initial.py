# Generated by Django 2.2.10 on 2020-03-28 10:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LogAction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logAction', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='LogCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logCategory', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='LogEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('ip', models.CharField(max_length=20)),
                ('desc', models.TextField(blank=True, max_length=800)),
                ('action', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logentrys', to='adminpanel.LogAction')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logentrys', to='adminpanel.LogCategory')),
            ],
        ),
    ]
