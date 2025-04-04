# Generated by Django 5.1.7 on 2025-03-31 13:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('reply_like', '0001_initial'),
        ('utilisateurs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='replylike',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='utilisateurs.user'),
        ),
        migrations.AlterUniqueTogether(
            name='replylike',
            unique_together={('reply', 'user')},
        ),
    ]
