# Generated by Django 4.1.5 on 2023-01-23 15:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0004_dimensiondate_year'),
    ]

    operations = [
        migrations.CreateModel(
            name='DimensionHappiness',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('level', models.CharField(max_length=150, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='factresponse',
            name='dim_happiness',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='analytics.dimensionhappiness'),
            preserve_default=False,
        ),
    ]
