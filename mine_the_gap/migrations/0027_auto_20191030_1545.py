# Generated by Django 2.0.13 on 2019-10-30 15:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mine_the_gap', '0026_auto_20191030_1542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estimated_data',
            name='region',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mine_the_gap.Region'),
        ),
    ]
