# Generated by Django 3.2.5 on 2021-07-10 07:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='responsecount',
            old_name='user_name',
            new_name='username',
        ),
    ]
