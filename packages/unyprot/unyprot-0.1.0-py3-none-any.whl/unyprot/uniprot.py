## remains of uniprot entry isolation

from urllib.request import urlopen
import re
import pyproteins.container.customCollection
import pyproteins.container.Core
#import pyproteinsext.pfam as pfam
import json

import gzip

from xml.etree.ElementTree import parse, dump, fromstring, register_namespace, ElementTree, tostring


from os.path import expanduser

#PfamEntrySet = None
#uniprotEntrySet = None

#PfamCache = None

from json import JSONEncoder

#import pyproteins.utils.make_json_serializable

## Returns a list of all keyword in collection, along with the list of uniprotObj featuring them
def keyWordChart(uniprotObjIter, kwType='GO'):
    def kwMapper(obj, _type) :
        if _type == 'GO':
            return obj.GO
        raise TypeError("implement other KW plz")

    kwChart = {}
    for uniprotObj in uniprotObjIter:
        for kwObj in  kwMapper(uniprotObj, kwType):
            if kwObj not in kwChart:
                kwChart[kwObj] = []
            kwChart[kwObj].append(uniprotObj)

    return sorted([ (k,v) for k,v in kwChart.items() ], key=lambda x : len(x[1]), reverse=True)

# Give link to uniprot Collection to allow proxy settings
# and cache setting for it and pfam
def getUniprotCollection ():
    global uniprotEntrySet
    if not uniprotEntrySet:
        uniprotEntrySet = EntrySet()

    return uniprotEntrySet

#def setCache(location):
#    print location
#    uniprotEntrySet.setCache(location=location)

#def proxySetting(**kwargs):
#    proxySetting(**kwargs)

def getPfamCollection ():
    global PfamEntrySet
    if not PfamEntrySet:
        home = expanduser("~")
        PfamCacheDefault = home
        PfamEntrySet = pfam.EntrySet(PfamCacheDefault)

    return PfamEntrySet

def proxySetting(**param):
    pyproteins.container.Core.proxySetting(param)

'''
    TODO Isoform, minimal -> affects the fasta sequence
                 Need to check isoform data xml structure, sequence variant specs of Uniprot
'''

def capture(string):
    subString = re.search("[OPQ][0-9][A-Z0-9]{3}[0-9]|[A-NR-Z][0-9]([A-Z][A-Z0-9]{2}[0-9]){1,2}", string)
    if subString:
        return subString.group()

    return None



class fetchEntries():
    def __init__(self, list):
        self.list = list
        self.entrySet = [Entry(id = id) for id in self.list]
    def __iter__(self):
        for entry in self.entrySet:
            yield entry



# Custom encoder for uniprot entity
class EntryEncoder(json.JSONEncoder):
    def default(self, entryObj):
        if isinstance(entryObj, pyproteins.container.Core.Container):
            container = {}
            for k, v in entryObj.__dict__.items():
                if k == 'name':
                    container[k] = v
                if k == 'GO':
                    container[k] = [ go.__dict__ for go in v ]
                if k == 'id':
                    container[k] = v
                if k == 'geneName':
                    container[k] = v
                if k == 'fullName':
                    container[k] = v
            return container
        # Error
        return json.JSONEncoder.default(self, entryObj)

