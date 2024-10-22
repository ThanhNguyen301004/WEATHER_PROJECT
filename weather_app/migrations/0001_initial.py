# Generated by Django 5.1.1 on 2024-10-21 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('image', models.ImageField(upload_to='img/')),
                ('description', models.TextField()),
                ('pdf', models.FileField(upload_to='pdf/')),
            ],
        ),
    ]