# Generated by Django 3.1.7 on 2021-04-03 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0002_auto_20210401_0828'),
    ]

    operations = [
        migrations.AddField(
            model_name='discussion',
            name='description',
            field=models.TextField(default='NULL'),
            preserve_default=False,
        ),
    ]
