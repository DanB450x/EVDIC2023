# Generated by Django 4.2.5 on 2023-11-03 04:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('principal', '0010_curso_cantidad_estudiantes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Docente',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='curso',
            name='docentes',
            field=models.ManyToManyField(to='principal.docente'),
        ),
    ]