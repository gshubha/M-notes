# Generated by Django 3.1.5 on 2021-08-03 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('owner', models.CharField(max_length=32)),
                ('head', models.CharField(max_length=32)),
                ('content', models.CharField(max_length=1048576)),
                ('md', models.CharField(default='A', max_length=1048576)),
            ],
        ),
    ]
