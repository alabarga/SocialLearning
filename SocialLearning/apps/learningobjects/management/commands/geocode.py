# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from comercios.models import *

import csv, codecs
from unidecode import unidecode
from geopy.geocoders import GoogleV3
from optparse import make_option

class Command(BaseCommand):
    args = 'file'
    help = 'Geolocaliza los comercios'

    option_list = BaseCommand.option_list + (
        make_option('-f','--file',
            dest='filename',
            help='Nombre del archivo a cargar'),
        )

    def handle(self, *args, **options):

        if options['filename'] == None:
            asociados = Asociado.objects.all()
            for asociado in asociados:
                print asociado.direccion
        else:
            with open(options['filename'], 'rb') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',')
                for row in spamreader:        
                    nombre = row[0]
                    try:
                        asociado = Asociado.objects.get(nombre=nombre)
                        latitude = row[1]
                        longitude = row[2]
                        asociado.location.latitude = latitude
                        asociado.location.longitude = longitude
                        asociado.save()
                        #print asociado.nombre
                    except:
                        print "Not found=%s" % nombre
                        

            
