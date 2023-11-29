# Generated by Django 4.2.6 on 2023-11-29 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('piece', '0007_rename_ratimg_piecestatus_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='piecestatus',
            name='rating',
            field=models.FloatField(blank=True, choices=[(0.5, '0.5'), (1.0, '1.0'), (1.5, '1.5'), (2.0, '2.0'), (2.5, '2.5'), (3.0, '3.0'), (3.5, '3.5'), (4.0, '4.0'), (4.5, '4.5'), (5.0, '5.0')], null=True),
        ),
    ]