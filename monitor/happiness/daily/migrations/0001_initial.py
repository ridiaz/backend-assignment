# Generated by Django 4.1.5 on 2023-01-21 21:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('team', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckIn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('responses', models.JSONField(default=[])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='team.team')),
            ],
        ),
    ]
