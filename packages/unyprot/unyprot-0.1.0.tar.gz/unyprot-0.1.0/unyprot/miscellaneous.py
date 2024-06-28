# Left over data types


class Domain(object):
    def __init__(self, xmlHandler, id):
        self.begin = [int(e['position']) for e in xmlHandler.find_all('begin')]
        self.end = [int(e['position']) for e in xmlHandler.find_all('end')]
        if len(self.begin) != len(self.end):
            raise ValueError("Number of end/stop differs " + str(self.begin) + "/" + str(self.end))
        if 'description' not in xmlHandler:
            #print "Warning Domain w/in \"" + id + "\" does not feature any description"
            self.description = None
        else:
            self.description = xmlHandler['description']
        self.carriedBy = id

    def __eq__(a, b):
        if a.id != b.id:
            return False
        if a.begin != b.begin:
            return False
        if a.end != b.end:
            return False
        if a.description != b.description:
            return False

        return True

    def __repr__(self):
        b = [ str (self.begin[i]) + "-" + str(self.end[i]) for i,e  in enumerate (self.begin) ]
        return "\"" + self.description + "\"\t" + ",".join(b) + "\n"

    def owns(self, position):
        try :
            j = int(position)
        except ValueError as err:
            print ("Improper amino acid position \"" + str(position) + "\"")
            return False

        for i, e  in enumerate (self.begin):
            if self.begin[i] <= j <= self.end[i]:
                return True

        return False



    @property
    def _dict(self):
        return self.__dict__

class Sse():
    def __init__(self, e):
        self.begin = int(e.find('begin')['position'])
        self.end =  int(e.find('end')['position'])
        self.type = e['type']
    def __repr__(self):
        return "SSE:" + self.type + " " + str(self.begin) + "-" + str(self.end)


class annotTerm:
    def __init__(self):
        pass
    def __hash__(self):
        return hash(str(self.id))
    def __eq__(self, other):
        return hash(self) == hash(other)

class GoKW(annotTerm):
    def __init__(self, id,term, evidence):
        self.id = id
        self.term = term
        self.evidence = evidence
    def __repr__(self):
        return self.id + ":" + self.term + "{" + self.evidence + "}"

class MimKW(annotTerm):
    def __init__(self, e):
        self.id = e['id']
        self.value = e.find('property', type='type')['value']
    def __repr__(self):
        return self.id + ":" + self.value

class OrphaKW(annotTerm):
    def __init__(self, e):
        self.id = e['id']
        self.type = e.find("property")['type']
        self.value = e.find('property')['value']

    def __repr__(self):
        return self.id + ": (" + self.type + ")" + self.value

class DI(annotTerm):
    def __init__(self, e):
        self.id = e['id']
        self.name = e.find('name').string
        acronym = e.find('acronym')
        self.acronym = acronym.string if acronym else 'NA'
        self.description = e.find('description').string
    def __repr__(self):
        return self.id + ":" + self.name + " (" + self.acronym + ") {" + self.description + "}"



class PDBref():
    def __init__(self, e):
        self.id = e['id']
        self.method = e.find('property', type='method')['value'] if e.find('property', type='method') else None
        self.resolution = e.find('property',type='resolution')['value'] if e.find('property', type='resolution') else None
        self.chains = e.find('property',type='chains')['value'] if e.find('property', type='chains') else None

    def __repr__(self):
        string = "PDB_id: " + self.id
        elements = []
        if self.method:
            elements.append("method: " + self.method)
        if self.resolution :
            elements.append("resolution: " + self.resolution)
        if self.chains:
            elements.append("chains: " + self.chains)
        if elements:
            return string + ':{' + ','.join(elements)  + '}'

        return string

class UniprotKW():
    def __init__(self, id, text):
        self.id = id
        self.term = text
    def __repr__(self):
        return self.id + ":" + self.term     

class Interpro():
    def __init__(self,e):
        self.id = e["id"]
        self.getName(e)

    def __repr__(self):
        return self.id + ":" + self.name

    def getName(self,e): 
        for name in e.find_all("property", type = "entry name"):
           self.name = name["value"]


class Genome():
    def __init__(self,xmlHandler):
        self.searchEMBL(xmlHandler)
        self.searchRefSeq(xmlHandler)

    def searchEMBL(self,xmlHandler):
        self.EMBLRef=[]
        self.EMBLProteinRef=[]
        for e in xmlHandler.find_all("dbReference", type="EMBL"):
            if str(e.parent.name) == 'entry':
                self.EMBLRef.append(e['id'])
                for e_prot_id in e.find_all('property',type='protein sequence ID'):
                    self.EMBLProteinRef.append(e_prot_id['value'])

    def searchRefSeq(self,xmlHandler):
        self.RefSeqRef=[]
        self.RefSeqProteinRef=[]
        for e in xmlHandler.find_all("dbReference", type="RefSeq"):
            if str(e.parent.name) == 'entry':
                self.RefSeqProteinRef.append(e['id'])
                for e_prot_id in e.find_all('property',type='nucleotide sequence ID'):
                    self.RefSeqRef.append(e_prot_id['value'])
