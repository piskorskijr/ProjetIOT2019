import twitter 
import math 
import grovepi 
from grove_rgb_lcd import * 
from grovepi import * 
import time 
import datetime 
import MySQLdb 
from pyfingerprint.pyfingerprint import PyFingerprint
#from datetime import datetime
import random
from time import sleep

# Connect to Twitter
api = twitter.Api(
    consumer_key='5LWAJXQ9k2hMslO67JPsfae7t',
    consumer_secret='fhjp8ZKumuz78AeUKvt3lFNm2XS9CqnA1D9LLQwn2Yd8xyYaCk',
    access_token_key='1199592481211527168-vlJ0UWH7bg1EWfYSbn60tLgUD7oy7P',
    access_token_secret='GL9WbFClNFQ4eyw5E1oqrfFrNUXNOoIKPGqG2bCtF0WoJ'
    )


#Connections
sensor = 4
blue = 0
air_sensor = 0
ledvert=2
lumiere=7
ledrouge=3
pinMode(lumiere,"OUTPUT")
pinMode(ledvert,"OUTPUT")
pinMode(ledrouge,"OUTPUT")
time.sleep(1)
setRGB(255,255,255)
grovepi.pinMode(air_sensor,"INPUT")
display = 5
grovepi.pinMode(display,"OUTPUT")
ledbar = 6
grovepi.pinMode(ledbar,"OUTPUT")
time.sleep(1)
i = 0
db = MySQLdb.connect(host="10.34.1.75", user="h19718", passwd="", db="h19718")
curs= db.cursor()
X=True
print("En attente d empreinte")
def main():
   timer = -1
    #Calcul nombre de lignes dans la table log
   while(True):
        try:
# orientation: (0 = red to green, 1 = green to red)
            grovepi.ledBar_init(ledbar, 0)
            time.sleep(.5)
            grovepi.fourDigit_init(display)
            time.sleep(.5)
            sensor_value = grovepi.analogRead(air_sensor)
            val = str(sensor_value)
            horloge= datetime.datetime.now().strftime("%H:%M:%S")
            print ("Qualite de l air : " + val)
            time.sleep(1)
            [temp,humidity] = grovepi.dht(sensor,blue)
            if math.isnan(temp) == False and math.isnan(humidity) == False:
                timer = timer+1 
                print ("timer" + str(timer)) 
                print("temp = %.02f C humidity =%.02f%%"%(temp,humidity))
                setText("Temp : " + str(temp) + "     Hum : " + str(humidity)+"%")
                if (timer%12==0):
                        print("La temperature de la piece a  " +str(horloge) + " est de : " + str(temp) + "  C")
                        api.PostUpdate("La temperature de la piece a " +str(horloge) + " est de : " + str(temp) + "  C")                
                else:
                        pass
            if sensor_value > 130:
                setText("Temp : " + str(temp) + "     Hum : " + str(humidity)+"%")
                setRGB(247,35,12)
                digitalWrite(ledvert,0)
                digitalWrite(ledrouge,1)
                time.sleep(.5)
                digitalWrite(ledrouge,0)
                grovepi.ledBar_setLevel(ledbar, 2)
                time.sleep(.5)
            elif sensor_value > 70:
                setText("Temp : " + str(temp) + "     Hum : " + str(humidity)+"%")
                setRGB(255,215,0)
                digitalWrite(ledvert,0)
                digitalWrite(ledrouge,1)
                time.sleep(2)
                digitalWrite(ledrouge,0)
                grovepi.ledBar_setLevel(ledbar, 5)
                time.sleep(.5)
            else: 
                setText("Temp : " + str(temp) + "     Hum : " + str(humidity)+"%")
                setRGB(15,157,232)
                digitalWrite(ledrouge,0)
                digitalWrite(ledvert,1)
                time.sleep(1)
                grovepi.ledBar_setLevel(ledbar, 11)
                time.sleep(.5)
            curs.execute("SELECT COUNT(*) FROM log2")
            lignes=curs.fetchone()
            nblignes=lignes[0]
            compteur = nblignes
            print("Il y a " +  str(compteur) + " personnes " )
            leading_zero = 0
            grovepi.fourDigit_number(display,compteur,leading_zero)
            time.sleep(.5)
            if (compteur !=0):
                digitalWrite(lumiere,1)
            else:
                digitalWrite(lumiere,0)

            f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

            if ( f.verifyPassword() == False ):
                raise ValueError('The given fingerprint sensor password is wrong!')
        except Exception as e:
            print('The fingerprint sensor could not be initialized!')
            print('Exception message: ' + str(e))

    #while ( f.readImage() == False ):
     #       pass
        try:
            key= f.readImage()
            today= datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            rdy = datetime.datetime.now().strftime("%b %d %Y")
            #str(today)
            clock= datetime.datetime.now().strftime("%H:%M:%S")
            if (key == False):
                pass
            if (key != False):
                curs.execute("SELECT COUNT(*) FROM log2")
                lignes=curs.fetchone()
                nblignes=lignes[0]
                print(nblignes)
    ## Converts read image to characteristics and stores it in charbuffer 1
                f.convertImage(0x01)
    ## Searchs template
                result = f.searchTemplate()

                positionNumber = result[0]
                curs.execute("SELECT statut FROM user WHERE id_finger= ('%s')" %positionNumber)
                statut = curs.fetchone()
                stat=statut[0]
                print("Vous etes un : " + str(stat))
                salle ="T229"
                if (stat == "PROF"):
                        today= datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        str(today)
                        print(today)
                        curs.execute("SELECT nomP FROM prof  WHERE id_finger = ('%s')" %positionNumber)
                        nomP= curs.fetchone()
                        nomtemp = nomP[0]
                        print( nomtemp)
                        curs.execute("SELECT numP FROM prof  WHERE id_finger = ('%s')" %positionNumber)
                        numP= curs.fetchone()
                        numtemp = numP[0]
                        print( numtemp)
                        sql=("SELECT COUNT(*) FROM log2  WHERE(nom='%s')" %(nomtemp))
                        curs.execute(sql)
                        nboccu=curs.fetchone()
                        noccu=nboccu[0]
                        if (noccu==0):
                                curs.execute("INSERT INTO log2 (nom, date, salle, num, statut) VALUES ('%s', '%s', '%s','%s','%s')" %(nomtemp, today, salle, numtemp, stat))
                                db.commit()
                        else:
                                curs.execute("DELETE FROM log2  WHERE num = ('%s')" %numtemp)
                                db.commit()
                else:
                        today= datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        str(today)
                        print(today)
                        curs.execute("SELECT nomE FROM eleve  WHERE id_finger = ('%s')" %positionNumber)
                        nomE= curs.fetchone()
                        nomtemp = nomE[0]
                        print( numtemp)

                        sql=("SELECT COUNT(*) FROM log2  WHERE(nom='%s')" %(nomtemp))
                        curs.execute(sql)
                        nboccu=curs.fetchone()
                        noccu=nboccu[0]
                        if (noccu==0):
                                curs.execute("INSERT INTO log2 (nom, date, salle, num, statut) VALUES ('%s', '%s', '%s','%s','%s')" %(nomtemp, today, salle, numtemp, stat))
                                db.commit()
                        else:
                                curs.execute("DELETE FROM log2  WHERE num = ('%s')" %numtemp)
                                db.commit()
        except KeyboardInterrupt:
                digitalWrite(lumiere,0)
                digitalWrite(ledrouge,0)
                digitalWrite(lumiere,0)
                digitalWrite(ledvert,0)
                quit(1)

        except Exception as e:
            print("Empreinte non reconnue , reesayez")
            print("Duplicate Tweet or Twitter Refusal: {}".format(e))
if __name__ == '__main__':
    while(X==True):
        try:
                main()
        except KeyboardInterrupt:
                digitalWrite(ledrouge,0)
                setText("")
                setRGB(255,255,255)
                grovepi.ledBar_setBits(ledbar, 0)
                 grovepi.fourDigit_off(display)
                digitalWrite(lumiere,0)
                digitalWrite(ledvert,0)
                X=False
                quit(1)
        finally:
                print("Fin du prog")
        time.sleep(1)





























