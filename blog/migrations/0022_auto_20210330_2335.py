# Generated by Django 3.1.4 on 2021-03-30 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0021_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='video',
            field=models.FileField(default='default.mp4', upload_to='video/%y'),
        ),
        migrations.AlterField(
            model_name='post',
            name='release_date',
            field=models.CharField(default='30/03/2021', max_length=100),
        ),
        migrations.AlterField(
            model_name='watchlater',
            name='release_date',
            field=models.CharField(default='30/03/2021', max_length=100),
        ),
    ]
