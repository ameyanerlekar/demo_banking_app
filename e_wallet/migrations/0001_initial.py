# Generated by Django 2.2.2 on 2019-06-19 11:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('username', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=15)),
                ('last_name', models.CharField(max_length=15)),
                ('address', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('account_number', models.IntegerField(primary_key=True, serialize=False)),
                ('account_balance', models.FloatField()),
                ('is_frozen', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='e_wallet.Client')),
            ],
        ),
    ]
