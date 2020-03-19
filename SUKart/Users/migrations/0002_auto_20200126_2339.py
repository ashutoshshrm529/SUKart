# Generated by Django 3.0.2 on 2020-01-26 23:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kartuser',
            name='city',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='Users.City'),
        ),
        migrations.AlterField(
            model_name='kartuser',
            name='dob',
            field=models.DateField(null=True),
        ),
    ]
