# Generated by Django 5.0.7 on 2024-09-28 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0005_alter_customuser_managers'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='domain_user',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]