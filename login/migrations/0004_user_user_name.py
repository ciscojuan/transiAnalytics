# Generated by Django 2.1.2 on 2018-11-10 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0003_remove_user_user_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_name',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
