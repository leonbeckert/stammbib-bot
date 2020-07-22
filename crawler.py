#!/usr/bin/python
# -*- coding: latin-1 -*-
from bs4 import BeautifulSoup
import requests
import smtplib
import time



firstRunBool = 1
url = 'https://www.ub.tum.de/arbeitsplatz-reservieren?field_teilbibliothek_tid_selective=1415&field_tag_value_selective=All'

boolsone = [0] * 22

def crawl():
    stammbib = 0
    termine = ''
    page = requests.get(url)
    page.raise_for_status()
    soup = BeautifulSoup(page.text, "lxml")

    length = len(soup.find_all("", class_="views-field views-field-views-conditional internlink"))
    for i in range(1, length):
        found = soup.find_all("", class_="views-field views-field-views-conditional internlink")[i]
        date = str(soup.find_all("", class_="views-field views-field-field-tag")[i]).split('>', 3)[2].split('<', 2)[0]
        time = str(soup.find_all("", class_="views-field views-field-field-zeitslot")[i]).split('>', 2)[1].split('<', 2)[0].split(' ', 12)[12].split('  ', 2)[0]
        rescheck = str(found).split('>', 3)[2].split('<', 2)[0]

        if rescheck == "Zur Reservierung":
            boolsone[i] = 1;
            termine += "\n"
            termine += date
            termine += ", "
            termine += time
            stammbib += 1
        else:
            boolsone[i] = 0;

    sendemail = 0
    for i in range(0, 22):
        if boolsone[i] == 1:
            sendemail = 1

    sent_from = "Stammbib-Update"
    to = ['max.mustermann@gmail.com', 'anna.musterfrau@gmail.com'] #add recipients
    subject = 'Neue Reservierungen verfuegbar'
    body = 'Hey du!\n\n    Es sind neue Termine in der Stammbib frei geworden:'
    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s\n
    Freie Termine: %i\n
    Klicke hier, um einen Platz zu reservieren:
    %s\n
    Dein Robohelfer Robert
    """ % (sent_from, ", ".join(to), subject, body, stammbib, url)
    message = 'Subject: {}\n\n{}'.format(subject, email_text)

    global sentemail
    sentemail = 0
    if sendemail:
        try:
            server_ssl = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server_ssl.ehlo()
            server_ssl.login('max.mustermann@gmail.com', 'passwort') #exchange for your username and password
            server_ssl.sendmail(sent_from, to, message)
            server_ssl.close()
            print("E-Mail gesendet!")
            sentemail = 1
        except:
            print("Etwas ist beim Versenden der E-Mail schief gelaufen!")
    else:
        print("Keine freien Reservierungen. Nächster Versuch in 60 Sekunden...")

if firstRunBool:
    firstRunBool = 0
    for i in range(1, 300):
        asleep = 60
        crawl()
        stunden = 0
        if i / 60 > 1:
            stunden = i / 60 - (i % 60) * 1 / 60
        minuten = i % 60
        print(str(i) + " Mal in " + str(stunden) + " Stunden und " + str(minuten) + " Minuten gecrawlt.")
        print("")
        if sentemail:
            asleep = 300
        time.sleep(asleep)
    print(i/60 + " Stunden lang gecrawlt. Programm wird beendet.")
