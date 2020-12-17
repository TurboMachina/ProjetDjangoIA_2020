# Generated by Django 3.1.4 on 2020-12-17 13:02

import ai.validators
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ai', '0002_auto_20201216_0303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ai',
            name='epsilon_greedy',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='ai',
            name='gamma',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='ai',
            name='learning_rate',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='esperance',
            name='esperance',
            field=ai.validators.MinMaxFloat(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='state',
            name='turn',
            field=models.IntegerField(),
        ),
    ]
