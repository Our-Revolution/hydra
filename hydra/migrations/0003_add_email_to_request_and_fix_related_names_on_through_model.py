# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-30 18:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import hydra.fields


class Migration(migrations.Migration):

    dependencies = [
        ('hydra', '0002_zipcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventpromotionrequest',
            name='sender_display_name',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='eventpromotionrequest',
            name='sender_email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='eventpromotionrequestthrough',
            name='recipient',
            field=hydra.fields.CrossDatabaseForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='bsd.Constituent'),
        ),
    ]
