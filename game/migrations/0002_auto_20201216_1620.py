# Generated by Django 3.1.3 on 2020-12-16 15:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ai', '0002_auto_20201216_0303'),
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usergame',
            name='movePrecedent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='UserGames', to='ai.esperance'),
        ),
    ]
