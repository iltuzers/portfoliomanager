# Generated by Django 4.2.6 on 2023-11-24 15:34

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('portfolio', '0003_alter_portfolio_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portfolio',
            name='name',
            field=models.CharField(default='Default', max_length=32),
        ),
        migrations.AlterUniqueTogether(
            name='portfolio',
            unique_together={('name', 'owner')},
        ),
    ]
