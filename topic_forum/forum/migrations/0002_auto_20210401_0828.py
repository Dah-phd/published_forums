# Generated by Django 3.1.7 on 2021-04-01 08:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='user',
            field=models.ForeignKey(default=7, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL),
        ),
    ]
