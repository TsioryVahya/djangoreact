# Generated by Django 5.1.7 on 2025-03-31 16:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('conversations', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='conversation',
            name='id_participant1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conversations_initiees', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='conversation',
            name='id_participant2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conversations_recues', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='conversation',
            unique_together={('id_participant1', 'id_participant2')},
        ),
    ]
