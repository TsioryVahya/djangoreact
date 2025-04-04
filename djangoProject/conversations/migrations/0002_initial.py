# Generated by Django 5.1.7 on 2025-03-31 13:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('conversations', '0001_initial'),
        ('utilisateurs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversation',
            name='participant1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conv_participant1', to='utilisateurs.user'),
        ),
        migrations.AddField(
            model_name='conversation',
            name='participant2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conv_participant2', to='utilisateurs.user'),
        ),
    ]
