# Generated by Django 3.1.4 on 2021-03-20 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20210321_0019'),
    ]

    operations = [
        migrations.AddField(
            model_name='bedrequest',
            name='age',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='bedrequest',
            name='ambulance_required',
            field=models.CharField(default=1, max_length=16),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bedrequest',
            name='city',
            field=models.CharField(default=1, max_length=16),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bedrequest',
            name='co_mobidity',
            field=models.CharField(default=1, max_length=16),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bedrequest',
            name='gender',
            field=models.CharField(default=1, max_length=16),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bedrequest',
            name='health_centre',
            field=models.CharField(default='KEM', max_length=16),
        ),
        migrations.AddField(
            model_name='bedrequest',
            name='pin_code',
            field=models.IntegerField(default=1, max_length=6),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bedrequest',
            name='scheme',
            field=models.CharField(default=1, max_length=16),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bedrequest',
            name='symptoms',
            field=models.CharField(default=1, max_length=16),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bedrequest',
            name='tested',
            field=models.CharField(default=1, max_length=16),
            preserve_default=False,
        ),
    ]