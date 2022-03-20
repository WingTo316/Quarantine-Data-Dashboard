import requests
import urllib.parse
import datetime
"""
usage: Reader.getDataAvailability()
     / Reader.getData(datetime.date)
"""
class Reader():
    apiEndPt = 'https://api.data.gov.hk/v2/filter?'
    total_occupancy = []
    centre_occupancy = []

    @classmethod
    def _getAllOccupancy(cls, date):
        params = {
            'q': {
                "resource": "http://www.chp.gov.hk/files/misc/no_of_confines_by_types_in_quarantine_centres_eng.csv",
                "section": 1,
                "format": "json",
                "filters": [ [1, "eq", [f'{date.day:02}/{date.month:02}/{date.year:04}']] ]
            }
        }
        query = urllib.parse.urlencode(params, quote_via=urllib.parse.quote).replace('%27','%22')
        cls.total_occupancy = requests.get(cls.apiEndPt+query).json()

    @classmethod
    def _getOccupancyByCentre(cls, date):
        params = {
            'q': {
                "resource": "http://www.chp.gov.hk/files/misc/occupancy_of_quarantine_centres_eng.csv",
                "section": 1,
                "format": "json",
                "filters": [ [1, "eq", [f'{date.day:02}/{date.month:02}/{date.year:04}']] ],
                "sorts": [ [8, "desc"] ]
            }
        }
        query = urllib.parse.urlencode(params, quote_via=urllib.parse.quote).replace('%27','%22')
        cls.centre_occupancy = requests.get(cls.apiEndPt+query).json()

    @classmethod
    def getPersonInUse(cls):
        sum = 0
        for centre in cls.centre_occupancy:
            sum += centre['Current person in use']
        return sum
    
    @classmethod
    def getUnitInUse(cls):
        sum = 0
        for centre in cls.centre_occupancy:
            sum += centre['Current unit in use']
        return sum
    
    @classmethod
    def getUnitAvailable(cls):
        sum = 0
        for centre in cls.centre_occupancy:
            sum += centre['Ready to be used (unit)']
        return sum
    
    @classmethod
    def getTop3Available(cls):
        top = [
            {
            "name": centre['Quarantine centres'],
            "units": centre['Ready to be used (unit)']
            } for centre in cls.centre_occupancy[0:3]
        ]
        return top

    @classmethod
    def getCloseContact(cls):
        for sth in cls.total_occupancy:
            return sth['Current number of close contacts of confirmed cases']
        return 0
    
    @classmethod
    def getNonCloseContact(cls):
        for sth in cls.total_occupancy:
            return sth['Current number of non-close contacts']
        return 0
    
    @classmethod
    def checkConsistency(cls):
        if cls.getPersonInUse() == (cls.getCloseContact() + cls.getNonCloseContact()):
            return True
        return False

    @classmethod
    def getDataAvailability(self):

        date = datetime.date.today()
        for _ in range(7):

            try:
                self.getData(date)
            except:
                return False, True, date

            if len(self.total_occupancy) != 0 and len(self.centre_occupancy) != 0:
                return True, True, date

            date -= datetime.timedelta(days=1)

        return True, False, date

    @classmethod
    def getData(cls, date):
        cls._getAllOccupancy(date)
        cls._getOccupancyByCentre(date)