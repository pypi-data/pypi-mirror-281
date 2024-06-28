import pyproteins.container.Core

from .miscellaneous import *
class Entry(pyproteins.container.Core.Container):
    ## Wrap and split kwargs
    # Re-encode etree xpath like search 
    # https://docs.python.org/3/library/xml.etree.elementtree.html#example
    # //div[@id='..' and @class='...]

    def __repr__(self):
        asStr = f"{self.id}:{self.AC}\n" 
        asStr += f"{self.name}:{self.fullName}({self.geneName})\n"
        
        if self.STRING_ID:
            asStr += f"STRING_ID:{self.STRING_ID}\n"
        
        asStr += f"taxid:{self.taxid}:{self.lineage}\n"
        asStr += f"KW:{self.KW}\n"
        asStr += f"GO:{self.GO}\n"
        
        return asStr

    def _buildXpath(self, xpath, **kwargs):
        
        _xpath_ = xpath.replace("/",f"/{self._ns}")
        _xpath_ += ' and '.join( [ f"[@{k}='{v}']" for k,v in kwargs.items() ] )

        if not ( _xpath_.startswith('/') or _xpath_.startswith('./') ) :
            _xpath_ = f"{self._ns}{_xpath_}"

        #print(f"building xpath from {xpath} to {_xpath_}")
        return _xpath_

    def _xmlAttrib(self, key, elem=None):
        if elem is None:
            elem = self.xmlHandler
        return elem.attrib[key]

    def _xmlFind(self, tag, elem=None, **kwargs):
        if elem is None:
            elem = self.xmlHandler
        if len(kwargs.keys()) > 1:
            raise(f"Asking for Too many attributes ({len(kwargs.keys())}) in tag xpath search")

        xpathStr = self._buildXpath(tag, **kwargs) 
        return elem.find(xpathStr)
        
    def _xmlFindAll(self, tag, elem=None, **kwargs):
        if elem is None:
            elem = self.xmlHandler
        
        xpath = self._buildXpath(tag, **kwargs) 
        return elem.findall(xpath)

    def __init__(self, id, baseUrl="http://www.uniprot.org/uniprot/", fetchable= True, fileName=None, xmlEtreeHandler=None, xmlNS=None):
        if not id:
            raise TypeError('identifier is empty')
        
        super().__init__(id, url=baseUrl + str(id) + '.xml', fileName=fileName)
        #pyproteins.container.Core.Container.__init__(self, id, url=baseUrl + str(id) + '.xml', fileName=fileName)
        
        if not xmlNS is None:
            self._ns = xmlNS

        if not xmlEtreeHandler is None:
            self.xmlHandler = xmlEtreeHandler
        else:
            print("Search for", f"{xmlNS}entry")
            self.xmlHandler = self.getXmlHandler(fetchable=fetchable).find(f"{xmlNS}entry")
        
        if self.xmlHandler is None:
            return None
        
        self.name = self._xmlFind("./name").text
        
        if not self._xmlFind("./protein/recommendedName/fullName") is None:
            self.fullName = self._xmlFind("./protein/recommendedName/fullName").text
        else:
            self.fullName = self.name
        
        self.geneName =  None
        e = self._xmlFind("gene")
        if not e is None:
           self.geneName = self._xmlFind("./name", elem=e).text

        self.STRING_ID = None
        e = self._xmlFind("./dbReference", type="STRING")
        if not e is None:
            self.STRING_ID = self._xmlAttrib('id', elem=e)
        
        self.parseAC()
        self.parseLineage()
        self.parseKW()
        self.parseGO()
        self.parseSequence()
        self.parse_subcellular_location()
        # adding dataset
        e = self._xmlFind("./")
        self.dataset =  self._xmlAttrib('dataset', elem=e)

# Following oarsing stages are disabled since we got rid of bs4
# Need to port them  to lxml, making use of xpath syntax
    def PARSER_TO_PORT_TO_ETREE(self):

       
        self.parseSse()
        self.Ensembl = self.parseEnsembl()
        self.GeneID = self.parseGeneID()
        self.parseSequence()
        self.parsePDB()
        self.parseMIM()
        self.parseDI()
        self.parseORPHA()
        self.xref = self.get_xref()
        self.parseInterpro()

    def __hash__(self):
        return hash(self.id)

    def __copy__(self):
        return self

    def __deepcopy__(self, memo):
        return self

    def __eq__ (self, other):
        return self.id == other.id

    def toJSON(self):
        #print ('toJSON')
        #asDict = {}
        #for k in self.__dict__.keys():
        #    if k == 'xmlHandler':
        ##        continue
        #    if k != 'GO':
        #        continue
        #    asDict[str(k)] = getattr(self, k)
        #    print(asDict)

        container = {}
        for k, v in self.__dict__.items():
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
            if k == 'taxid':
                container[k] = v
        return container

    def parseAC(self):
        self.AC = [ e.text for e in  self._xmlFindAll("./accession") ]
          
    def parseLineage(self):
        self.lineage = [ e.text for e in  self._xmlFindAll("./organism/lineage/taxon") ]
        e = self._xmlFind('organism/dbReference', type='NCBI Taxonomy')
        self.taxid = self._xmlAttrib('id', elem=e)
    
    def parseMIM(self):
        self.MIM = []
        for e in self.xmlHandler.find_all("dbReference", type="MIM"):
            if str(e.parent.name) == 'entry':
                self.MIM.append(MimKW(e))

    def parseDI(self):
        self.DI = []
        for e in self.xmlHandler.find_all("disease"):
            self.DI.append(DI(e))

    def parseGO(self):
        self.GO = []
        for e in self._xmlFindAll("dbReference", type="GO"):
            self.GO.append(GoKW(
                self._xmlAttrib('id', elem=e),
                self._xmlAttrib('value', elem = self._xmlFind("property", elem=e, type="term") ),
                self._xmlAttrib('value', elem = self._xmlFind("property", elem=e, type="evidence") )
            ))
        
    def parseORPHA(self):
        self.ORPHA = []
        for e in self.xmlHandler.find_all("dbReference", type="Orphanet"):
            if str(e.parent.name) == 'entry':
                self.ORPHA.append(OrphaKW(e))

    def parsePDB(self):
        self.pdbRef = []
        for e in self.xmlHandler.find_all("dbReference", type="PDB"):
            self.pdbRef.append(PDBref(e))

    def parseDomain(self):
        try:
            self.domains=getPfamCollection().map(uniprotID=self.id)
        except:
            self.domains=[]

        #self.domains = []
        #for e in self.xmlHandler.find_all("feature", type="domain"):
        #    buf = Domain(e, self.id)
        #    if buf.description:
        #        self.domains.append(Domain(e, self.id))
        #for e in self.xmlHandler.find_all("feature", type="repeat"):
        #    buf = Domain(e, self.id)
        #    if buf.description:
        #        self.domains.append(Domain(e, self.id))
        #if not self.domains:
        #    print "No domain data found for " + self.id + ", attempting pfam"
        #    try :
        #        self.domains = getPfamCollection().map(uniprotID=self.id)
        #    except ValueError as msg:
        #        print ("Could not bind uniprot to its pfam ressources reason\n" + str(msg))

    def parseSse(self):
        self.sse = []
        for e in self.xmlHandler.find_all("feature", type="strand"):
            self.sse.append(Sse(e))
        for e in self.xmlHandler.find_all("feature", type="turn"):
            self.sse.append(Sse(e))
        for e in self.xmlHandler.find_all("feature", type="helix"):
            self.sse.append(Sse(e))

    def parseKW(self):
        self.KW = []
        
        for e in self._xmlFindAll("./keyword"):
            self.KW.append( UniprotKW(self._xmlAttrib('id', elem=e), e.text) ) 

    def parseSequence(self):
        self.sequence = self._xmlFind("./sequence").text.replace("\n", "").replace(" ", "")
        #self.sequence = Sequence(self.xmlHandler.find("sequence", {"length" : True}))
    #    pass
    
    def parseEnsembl(self):
        #Search for Ensembl id : ENSGXXXXXXXXXXX
        Ensembl_id = []
        for e in self.xmlHandler.find_all("dbReference", type="Ensembl"):
            for e_gene_id in e.find_all('property',type='gene ID'):
                if e_gene_id["value"] not in Ensembl_id:
                    Ensembl_id.append(e_gene_id["value"])
        return Ensembl_id
        
    def parseGeneID(self):
        GeneID= []
        for e_gene_id in self.xmlHandler.find_all("dbReference", type="GeneID"):
            if e_gene_id["id"] not in GeneID:
                GeneID.append(e_gene_id["id"])
        return GeneID

    def parse_subcellular_location(self):
        self.subcellular_location = []
        for citation in self._xmlFindAll('comment', type="subcellular location"):
            for sl in self._xmlFindAll('subcellularLocation', elem = citation):
                for location in self._xmlFindAll('location', elem = sl):
                    self.subcellular_location.append(location.text)
        # except : 
        #     print("WARNING", self.AC, "subcellular location can't be parsed")
        #     print(citation, sl, location)

        # self.subcellular_location = []
        # citations = self._xmlFindAll("comment", type="subcellular location")
        # for citation in citations:
        #     annotation = self._xmlFind('subcellularLocation/location', elem=citation)
           

        #     # if not annotation:
        #     #     print("no annotation", self.AC, annotation)
        #     # else:
        #     try:
        #         self.subcellular_location.append(annotation.text)
        #     except:
        #         print("WARNING", self.AC, "subcellular location can't be parsed")
        #         self.subcellular_location = ['WARNING']
        
    def get_xref(self):
        # print("GET XREF")
        dic_xref = {'EMBL': {}, 'RefSeq': {}}
        # Search EMBL
        for e in self.xmlHandler.find_all("dbReference", type="EMBL"):
            if str(e.parent.name) == 'entry':
                for e_prot_id in e.find_all('property',type='protein sequence ID'):
                    dic_xref["EMBL"][e["id"]] = e_prot_id["value"]
        # Search RefSeq
        for e in self.xmlHandler.find_all("dbReference", type="RefSeq"):
            if str(e.parent.name) == 'entry':
                for e_prot_id in e.find_all('property',type='nucleotide sequence ID'):
                    dic_xref["RefSeq"][e_prot_id["value"]] = e["id"]
        return dic_xref

    def parseInterpro(self):
        self.Interpro = []
        for e in self.xmlHandler.find_all("dbReference", type = "InterPro"):
            for name in e.find_all("property", type = "entry name"):
                self.Interpro.append(Interpro(e))

    @property
    def fasta(self):
        return '>' + str(self.id) + ' ' + str(self.name) + '\n' + str(self.sequence)

    def peptideSeed(self):
        return {
            'id' : self.id,
            'desc' : self.name,
            'seq' : str(self.sequence)
        }



        #self.parseIsoform()

    def hasKW(self, keyword):
        if keyword.upper() in (kw.id.upper() for kw in self.KW):
            return True
        return False
    
    @property
    def isGOannot(self):
        return not len(self.GO) == 0
        
    def hasGO(self, keyword):
        if keyword.upper() in (kw.id.upper() for kw in self.GO):
            return True
        return False

    def hasMIM(self, keyword):
        if keyword.upper() in (kw.id.upper() for kw in self.MIM):
            return True
        return False

    def hasORPHA(self, keyword):
        if keyword.upper() in (kw.id.upper() for kw in self.ORPHA):
            return True
        return False

    def hasDI(self, keyword):
        if keyword.upper() in (kw.id.upper() for kw in self.DI):
            return True
        return False

    # returns a position information container
    def pos(self, i, lookup=False):
        if  i < 1 or i >= len(self.sequence):
            raise IndexError("sequence index \""  + str(i) + "\" is out of range (" + str(len(self.sequence)) + ")")
        d = self._domainFlyCast(position=i)
        if len(d) > 1:
            raise ValueError("\"" + self.id + "\" lays more than one domain \"" + str(len(d)) +
                             "\" at position " + str(i)  )
        domain="SomeDefault"
        if d:
            domain = d[0]
        else:
            l = self._domainFlyCast(NterLookup=i)
            r = self._domainFlyCast(CterLookup=i)
            if l and r:
                domain = { 'outOfBounds' : 'hinge' }
            elif l:
                domain = { 'outOfBounds' : 'Cter' }
            elif r:
                domain = { 'outOfBounds' : 'Nter' }
            else:
                print ("Not a hinge a Cter or a Nter at " + str(i) + " in " + self.id)
        return Position(i, domain=domain, sse=self._getSse(i), letter=self.sequence[i])


    def _domainFlyCast(self, **kwargs):
        if not self.domains:
            raise ValueError("No domain data available for " + self.id)
            #return None
        if 'position' in kwargs:
            results = [ d._dict for d in self.domains if d.owns(kwargs['position']) ]
            return results
        if 'NterLookup' in kwargs:
            for i in range (int(kwargs['NterLookup']), 0, -1):
                d = self._domainFlyCast(position=i)
                if d:
                    return d#d[0]
        if 'CterLookup' in kwargs:
            for i in range (int(kwargs['CterLookup']), len(self.sequence) + 1):
                d = self._domainFlyCast(position=i)
                if d:
                    return d#d[0]


        return None

    def _getSse(self, position):
        i = int(position)
        if not self.sse:
            return None
        for d in self.sse:
            if d.begin <= i <= d.end:
                return d.type
        return "coil"
