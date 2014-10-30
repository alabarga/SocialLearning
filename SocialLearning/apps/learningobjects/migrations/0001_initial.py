# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import redactor.fields
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Mention',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('card', redactor.fields.RedactorField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('identifier', models.CharField(max_length=20, null=True, blank=True)),
                ('title', models.CharField(max_length=255)),
                ('url', models.URLField()),
                ('description', redactor.fields.RedactorField(null=True, blank=True)),
                ('last_processed', models.DateTimeField(null=True, blank=True)),
                ('status', models.IntegerField(default=0, choices=[(0, b'Added'), (1, b'Described'), (2, b'Discovered'), (3, b'Expanded')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ResourceContainer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField()),
                ('rss', models.URLField()),
                ('name', models.CharField(max_length=255, null=True, blank=True)),
                ('descripcion', redactor.fields.RedactorField(null=True, blank=True)),
                ('last_processed', models.DateTimeField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Scores',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('topic', models.CharField(max_length=255)),
                ('score', models.FloatField()),
                ('resource', models.ForeignKey(related_name=b'scores', to='learningobjects.Resource')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SocialNetwork',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('descripcion', redactor.fields.RedactorField(null=True, blank=True)),
                ('url', models.URLField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SocialProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=255)),
                ('url', models.URLField(max_length=255)),
                ('descripcion', redactor.fields.RedactorField(null=True, blank=True)),
                ('social_network', models.ForeignKey(related_name=b'profiles', to='learningobjects.SocialNetwork')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='resource',
            name='container',
            field=models.ForeignKey(related_name=b'resources', blank=True, to='learningobjects.ResourceContainer', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='resource',
            name='seen_at',
            field=models.ManyToManyField(related_name=b'resources', null=True, through='learningobjects.Mention', to='learningobjects.SocialProfile', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='resource',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='mention',
            name='profile',
            field=models.ForeignKey(related_name=b'mentions', to='learningobjects.SocialProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='mention',
            name='resource',
            field=models.ForeignKey(related_name=b'mention', to='learningobjects.Resource'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='mention',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='collection',
            name='resources',
            field=models.ManyToManyField(related_name=b'collections', null=True, to='learningobjects.Resource', blank=True),
            preserve_default=True,
        ),
    ]
