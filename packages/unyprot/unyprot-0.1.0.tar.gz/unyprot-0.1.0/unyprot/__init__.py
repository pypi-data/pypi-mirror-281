from .collection import EntrySet


def create_uniprot_collection_from_xml_file(xml_file):
    new_coll = EntrySet(collectionXML=xml_file)
    return new_coll

def create_uniprot_collection_from_xml_stream(xml_stream):
    new_coll = EntrySet(streamXML=xml_file)
    return new_coll
    