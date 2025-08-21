from rdflib import Graph, Literal, Namespace, RDF, RDFS, SKOS, URIRef, XSD
import re
import uuid

################################################################################
# CONSTANTS
################################################################################

SHERLOCK_DATA = Namespace("http://data-iremus.huma-num.fr/id/")
CRM = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
SHERLOCK = Namespace("http://data-iremus.huma-num.fr/ns/sherlock#")

ENTITIES_CODE_TO_CLASS_URI = {
    'E65': CRM.E65_Creation
}

DIRECT_PROPERTIES = {
    'P9_consists_of': 'P9i_forms_part_of',
    'P70_documents': 'P70i_is_documented_in',
    'P94_has_created': 'P94i_was_created_by',
}

INVERSE_PROPERTIES = {
    'P9i_forms_part_of': 'P9_consists_of',
    'P70i_is_documented_in': 'P70_Documents',
    'P94i_was_created_by': 'P94_has_created',
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


def get_entity_uri_by_code(code):
    if code not in ENTITIES_CODE_TO_CLASS_URI:
        raise ValueError(f'Unknown entity code: "{code}"')
    return ENTITIES_CODE_TO_CLASS_URI[code]


def format_crm_property(p):
    if p.startswith('crm:'):
        p = p.replace('crm:', '')
    if not p.startswith(str(CRM)):
        p = CRM[p]
    return p


################################################################################
# CLASS
################################################################################

class DataParser:

    def __init__(self, rdf_properties, project_id, out_ttl, e13_authors, e41_e55, e42_e55, e13_e55, p3_e55, makerdfslabelfrom):
        self.rdf_properties_prefixes = set()
        for x in rdf_properties.keys():
            self.rdf_properties_prefixes.add(x.split(':')[0])
        self.RDF_PROPERTIES = rdf_properties
        self.E41_E55_BY_CODE = e41_e55
        self.E42_E55_BY_CODE = e42_e55
        self.E13_E55_BY_CODE = e13_e55
        self.P3_E55_BY_CODE = p3_e55

        self.project_id = project_id
        self.out_ttl = out_ttl
        self.graph = make_graph()
        self.e13_authors = [URIRef(x) for x in e13_authors]
        self.makerdfslabelfrom = makerdfslabelfrom

        self.unknown_E41_id = set()
        self.unknown_E42_id = set()
        self.processed_column_names = set()
        self.unprocessed_column_names = set()

    def __del__(self):
        self.graph.serialize(destination=self.out_ttl, encoding='utf-8')

    def process_cell(self, subject, column_name, column_value):
        column_value = str(column_value)
        column_name = column_name.strip()
        if column_value:
            column_value = column_value.strip()
        if not column_value:
            return False

        # How many parts?
        column_names_parts = column_name.split('___')

        matched = False

        # We have a predicate! (or a predicate that points to a lesser CRM entity)
        if len(column_names_parts) == 1:
            # First we check if it's a RDF property
            rdf_property_uri = self.get_rdf_property_uri(column_name)
            if rdf_property_uri:
                self.graph.add((subject, URIRef(rdf_property_uri), Literal(column_value)))
                matched = True
            else:
                if re.match('P1_', column_name):
                    self.graph.add((subject, CRM.P1_is_identified_by, Literal(column_value)))
                    matched = True
                elif re.match('P102_', column_name):
                    self.graph.add((subject, CRM.P102_has_title, Literal(column_value)))
                    matched = True
                elif re.match('P82aP82b', column_name):
                    self.make_E52(subject, column_value)
                    matched = True
                elif re.match('P3_.*', column_name):
                    self.make_P3(subject, column_value, self.P3_E55_BY_CODE[remove_trailing_integers(column_name.replace('P3_', ''))])
                    matched = True
                elif re.match('E42_.*', column_name):
                    E42_type = remove_trailing_integers(column_name.replace('E42_', ''))
                    if E42_type in self.E42_E55_BY_CODE:
                        self.make_E42(subject, column_value, self.E42_E55_BY_CODE[E42_type])
                        matched = True
                    else:
                        self.unknown_E42_id.add(E42_type)
                elif re.match('E41_.*', column_name):
                    E41_type = remove_trailing_integers(column_name.replace('E41_', ''))
                    if E41_type in self.E41_E55_BY_CODE:
                        self.make_E41(subject, column_value, self.E41_E55_BY_CODE[E41_type])
                        matched = True
                    else:
                        self.unknown_E41_id.add(E41_type)
                elif column_name.startswith('E13_'):
                    x = column_name.replace('E13_', '')
                    x = self.project_id + '::' + x
                    annotation_type_uuid = self.E13_E55_BY_CODE[x]
                    self.make_E13_with_literal_P141(subject, annotation_type_uuid, column_value)
                    # rdfs:label
                    if x in self.makerdfslabelfrom:
                        current_rdfs_label_value = self.graph.value(subject=subject, predicate=RDFS.label)
                        if current_rdfs_label_value:
                            self.graph.remove((subject, RDFS.label, Literal(current_rdfs_label_value)))
                        else:
                            current_rdfs_label_value = ''
                        new_rdfs_label = ' • '.join(filter(lambda x: x, [current_rdfs_label_value, column_value]))
                        self.graph.add((subject, RDFS.label, Literal(new_rdfs_label)))
                    matched = True
                elif column_value != '0':
                    if column_name in DIRECT_PROPERTIES.keys() or column_name in INVERSE_PROPERTIES.keys():
                        self.make_p_and_pi(column_name, subject, URIRef(column_value))
                        matched = True
        if len(column_names_parts) == 3:
            # Properties creation
            p1 = column_names_parts[0]
            p1i = None
            p2 = column_names_parts[2]
            p2i = None
            if p1 in DIRECT_PROPERTIES:
                p1i = DIRECT_PROPERTIES[p1]
            elif p1 in INVERSE_PROPERTIES:
                p1i = INVERSE_PROPERTIES[p1]
            if p2 in DIRECT_PROPERTIES:
                p2i = DIRECT_PROPERTIES[p2]
            elif p2 in INVERSE_PROPERTIES:
                p2i = INVERSE_PROPERTIES[p2]
            # Medium entity creation
            medium_entity_class_resource = get_entity_uri_by_code(column_names_parts[1])
            medium_entity_resource = URIRef(str(uuid.uuid4()))
            self.graph.add((medium_entity_resource, RDF.type, medium_entity_class_resource))
            # Weaving
            self.graph.add((subject, format_crm_property(p1), medium_entity_resource))
            self.graph.add((medium_entity_resource, format_crm_property(p1i), subject))
            self.graph.add((medium_entity_resource, format_crm_property(p2), URIRef(column_value)))
            self.graph.add((URIRef(column_value), format_crm_property(p2i), medium_entity_resource))
            matched = True
        if matched == False and column_name != 'UUID':
            self.unprocessed_column_names.add(column_name)
        else:
            self.processed_column_names.add(column_name)

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

    def make_E41(self, subject, column_value, E41_type):
        E41 = URIRef(str(uuid.uuid4()))
        self.graph.add((subject, CRM.P1_is_identified_by, E41))
        self.graph.add((E41, RDF.type, CRM.E41_Appellation))
        self.graph.add((E41, CRM.P2_has_type, SHERLOCK_DATA[E41_type]))
        if column_value.startswith('http'):
            self.graph.add((E41, CRM.P190_has_symbolic_content, URIRef(column_value)))
        else:
            self.graph.add((E41, CRM.P190_has_symbolic_content, Literal(column_value)))

    def make_E13_with_literal_P141(self, P140, P177, P141):
        E13 = URIRef(str(uuid.uuid4()))
        self.graph.add((E13, RDF.type, CRM.E13_Attribute_Assignment))
        self.graph.add((E13, CRM.P140_assigned_attribute_to, P140))
        self.graph.add((E13, CRM.P177_assigned_property_of_type, URIRef(P177)))
        self.graph.add((E13, CRM.P141_assigned, Literal(P141)))
        for e13_author in self.e13_authors:
            self.graph.add((E13, CRM.P14_carried_out_by, e13_author))

    def log(self):
        print('🦀' * 80)
        print('WHEN MAKING TTL DATA IN :', self.out_ttl)
        print('UNKNOWN E41 ID          :', ' • '.join((self.unknown_E41_id)))
        print('UNKNOWN E42 ID          :', ' • '.join((self.unknown_E42_id)))
        print('UNPROCESSED COLUMN NAMES:', ' • '.join(sorted(self.unprocessed_column_names)))
        print('PROCESSED COLUMN NAMES. :', ' • '.join(sorted(self.processed_column_names)))

    def get_rdf_property_uri(self, column_name):
        column_name_parts = column_name.split('_')
        prefix = column_name_parts[0]
        if prefix in self.rdf_properties_prefixes:
            localName = ''
            if column_name_parts[-1].isdigit():
                localName = '_'.join(column_name_parts[1:-1])
            else:
                localName = '_'.join(column_name_parts[1:])
            return self.RDF_PROPERTIES[prefix + ':' + localName]
        return None

    def make_p_and_pi(self, x, s, o):
        p = None
        pi = None
        if x in DIRECT_PROPERTIES:
            p = x
            pi = DIRECT_PROPERTIES[x]
        elif x in INVERSE_PROPERTIES:
            p = INVERSE_PROPERTIES[x]
            pi = x
        self.graph.add((s, format_crm_property(p), o))
        self.graph.add((o, format_crm_property(pi), s))
