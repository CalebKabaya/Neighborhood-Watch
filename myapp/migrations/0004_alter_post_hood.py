# Generated by Django 4.0.5 on 2022-06-19 18:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_alter_neighbourhood_admin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='hood',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hood_post', to='myapp.neighbourhood'),
        ),
    ]
