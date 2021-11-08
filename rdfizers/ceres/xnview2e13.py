import argparse
from rdflib import DCTERMS, Graph, Literal, Namespace, RDF, RDFS, URIRef, XSD
import re
from sherlockcachemanagement import Cache
import sqlite3

################################################################################
# INIT
################################################################################

parser = argparse.ArgumentParser()
parser.add_argument('--author_uuid')
parser.add_argument('--cache')
parser.add_argument('--in_xnviewdb')
parser.add_argument('--out_ttl')
parser.add_argument('--vocabulary_uuid')
parser.add_argument('--vocabulary_title')
args = parser.parse_args()

cache = Cache(args.cache)
ceresfile = Namespace('http://ceres.huma-num.fr/sha1/')
crm = Namespace('http://www.cidoc-crm.org/cidoc-crm/')
crmdig = Namespace('http://www.cidoc-crm.org/crmdig/')
sherlock = Namespace('http://data-iremus.huma-num.fr/id/')
sherlockns = Namespace('http://data-iremus.huma-num.fr/ns/sherlock#')
g = Graph()
g.bind('ceresfile', str(ceresfile))
g.bind('crm', str(crm))
g.bind('crmdig', str(crmdig))
g.bind('dcterms', str(DCTERMS))
g.bind('sherlock', str(sherlock))
g.bind('sherlockns', str(sherlockns))

con = sqlite3.connect(args.in_xnviewdb)

################################################################################
# MEDIAS
################################################################################


def extension2mime(ext):
    return {
        'jpg': 'image/jpeg',
        'mp4': 'video/mp4',
        'png': 'image/png',
    }[ext]


mediaid2sha1 = {}
sha12mediaid = {}

cur = con.cursor()
for row in cur.execute('SELECT ImageID, Filename FROM Images'):
    if re.match('[0-9abcdef]{40}[\._].*', row[1]):
        sha1 = row[1][:40]
        mediaid2sha1[row[0]] = sha1
        if sha1 not in sha12mediaid:
            sha12mediaid[sha1] = []
        sha12mediaid[sha1].append(row[0])
        if row[1][40] == '.':
            g.add((ceresfile[sha1], RDF.type, crmdig['D1_Digital_Object']))
            extension = row[1].split('.')[1]
            g.add((ceresfile[sha1], DCTERMS.format, Literal(extension2mime(extension))))
            e42_sha1 = URIRef(cache.get_uuid(['media', sha1, 'e42_mime'], True))
            g.add((ceresfile[sha1], crm['P1_is_identified_by'], e42_sha1))
            g.add((e42_sha1, RDF.type, crm['E42_Identifier']))
            g.add((e42_sha1, crm['P2_has_type'], sherlock['01de41ec-850f-473b-bd7f-268a18afc6a3']))
            g.add((e42_sha1, RDFS.label, Literal(sha1)))

################################################################################
# TAGS
################################################################################

vocabulary = URIRef(args.vocabulary_uuid)
g.add((vocabulary, RDF.type, crm['E32_Authority_Document']))
g.add((vocabulary, crm['P1_is_identified_by'], Literal(args.vocabulary_title)))
g.add((vocabulary, DCTERMS.creator, URIRef(args.author_uuid)))

for row in cur.execute('SELECT TagID, Label, ParentID FROM Tags'):
    tag = URIRef(cache.get_uuid([args.author_uuid, 'tags', row[0]], True))
    parent_tag = URIRef(cache.get_uuid([args.author_uuid, 'tags', row[2]], True))

    g.add((tag, RDF.type, crm['E55_Type']))
    g.add((tag, crm['P1_is_identified_by'], Literal(row[1])))

    g.add((vocabulary, crm['P71_lists'], tag))
    if(row[2] == -1):
        g.add((vocabulary, sherlockns['sheP_a_pour_entité_de_plus_haut_niveau'], tag))
    else:
        g.add((tag, crm['P150_defines_typical_parts_of'], parent_tag))

################################################################################
# ANNOTATIONS
################################################################################

mediaid2tags = {}

for row in cur.execute('SELECT ImageID, TagID FROM TagsTree'):
    if row[0] not in mediaid2tags:
        mediaid2tags[row[0]] = []
    mediaid2tags[row[0]].append(row[1])

for mediaid, tags in mediaid2tags.items():
    sha1 = mediaid2sha1[mediaid]
    [id_a, id_b] = sha12mediaid[sha1]
    tags_a = mediaid2tags[id_a] if id_a in mediaid2tags else []
    tags_b = mediaid2tags[id_b] if id_b in mediaid2tags else []
    tags = sorted(set(tags_a + tags_b))

    for tag in tags:
        tag = URIRef(cache.get_uuid([args.author_uuid, 'tags', tag], True))
        e13 = URIRef(cache.get_uuid(['e13', sha1, tag], True))

        g.add((e13, RDF.type, crm['E13_Attribute_Assignment']))
        g.add((e13, crm['P14_carried_out_by'], URIRef(args.author_uuid)))
        g.add((e13, crm['P140_assigned_attribute_to'], ceresfile[sha1]))
        g.add((e13, crm['P141_assigned'], tag))
        g.add((e13, crm['P177_assigned_property_of_type'], sherlock['9fc0f49c-07c7-44b0-953c-8dfa3a698824']))

################################################################################
# THAT'S ALL FOLKS
################################################################################

cache.bye()
g.serialize(format='turtle', destination=args.out_ttl, base=sherlock)
