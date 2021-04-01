# Generated by Django 3.1.4 on 2021-04-01 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0022_auto_20210330_2335'),
    ]

    operations = [
        migrations.CreateModel(
            name='Liked',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(default='Unknown', max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('type', models.CharField(default='Unknown', max_length=100)),
                ('content', models.TextField(default='Unknown')),
                ('director', models.CharField(default='Unknown', max_length=100)),
                ('cast', models.CharField(default='Unknown', max_length=100)),
                ('country', models.CharField(default='Unknown', max_length=100)),
                ('genres', models.TextField(default='Unknown', max_length=100)),
                ('duration', models.CharField(default='Unknown', max_length=100)),
                ('release_date', models.CharField(default='01/04/2021', max_length=100)),
                ('likes', models.IntegerField(default=0)),
            ],
        ),
        migrations.AlterField(
            model_name='post',
            name='release_date',
            field=models.CharField(default='01/04/2021', max_length=100),
        ),
        migrations.AlterField(
            model_name='watchlater',
            name='release_date',
            field=models.CharField(default='01/04/2021', max_length=100),
        ),
    ]
