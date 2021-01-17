import unittest
import sys
from pathlib import Path
import json
sys.path.insert(0, str(Path(__file__).parent.parent) + '/module/')

import api_teamnexus as api

class TestApiTeamnexus(unittest.TestCase):

    def test_getProdotti(self):
        self.assertEquals(type(api.getProdotti()), str)

    def test_checkBlacklist(self):
        self.assertFalse(api.checkBlacklist("pincopallino@gmail.com"), "Utente in blacklist")
        self.assertTrue(api.checkBlacklist("reviewer.amzn.it@gmail.com"), "Utente non in blacklist")
        
    def test_getAsin(self):
        self.assertEquals(api.getAsin("F1-ZZ005"), "XXXXXXXXXX")
        
    def test_booking(self):
        prenotazione = api.booking("F1-ZZ005")
        
        if prenotazione == -1:
            self.assertEquals(prenotazione, -1)
        elif prenotazione == -2:
            self.assertEquals(prenotazione, -2)
        elif prenotazione == -3:
            self.assertEquals(prenotazione, -3)
        else:
            self.assertEquals(type(prenotazione), dict)
            
    def test_checkRimborso(self):
        resp = api.checkRimborso("B08NG6KT7V", "405-5865801-6007503")
        
        if resp == -1:
            self.assertEquals(resp, -1)
        elif resp == -2:
            self.assertEquals(resp, -2)
        else:
            self.assertEquals(type(resp), dict)

if __name__ == '__main__':
    unittest.main()