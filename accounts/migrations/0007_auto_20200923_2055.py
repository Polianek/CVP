# Generated by Django 3.0.5 on 2020-09-23 18:55

from django.db import migrations, models
import ponytoon.validators


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20200920_0533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='profile.png', upload_to='avatars', validators=[ponytoon.validators.validate_file_size]),
        ),
    ]