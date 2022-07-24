# Generated by Django 4.0.5 on 2022-07-24 12:42

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('livros_app', '0009_alter_emprestimos_data_emprestimo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emprestimos',
            name='data_emprestimo',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 24, 9, 42, 33, 660550)),
        ),
        migrations.AlterField(
            model_name='emprestimos',
            name='livro',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='livros_app.livros'),
            preserve_default=False,
        ),
    ]
