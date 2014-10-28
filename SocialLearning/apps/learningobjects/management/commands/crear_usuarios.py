# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from comercios.models import *

import csv, codecs
from unidecode import unidecode
from geopy.geocoders import GoogleV3
from optparse import make_option

from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string

class Command(BaseCommand):
    args = 'file'
    help = 'generar usuarios'

    option_list = BaseCommand.option_list + (
        make_option('-f','--file',
            dest='filename',
            help='Nombre del archivo a cargar'),
        )

    User = get_user_model()

    def handle(self, *args, **options):

        if options['filename'] == None:
            raise CommandError("Option `--file=...` must be specified.")
        else:
            with open(options['filename'], 'rb') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',')
                for row in spamreader:        
                    email = row[0]
                    try:
                        password = get_random_string()
                        user = User.objects.create_user(email, email, password)
                        user.save()
                        print "%s,%s" % (email,password)
                    except:
                        print "%s failed!" % email