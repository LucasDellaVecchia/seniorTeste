# Generated by Django 5.1.2 on 2024-10-24 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vagas', '0005_alter_candidatos_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vagas',
            name='data',
            field=models.DateField(),
        ),
    ]
