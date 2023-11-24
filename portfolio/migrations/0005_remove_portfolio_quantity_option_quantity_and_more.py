# Generated by Django 4.2.6 on 2023-11-24 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0004_alter_portfolio_name_alter_portfolio_unique_together'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='portfolio',
            name='quantity',
        ),
        migrations.AddField(
            model_name='option',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='stock',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
    ]
