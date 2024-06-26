import requests
import json

def get_genomes() -> dict:
    url = "https://api.genome.ucsc.edu/list/ucscGenomes"
    
    return json.loads(requests.get(url).content)['ucscGenomes']
