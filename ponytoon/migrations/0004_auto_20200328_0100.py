# Generated by Django 2.2.10 on 2020-03-28 01:00

from django.db import migrations, models
import ponytoon.models
import ponytoon.validators


class Migration(migrations.Migration):

    dependencies = [
        ('ponytoon', '0003_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='upload',
            name='pic',
            field=models.ImageField(upload_to=ponytoon.models.upload_to, validators=[ponytoon.validators.validate_file_size]),
        ),
    ]
