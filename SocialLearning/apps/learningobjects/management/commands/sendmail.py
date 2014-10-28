# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from comercios.models import *
import smtplib
import csv, codecs
from unidecode import unidecode
from geopy.geocoders import GoogleV3
from optparse import make_option

from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from django.core.mail import send_mail, EmailMessage
class Command(BaseCommand):
    args = 'file'
    help = u'enviar contraseñas'

    option_list = BaseCommand.option_list + (
        make_option('-f','--file',
            dest='filename',
            help='Nombre del archivo a cargar'),
        )

    def handle(self, *args, **options):
        headers = {'Reply-To': 'asociados@areacomercial.com'}
        remitente = u"Ensanche Área Comercial  <asociados@areacomercial.com>"
        asunto = u"Acceso asociados a Área Comercial" 
        texto = u"""Hola!<br/> <br/> 
                     Ya puede acceder a su panel de administrador de comercio en <a href="http://www.areacomercial.com/">areacomercial.com</a><br/> <br/> 
                  """        

        if options['filename'] == None:
            raise CommandError("Option `--file=...` must be specified.")
        else:

            with open(options['filename'], 'rb') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',')
                for row in spamreader:        
                    destinatario = row[0]
                    password = row[1]

                    mensaje = u"""%s
                        Su contraseña es: %s
                     """ % (texto, password) 

                    correo = u"""From: %s 
To: %s 
MIME-Version: 1.0 
Content-type: text/html 
Subject: %s 
 
%s
""" % (remitente, destinatario, asunto, mensaje) 
                    #send_mail(asunto, mensaje, 'web@areacomercial.com', [destinatario], fail_silently=False)
                    try: 

                        msg = EmailMessage(asunto, mensaje, 'web@areacomercial.com', [destinatario], headers=headers)
                        msg.content_subtype = "html"
                        msg.send()

                        #send_mail(asunto, mensaje, 'web@areacomercial.com', [destinatario], fail_silently=False)
                        print u"Correo enviado a %s" % destinatario
                    except: 
                        print u"Error: el mensaje a %s no pudo enviarse." % destinatario