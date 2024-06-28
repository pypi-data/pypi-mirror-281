''' Collection of uniprot entries
customary cache location is "/Users/guillaumelaunay/work/data/uniprot"
'''
import pyproteins.container.customCollection
from os.path import expanduser
import gzip
from xml.etree.ElementTree import parse#, dump, fromstring, register_namespace, ElementTree, tostring
from .entry import Entry
from .utils import isValidID, strip

class EntrySet(pyproteins.container.customCollection.EntrySet):

    def __init__(self, **kwargs):
        self.ns = '{http://uniprot.org/uniprot}'

        home = expanduser("~")
        cachePath = home     
        self.isXMLCollection = False
        self.isRedisCollection = False

        if 'streamXML' or 'collectionXML' in kwargs:
            self.isXMLCollection = True
            if 'streamXML' in kwargs:
                self.etree = parse(kwargs['streamXML'])
            elif 'collectionXML' in kwargs:
                if kwargs['collectionXML'].endswith('.gz'):
                    with gzip.open(kwargs['collectionXML'], 'r') as gz:
                        self.etree = parse(gz)
                else:
                    self.etree = parse(kwargs['collectionXML'])


            self.etree_root = self.etree.getroot()
            self.index = None
          #  print(f"==> {type(self.etree_root)} {type(self.etree)} <==")

        super().__init__(collectionPath=cachePath, constructor=Entry, typeCheck=isValidID, indexer=strip)
        if 'collectionXML' in kwargs:
            print (f"Acknowledged {len(self)} entries {kwargs['collectionXML']}")
      
    def __len__(self):
        if self.isXMLCollection:
            return len(list([ _ for _ in self ]))
        return super().__len__()

    def keys(self):
        """ Returns uniprot identifiers within collection as a generator """
        if self.isXMLCollection:
            for entry in self.etree_root.findall(f"{self.ns}entry"):
                for alt_acc in entry.findall(f"{self.ns}accession"):
                    yield(alt_acc.text)
        else :
            return super().keys()
    
    def has(self, id):
        if self.isXMLCollection:
            if self.index is None:
                self.index = {}
                for acc in self.keys():
                    self.index[acc] = True
            return id in self.index
        else :
            return super().has()

    def __iter__(self):
        if self.isXMLCollection:
            for entry in self.etree_root.findall(f"{self.ns}entry"):
                uniprotID = entry.find(f"{self.ns}accession").text
                yield Entry(uniprotID, xmlEtreeHandler = entry, xmlNS = self.ns)

    def get(self, uniprotID):
        if self.isXMLCollection:
            for entry in self.etree_root.findall(f"{self.ns}entry"):
                for acc in entry.findall(f"{self.ns}accession"):
                    if acc.text == uniprotID: # entry is the node matching provided UNIPROT accessor
                        return Entry(uniprotID, xmlEtreeHandler = entry, xmlNS = self.ns)
            return None
        else :
            print(f"Looking in XML files/dir collection for {uniprotID}")
            return super().get(uniprotID, xmlNS = self.ns)
        
        
    def serialize(self, ext=''):
        global PfamCache
        print ("serializing uniprot collection")
        super().serialize(ext=ext)
        if PfamCache:
            print ("serializing pfam collection")
            getPfamCollection().serialize(ext=ext)
    
    @property
    def taxids(self):
        taxids = set()
        for e in self:
            taxids.add(e.taxid)
        return list(taxids)
