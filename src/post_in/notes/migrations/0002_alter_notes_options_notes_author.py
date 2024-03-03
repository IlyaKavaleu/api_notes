# Generated by Django 5.0.2 on 2024-03-02 10:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notes',
            options={'ordering': ['-updated'], 'verbose_name': 'Note', 'verbose_name_plural': 'Notes'},
        ),
        migrations.AddField(
            model_name='notes',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]