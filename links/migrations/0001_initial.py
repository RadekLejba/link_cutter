# Generated by Django 2.1.7 on 2019-04-06 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('url', models.URLField(max_length=10000)),
                ('visits', models.IntegerField(default=0)),
                ('shortcut', models.CharField(max_length=20, primary_key=True, serialize=False, unique=True)),
                ('sender_ip', models.CharField(max_length=20, null=True)),
                ('sender_system_info', models.TextField(null=True)),
                ('sender_referer', models.TextField(null=True)),
            ],
        ),
    ]
