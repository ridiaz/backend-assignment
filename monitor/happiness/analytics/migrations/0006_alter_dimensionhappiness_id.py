# Generated by Django 4.1.5 on 2023-01-23 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0005_dimensionhappiness_factresponse_dim_happiness'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dimensionhappiness',
            name='id',
            field=models.CharField(max_length=250, primary_key=True, serialize=False),
        ),
    ]
