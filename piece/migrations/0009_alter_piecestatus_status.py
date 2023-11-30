# Generated by Django 4.2.6 on 2023-11-30 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('piece', '0008_alter_piecestatus_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='piecestatus',
            name='status',
            field=models.CharField(choices=[('finished', 'Finished'), ('abandoned', 'Abandoned'), ('in_progress', 'In Progress'), ('paused', 'Paused'), ('hoping_to_start', 'Hoping to Start')], max_length=20),
        ),
    ]
