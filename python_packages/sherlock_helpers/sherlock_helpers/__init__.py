from rdflib import Graph, Literal, Namespace, RDF, RDFS, SKOS, URIRef, XSD
import re
import uuid

################################################################################
# CONSTANTS
################################################################################

SHERLOCK_DATA = Namespace("http://data-iremus.huma-num.fr/id/")
CRM = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
SHERLOCK = Namespace("http://data-iremus.huma-num.fr/ns/sherlock#")
E42_types = {
    "sherlock_annotation_project_code": "5372610b-88b1-4949-b87a-1e5102bf2fb7",
    "catalogue_bnf_fr": "59835932-52aa-4a19-ac6e-916d2a4b9228",
    "data_bnf_fr": "df9f27d6-b08b-46e6-ad67-202259c4cdbd",
    "gallica": "f4262bac-f72c-40e2-aa51-ae352da5a35c",
    "grove": "179c61b8-4215-4644-bb52-ad9fe2094da1",
    "isni": "49729025-e609-46ed-a749-5f3ae53dbfbe",
    "mgg": "5d535add-e1bc-421d-b4f3-190dbd788fd3",
    "opentheso": "c7465286-fe10-4b2a-a764-c2a25ed3c63f",
    "rism": "c3c91ea4-e5eb-4c22-9727-923564355d2e",
    "versailles": "c8e6991d-46cf-401a-9218-4dbda6abb805",
    "viaf": "bae39954-9d0c-40e4-8258-c1b6dfd0a4a4",
    "wikidata": "d1106e67-f0b7-4eb6-a4dd-54f39e33559a"
}
P3_types = {
    "definition": "c5402ae4-4ae9-48a1-86ed-c13de0c97d53",
    "définition": "c5402ae4-4ae9-48a1-86ed-c13de0c97d53",
    "note_historique": "60e0538c-c548-4e0a-8456-4bd654acb59d"
}

################################################################################
# HELPERS
################################################################################


def hash_string_to_uuid(string):
    namespace = uuid.NAMESPACE_DNS
    return uuid.uuid5(namespace, string)


def remove_trailing_integers(s):
    return re.sub(r'\d+$', '', s)


def make_graph():
    g = Graph(base=str(SHERLOCK_DATA))
    g.bind("crm", CRM)
    g.bind("sherlock", SHERLOCK)
    return g


################################################################################
# CLASS
################################################################################

class DataParser:

    def __init__(self, sherlock_project_code, out_ttl, sherlock_e13_e55_ttl, e13_authors):
        self.E13_E55_BY_CODE = {}
        self.sherlock_project_code = sherlock_project_code
        self.out_ttl = out_ttl
        self.graph = make_graph()
        self.init_sherlock_e13_e55(sherlock_e13_e55_ttl)
        self.e13_authors = [URIRef(x) for x in e13_authors]

    def __del__(self):
        self.graph.serialize(destination=self.out_ttl, encoding='utf-8')

    def init_sherlock_e13_e55(self, sherlock_e13_e55_ttl):
        sherlock_e13_e55_graph = Graph()
        sherlock_e13_e55_graph.parse(sherlock_e13_e55_ttl)
        knows_query = """
        PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX sherlock: <http://data-iremus.huma-num.fr/id/>
        SELECT DISTINCT ?e55 ?code
        WHERE {
            ?e55 ?p ?o .
            ?e55 rdf:type crm:E55_Type .
            ?e55 crm:P1_is_identified_by ?e42 .
            ?e42 rdf:type crm:E42_Identifier .
            ?e42 crm:P2_has_type sherlock:5372610b-88b1-4949-b87a-1e5102bf2fb7 .
            ?e42 crm:P190_has_symbolic_content ?code .
        }
        ORDER BY ?code
        """

        qres = sherlock_e13_e55_graph.query(knows_query)
        for row in qres:
            self.E13_E55_BY_CODE[str(row.code)] = row.e55.split('/')[-1]

    def process_cell(self, subject, column_name, column_value):
        column_value = str(column_value)
        column_name.strip().lower()
        if column_value:
            column_value.strip()
        if not column_value:
            return False

        # How many parts?
        column_name = column_name.replace('__', '🍄‍🟫')
        column_names_parts = column_name.split('🍄‍🟫')

        # We have a predicate! (or a predicate that points to a lesser CRM entity)
        if len(column_names_parts) == 1:
            if re.match('P1', column_name):
                self.graph.add((subject, CRM.P1_is_identified_by, Literal(column_value)))
            elif re.match('skos_prefLabel', column_name):
                self.graph.add((subject, SKOS.prefLabel, Literal(column_value)))
            elif re.match('skos_altLabel\d*', column_name):
                self.graph.add((subject, SKOS.altLabel, Literal(column_value)))
            elif re.match('P82aP82b', column_name):
                self.make_E52(subject, column_value)
            elif re.match('P3_.*', column_name):
                self.make_P3(subject, column_value, P3_types[remove_trailing_integers(column_name.replace('P3_', ''))])
            elif re.match('E42_.*', column_name):
                E42_type = remove_trailing_integers(column_name.replace('E42_', ''))
                if E42_type in E42_types:
                    self.make_E42(subject, column_value, E42_types[E42_type])
                else:
                    print("Type d'identifiant inconnu :", E42_type)
            elif column_name.startswith('E13_'):
                x = column_name.replace('E13_', '')
                x = self.sherlock_project_code + '::' + x
                annotation_type_uuid = self.E13_E55_BY_CODE[x]
                self.make_E13_with_literal_P141(subject, annotation_type_uuid, column_value)

    def make_E52(self, subject, P82aP82b_column_value, graph):
        E52 = URIRef(str(uuid.uuid4()))
        self.graph.add((subject, CRM['P4_has_time-span'], E52))
        self.graph.add((E52, CRM.P82a_begin_of_the_begin, Literal(P82aP82b_column_value, datatype=XSD.dateTime)))
        self.graph.add((E52, CRM.P82b_end_of_the_end, Literal(P82aP82b_column_value, datatype=XSD.dateTime)))

    def make_P3(self, subject, column_value, P3_type):
        pc = URIRef(str(uuid.uuid4()))
        self.graph.add((pc, RDF.type, CRM.PC3_has_note))
        self.graph.add((pc, CRM.P01_has_domain, subject))
        self.graph.add((pc, CRM.P03_has_range_literal, Literal(column_value)))
        self.graph.add((pc, CRM['P3.1_has_type'], SHERLOCK_DATA[P3_type]))

    def make_E42(self, subject, column_value, E42_type):
        E42 = URIRef(str(uuid.uuid4()))
        self.graph.add((subject, CRM.P1_is_identified_by, E42))
        self.graph.add((E42, RDF.type, CRM.E42_Identifier))
        self.graph.add((E42, CRM.P2_has_type, SHERLOCK_DATA[E42_type]))
        if column_value.startswith('http'):
            self.graph.add((E42, CRM.P190_has_symbolic_content, URIRef(column_value)))
        else:
            self.graph.add((E42, CRM.P190_has_symbolic_content, Literal(column_value)))

    def make_E13_with_literal_P141(self, P140, P177, P141):
        E13 = URIRef(str(uuid.uuid4()))
        self.graph.add((E13, RDF.type, CRM.E13_Attribute_Assignment))
        self.graph.add((E13, CRM.P140_assigned_attribute_to, P140))
        self.graph.add((E13, CRM.P177_assigned_property_of_type, URIRef(P177)))
        self.graph.add((E13, CRM.P141_assigned, Literal(P141)))
        for e13_author in self.e13_authors:
            self.graph.add((E13, CRM.P14_carried_out_by, e13_author))
