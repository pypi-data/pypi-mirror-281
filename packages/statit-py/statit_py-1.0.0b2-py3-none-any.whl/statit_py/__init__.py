import requests
from urllib.parse import urljoin

ENDPOINT = 'https://api.gostatit.com'

class coreAPI:
  '''A python API to interact with the api.gostatit.com core web API'''
  
  def __init__(self, username: str, apikey: str):
    self.username = username
    self.apikey = apikey

  def post(self, action: str, inputDict: dict):
    url = urljoin(ENDPOINT, 'core')
    json = {'action': action, 'input': inputDict}
    r = requests.post(url, auth=(self.username, self.apikey), json=json)
    if r.status_code != 200:
      raise ValueError(r.text)
    return r.json()


  def getSerie(self, ID: str) -> dict:
    return self.post('getSerie', {'id': ID})

  def listSeries(self, ID: str) -> list[dict]:
    return self.post('listSeries', {'id': ID})

  def deleteSerie(self, ID: str):
    return self.post('deleteSerie', {'id': ID})


  def getSerieJSON(self, inputDict: dict) -> dict:
    return self.post('getSerie', inputDict)

  def batchGetSerieJSON(self, inputDict: dict):
    return self.post('batchGetSerie', inputDict)

  def listSeriesJSON(self, inputDict: dict) -> list[dict]:
    return self.post('listSeries', inputDict)

  def putSerieJSON(self, inputDict: dict):
    return self.post('putSerie', inputDict)

  def batchPutSerieJSON(self, inputDict: list[dict]):
    return self.post('batchPutSerie', inputDict)

  def updateSerieJSON(self, inputDict: dict):
    return self.post('updateSerie', inputDict)

  def deleteSerieJSON(self, inputDict: dict):
    return self.post('deleteSerie', inputDict)

  def batchDeleteSerieJSON(self, inputDict: list[dict]):
    return self.post('batchDeleteSerie', inputDict)



class functionsAPI:
  '''A python API to interact with the api.gostatit.com functions web API'''

  def __init__(self, username: str, apikey: str):
    self.username = username
    self.apikey = apikey

  def post(self, action: str, inputDict: dict):
    url = urljoin(ENDPOINT, 'functions')
    json = {'action': action, 'input': inputDict}
    r = requests.post(url, auth=(self.username, self.apikey), json=json)
    if r.status_code != 200:
      raise ValueError(r.text)
    return r.json()


  def getValue(self, ID: str, endDate=None):
    inputDict = {'id': ID}
    if endDate is not None:
      inputDict['endDate'] = endDate
    return self.post('getValue', inputDict)

  def getValueSum(self, ID: str, endDate=None, periods=None):
    inputDict = {'id': ID}
    if endDate is not None:
      inputDict['endDate'] = endDate
    if periods is not None:
      inputDict['periods'] = periods
    return self.post('getValueSum', inputDict)

  def getValueAverage(self, ID: str, endDate=None, periods=None):
    inputDict = {'id': ID}
    if endDate is not None:
      inputDict['endDate'] = endDate
    if periods is not None:
      inputDict['periods'] = periods
    return self.post('getValueAverage', inputDict)

  def getValueChange(self, ID: str, endDate=None, periods=None):
    inputDict = {'id': ID}
    if endDate is not None:
      inputDict['endDate'] = endDate
    if periods is not None:
      inputDict['periods'] = periods
    return self.post('getValueChange', inputDict)

  def getValueChangePercent(self, ID: str, endDate=None, periods=None):
    inputDict = {'id': ID}
    if endDate is not None:
      inputDict['endDate'] = endDate
    if periods is not None:
      inputDict['periods'] = periods
    return self.post('getValueChangePercent', inputDict)

  def getValueDate(self, ID: str, endDate=None):
    inputDict = {'id': ID}
    if endDate is not None:
      inputDict['endDate'] = endDate
    return self.post('getValueDate', inputDict)

  def getObs(self, ID: str, endDate=None):
    inputDict = {'id': ID}
    if endDate is not None:
      inputDict['endDate'] = endDate
    return self.post('getObs', inputDict)

  def getObsSum(self, ID: str, endDate=None, periods=None):
    inputDict = {'id': ID}
    if endDate is not None:
      inputDict['endDate'] = endDate
    if periods is not None:
      inputDict['periods'] = periods
    return self.post('getObsSum', inputDict)

  def getObsAverage(self, ID: str, endDate=None, periods=None):
    inputDict = {'id': ID}
    if endDate is not None:
      inputDict['endDate'] = endDate
    if periods is not None:
      inputDict['periods'] = periods
    return self.post('getObsAverage', inputDict)

  def getObsChange(self, ID: str, endDate=None, periods=None):
    inputDict = {'id': ID}
    if endDate is not None:
      inputDict['endDate'] = endDate
    if periods is not None:
      inputDict['periods'] = periods
    return self.post('getObsChange', inputDict)

  def getObsChangePercent(self, ID: str, endDate=None, periods=None):
    inputDict = {'id': ID}
    if endDate is not None:
      inputDict['endDate'] = endDate
    if periods is not None:
      inputDict['periods'] = periods
    return self.post('getObsChangePercent', inputDict)

  def getSerie(self, ID: str, startDate=None, endDate=None):
    inputDict = {'id': ID}
    if startDate is not None:
      inputDict['startDate'] = startDate
    if endDate is not None:
      inputDict['endDate'] = endDate
    return self.post('getSerie', inputDict)

  def getSerieSum(self, ID: str, startDate=None, endDate=None, periods=None):
    inputDict = {'id': ID}
    if startDate is not None:
      inputDict['startDate'] = startDate
    if endDate is not None:
      inputDict['endDate'] = endDate
    if periods is not None:
      inputDict['periods'] = periods
    return self.post('getSerieSum', inputDict)

  def getSerieAverage(self, ID: str, startDate=None, endDate=None, periods=None):
    inputDict = {'id': ID}
    if startDate is not None:
      inputDict['startDate'] = startDate
    if endDate is not None:
      inputDict['endDate'] = endDate
    if periods is not None:
      inputDict['periods'] = periods
    return self.post('getSerieAverage', inputDict)

  def getSerieChange(self, ID: str, startDate=None, endDate=None, periods=None):
    inputDict = {'id': ID}
    if startDate is not None:
      inputDict['startDate'] = startDate
    if endDate is not None:
      inputDict['endDate'] = endDate
    if periods is not None:
      inputDict['periods'] = periods
    return self.post('getSerieChange', inputDict)

  def getSerieChangePercent(self, ID: str, startDate=None, endDate=None, periods=None):
    inputDict = {'id': ID}
    if startDate is not None:
      inputDict['startDate'] = startDate
    if endDate is not None:
      inputDict['endDate'] = endDate
    if periods is not None:
      inputDict['periods'] = periods
    return self.post('getSerieChangePercent', inputDict)

  
