# Generated by Django 2.0.5 on 2018-05-08 15:01

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='ArticleVersion',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('Published', 'Published'), ('Unpublished', 'Unpublished')], default='Unpublished', max_length=50)),
                ('version', models.IntegerField()),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='versions', to='articles.Article')),
            ],
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('language', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=250)),
                ('text', models.TextField(blank=True, null=True)),
                ('article_version', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='content_items', to='articles.ArticleVersion')),
            ],
        ),
    ]
