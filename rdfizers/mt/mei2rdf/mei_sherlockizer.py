from lxml import etree
from rdflib import DCTERMS, RDF, RDFS, Graph, Literal as l, Namespace, URIRef as u, XSD

mei_ns = {"tei": "http://www.music-encoding.org/ns/mei"}
xml_ns = {"xml": "http://www.w3.org/XML/1998/namespace"}


def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return None


def isinteger(value):
    try:
        int(value)
        return True
    except ValueError:
        return None


crm_ns = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
crmdig_ns = Namespace("http://www.ics.forth.gr/isl/CRMdig/")
sherlockmei_ns = Namespace("http://data-iremus.huma-num.fr/ns/sherlockmei#")


def rdfize(graph, root, score_uuid, score_offsets, elements_offsets_data, output_ttl_file):
    g = Graph()
    g.bind("crm", crm_ns)
    g.bind("crmdig", crmdig_ns)
    g.bind("dcterms", DCTERMS)
    g.bind("sherlockmei", sherlockmei_ns)

    score_iri = u(score_uuid)

    g.add((score_iri, RDF.type, crmdig_ns["D1_Digital_Object"]))
    g.add((score_iri, RDF.type, crm_ns["E31_Document"]))
    g.add((score_iri, crm_ns["P2_has_type"], u("bf9dce29-8123-4e8e-b24d-0c7f134bbc8e")))  # Partition MEI
    g.add((score_iri, DCTERMS["format"], l("application/vnd.mei+xml")))

    # Score offsets
    for offset in score_offsets:
        score_offset_iri = u(score_uuid + "_offset-" + str(offset))
        g.add((score_offset_iri, sherlockmei_ns["in_score"], score_iri))
        # g.add((score_iri, crm_ns["P106_is_composed_of"], score_offset_iri))
        g.add((score_offset_iri, RDF.type, crmdig_ns["D35_Area"]))
        g.add((score_offset_iri, crm_ns["P2_has_type"], u("90a2ae1e-0fbc-4357-ac8a-b4b3f2a06e86")))  # the IRI of the concept: "MEI score offset"
        g.add((score_offset_iri, RDF.value, l(float(offset), datatype=XSD.float)))

    # Identified elements offsets data
    for k, v in elements_offsets_data.items():
        element_id = u(score_uuid + "_" + k)

        g.add((element_id, sherlockmei_ns["duration"], l(v["duration"], datatype=XSD.float)))
        g.add((element_id, sherlockmei_ns["offset_from"], l(v["from"], datatype=XSD.float)))
        g.add((element_id, sherlockmei_ns["offset_to"], l(v["to"], datatype=XSD.float)))
        g.add((element_id, sherlockmei_ns["measureNumber"], l(v["measureNumber"], datatype=XSD.integer)))
        g.add((element_id, sherlockmei_ns["beat"], l(v["beat"], datatype=XSD.float)))

        if "offsets" in v:
            for offset in v["offsets"]:
                # Link the current note to the current score offset
                score_offset_iri = u(score_uuid + "_offset-" + str(offset))
                g.add((element_id, sherlockmei_ns["contains_offset"], score_offset_iri))

                # Create an annotation anchor for each offset which occurs within the note duration
                element_offset_anchor_iri = u(score_uuid + "_" + k + "_offset-" + str(offset))
                g.add((element_id, sherlockmei_ns["has_offset_anchor"], element_offset_anchor_iri))
                g.add((element_offset_anchor_iri, crm_ns['P2_has_type'], u("689e148d-a97d-45b4-898d-c395a24884df")))  # the IRI of the concept: "Note offset anchor"
                g.add((element_offset_anchor_iri, RDF.value, l(float(offset), datatype=XSD.float)))

    # We census everything which has a xml:id
    for e in root.xpath("//*"):
        xmlida = "{" + xml_ns["xml"] + "}id"
        if xmlida in e.attrib:
            element_id = u(score_uuid + "_" + e.attrib[xmlida])

            g.add((element_id, sherlockmei_ns["in_score"], score_iri))

            g.add((element_id, RDF.type, crmdig_ns["D35_Area"]))

            if e.text and e.text.strip() and e.text.strip() != "None":
                g.add((element_id, sherlockmei_ns["text"], l(e.text.strip())))

            g.add((element_id, sherlockmei_ns["element"], l(etree.QName(e.tag).localname)))
            for a in e.attrib:
                if a != xmlida:
                    o = None
                    if isinteger(e.attrib[a]):
                        o = l(int(e.attrib[a]), datatype=XSD.integer)
                    elif isfloat(e.attrib[a]):
                        o = l(float(e.attrib[a]), datatype=XSD.float)
                    else:
                        o = l(e.attrib[a])
                    g.add((element_id, sherlockmei_ns[a], o))

            # xml:id E42
            e42_id = u(score_uuid + "_" + e.attrib[xmlida] + "_E42")
            g.add((element_id, crm_ns["P1_is_identified_by"], e42_id))
            g.add((e42_id, RDF.type, crm_ns["E42_Identifier"]))
            g.add((e42_id, RDFS.label, l(e.attrib[xmlida])))
            g.add((e42_id, crm_ns['P2_has_type'], u("db425957-e8bc-41d7-8a6b-d1b935cfe48d")))  # xml:id

            # P106 parent element
            if e.getparent() is not None:
                parent_element_id = score_uuid + "_" + e.getparent().attrib[xmlida]
                g.add((u(parent_element_id), crm_ns["P106_is_composed_of"], u(element_id)))
            else:
                g.add((score_iri, crm_ns["P106_is_composed_of"], u(element_id)))

    # That's all folks
    serialization = g.serialize(format='turtle', base="http://data-iremus.huma-num.fr/id/")
    with open(output_ttl_file, "w+") as f:
        f.write(serialization)
