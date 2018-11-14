import requests

r = requests.get('http://transport.opendata.ch/v1/connections?from=Diesbach-Betschwanden&to=Schwanden GL&fields[]=connections/from/departure&fields[]=connections/to/arrival')

print(r.text)