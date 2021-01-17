import requests
import json
import logging
from endpoint import Endpoint

logger = logging.getLogger(__name__)

def getProdotti(nazione = "IT", filtro = "ALL"):
    data = {'nazione': nazione,
            'filtro': filtro}

    resp = requests.post(Endpoint.GET_PRODUCTS, data)

    if resp.status_code != 200:
        msg = "Errore: " + str(resp.status_code)
        logging.error(msg)
        return -1
    else:
        msg = "Errore: " + str(resp.text)
        logging.info(msg)
        return resp.text


def checkBlacklist(value):
    #0 blacklist, 1 no blacklist
    data = {'search': value}
    resp = requests.post(Endpoint.CHECK_BLACKLIST, data)
    
    if resp.status_code != 200:
        msg = "Errore: " + str(resp.status_code)
        logging.error(msg)
        return -1
    else:
        if resp.text == "1":
            return False
        elif resp.text == "0":
            return True
        else:
            return -1


def getAsin(codice):
    #data = {'codice': codice}

    resp = requests.post(Endpoint.GET_ASIN_BY_CODE+"&codice={}".format(codice))

    if resp.status_code != 200:
        msg = "Errore: " + str(resp.status_code)
        logging.error(msg)
        return -1
    elif resp.text:
        #print("Resp: " + resp.text)
        return resp.text
    else:
        return -1


def booking(codice, nazione = "IT"):
    asin = getAsin(codice)
    data = {'asin': asin,
            'nazione': nazione,
            'codice': codice}
    
    #Codice non trovato
    if asin == 0:
        msg = "Codice non trovato"
        logging.info(msg)
        return -3

    else:
        resp = requests.post(Endpoint.BOOKING, data)
        data = resp.json()

        #server error
        if resp.status_code != 200:
            msg = "Errore server: " + str(resp.status_code)
            logging.error(msg)
            return -1

        #finished product
        elif data["success"] == False:
            msg = "Prodotto esaurito o non disponibile"
            logging.info(msg)
            return -2

        elif data["success"] == True:
            msg = "Prodotto prenotato correttamente"
            logging.info(msg)
            return data


def deleteBooking(id):
    data = {'id': id}

    resp = requests.post(Endpoint.DELETE_BOOKING, data)
    resp1 = resp.json()

    if resp.status_code != 200:
        msg = "Errore: " + str(resp.status_code)
        logging.error(msg)
        return -1
    else:
        return resp1


def insertOrder(id, cliente, ordine, profilo, paypal):
    data = {'id': id,
                'cliente': cliente,
                'ordine' : ordine,
                'profilo': profilo,
                'paypal': paypal 
            }
    
    resp = requests.post(Endpoint.INSERT_ORDER, data)
    resp1 = resp.json()

    if resp.status_code != 200:
        msg = "Errore: " + str(resp.status_code)
        logging.error(msg)
        return -1
    
    elif resp1["success"] == True:
        msg = "Response: " + str(resp1["success"])
        logging.info(msg)
        return resp1

    elif resp1["success"] == False:
        msg = "Response: " + str(resp1["error"])
        logging.info(msg)
        #print("resp: " + resp[0])
        return resp1


def insertScreen(asin, ordine, url):
    data = {'asin': asin,
            'ordine': ordine,
            'url': url}

    resp = requests.post(Endpoint.UPLOAD_SCREEN, data)

    if resp.status_code != 200:
        msg = "Errore: " + str(resp.status_code)
        logging.error(msg)
        return -1
    else:
        msg = str(resp.text)
        logging.info(msg)
        return resp.text


def insertRecensione(asin, ordine, recensione):
    data = {'asin': asin,
                'ordine': ordine,
                'review' : recensione
            }
    
    resp = requests.post(Endpoint.INSERT_REVIEW, data)
    resp1 = resp.json()

    if resp.status_code != 200:
        msg = "Errore: " + str(resp.status_code)
        logging.error(msg)
        return -1
    
    elif resp1["success"] == True:
        #print("resp: " + str(resp1["success"]))
        return resp1

    elif resp1["success"] == False:
        msg = str(resp1["error"])
        logging.info(msg)
        return resp1


def checkRimborso(asin, ordine, nazione = "IT"):
    data = {'asin': asin,
                'nazione': nazione,
                'ordine' : ordine
            }
    
    resp = requests.post(Endpoint.CHECK_REFUND, data)
    resp1 = resp.json()

    if resp.status_code != 200:
        msg = "Errore: " + str(resp.status_code)
        logging.error(msg)
        return -1

    elif resp1["rimborso"]:
        return resp1
    
    else:
        return -2

    return resp    