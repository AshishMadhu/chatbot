# Generated by Django 3.2.5 on 2021-07-10 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ResponseCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(choices=[['telegram', 'Telegram'], ['ws', 'Websocket']], max_length=10)),
                ('stupid_count', models.PositiveIntegerField(default=0)),
                ('fat_count', models.PositiveIntegerField(default=0)),
                ('dumb_count', models.PositiveIntegerField(default=0)),
                ('user_name', models.CharField(max_length=50)),
            ],
        ),
    ]
