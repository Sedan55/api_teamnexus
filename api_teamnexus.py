import requests
import json
import logging
import configparser
import pathlib

path = str(pathlib.Path(__file__).parent.absolute())
config = configparser.ConfigParser()
config.read(path + '/config.ini')

TOKEN_API = config.get('TOKEN', 'TokenApi')
USER = config.get('TOKEN', 'User')
PASSWORD = config.get('TOKEN', 'Password')

blacklist = "https://api.amz-review.com/?username=" + USER + "&password=" + PASSWORD + "&action=checkblacklist"
book = "https://teamnexus.it/api/booking.php?token=" + TOKEN_API
asin = "https://teamnexus.it/api/getasinbycode.php?token=" + TOKEN_API
order = "https://teamnexus.it/api/insertorder.php?token=" + TOKEN_API
review = "https://teamnexus.it/api/insertreview.php?token=" + TOKEN_API
refund = "https://teamnexus.it/api/checkrimborso.php?token=" + TOKEN_API
del_book = "https://teamnexus.it/api/deletebooking.php?token=" + TOKEN_API
products = "https://teamnexus.it/api/getproducts.php?token=" +TOKEN_API
screen = "https://teamnexus.it/api/uploadscreen.php?token=" +TOKEN_API

logger = logging.getLogger(__name__)

def getProducts(nazione = "IT", filtro = "ALL"):

    data = {'nazione': nazione,
            'filtro': filtro}

    resp = requests.post(products, data)

    if resp.status_code != 200:
        msg = "API - Errore getProducts: " + str(resp.status_code)
        logging.error(msg)

    else:
        msg = "API - getProducts: " + str(resp.text)
        logging.info(msg)
        return resp.text

def checkblacklist(value):
    #0 blacklist, 1 no blacklist

    data = {'search': value}

    resp = requests.post(blacklist, data)
    if resp.status_code != 200:

        msg = "API - Errore checkblacklist: " + str(resp.status_code)
        logging.error(msg)

    else:
        msg = "API - Blacklist Team Nexus: " + str(resp.text)
        logging.info(msg)
        return resp.text

def getAsin(codice):

    #data = {'codice': codice}
    
    #resp = requests.post(asin, data["codice"] )
    resp = requests.post(asin+"&codice="+codice)

    if resp.status_code != 200:

        msg = "API - Errore getAsin: " + str(resp.status_code)
        logging.error(msg)

    elif resp.text:

        #print("Resp: " + resp.text)
        return resp.text

    else:
        return 0

def booking(codice, nazione = "IT"):
    
    asin = getAsin(codice)

    data = {'asin': asin,
            'nazione': nazione,
            'codice': codice}

    #cod not found
    if asin == 0:

        msg = "API - Booking - Codice non trovato"
        logging.info(msg)
        return -3

    else:

        resp = requests.post(book, data)
        data = resp.json()
        #print(data)

        #server error
        if resp.status_code != 200:

            msg = "API - Errore: " + str(resp.status_code)
            logging.error(msg)
            return -1

        #finished product
        elif data["success"] == False:

            msg = "API - Booking - Prodotto esaurito controlla il catalogo"
            logging.info(msg)
            return -2

        else:
            msg = "API - Booking - Prodotto prenotato correttamente"
            logging.info(msg)
            return data

def del_booking(id):

    data = {'id': id}

    resp = requests.post(del_book, data)
    resp1 = resp.json()

    if resp.status_code != 200:
    
        msg = "API - del_booking - Errore: " + str(resp.status_code)
        logging.error(msg)
        return -1
    else:
        return resp1

def insertorder(id, cliente, ordine, profilo, paypal):

    data = {'id': id,
                'cliente': cliente,
                'ordine' : ordine,
                'profilo': profilo,
                'paypal': paypal 
            }

    resp = requests.post(order, data)
    resp1 = resp.json()

    if resp.status_code != 200:
        
        msg = "API - insertorder - Errore: " + str(resp.status_code)
        logging.error(msg)
        return -1
    
    elif resp1["success"] == True:

        msg = "API - insertorder - resp: " + str(resp1["success"])
        logging.info(msg)
        return resp1

    elif resp1["success"] == False:
        
        msg = "API - insertorder - resp: " + str(resp1["error"])
        logging.info(msg)
        #print("resp: " + resp[0])
        return resp1

def insertScreen(asin, ordine, url):
    
    data = {'asin': asin,
            'ordine': ordine,
            'url': url}

    resp = requests.post(screen, data)

    if resp.status_code != 200:
        msg = "API - Errore insertScreen: " + str(resp.status_code)
        logging.error(msg)

    else:
        msg = "API - insertScreen: " + str(resp.text)
        logging.info(msg)
        return resp.text

def insertrev(asin, ordine, recensione):
    
    data = {'asin': asin,
                'ordine': ordine,
                'review' : recensione
            }

    resp = requests.post(review, data)
    #print(resp)
    resp1 = resp.json()

    if resp.status_code != 200:
        msg = "API - insertrev - Errore: " + str(resp.status_code)
        logging.error(msg)
        return -1
    
    elif resp1["success"] == True:
        #print("resp: " + str(resp1["success"]))
        return resp1

    elif resp1["success"] == False:
        msg = "API - insertrev: " + str(resp1["error"])
        logging.info(msg)
        return resp1

def checkrefund(asin, ordine, nazione = "IT"):
    
    data = {'asin': asin,
                'nazione': nazione,
                'ordine' : ordine
            }

    resp = requests.post(refund, data)
    resp1 = resp.json()
    print(resp1)

    if resp.status_code != 200:

        msg = "API - checkrefund - Errore: " + str(resp.status_code)
        logging.error(msg)
        return -1

    elif resp1["rimborso"]:

        return resp1
    
    else:
        return -2
        

    return resp