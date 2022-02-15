import argparse
from asyncio.format_helpers import _format_callback
import chardet
from lxml import etree
from pprint import pprint

from sherlock_xml import idize
from mei_offsets import get_offsets_data
from mei_sherlockizer import rdfize

parser = argparse.ArgumentParser()
parser.add_argument("--input_mei_file")
parser.add_argument("--input_mei_file_uuid")
parser.add_argument("--output_mei_file")
parser.add_argument("--output_ttl_file")
args = parser.parse_args()

with open(args.input_mei_file, "rb") as f:
    f_content = f.read()
    input_mei_file_encoding = chardet.detect(f_content)
    input_mei_file_doc = etree.fromstring(f_content)
    idized_input_mei_file_doc = idize(input_mei_file_doc)
    with open(args.output_mei_file, "wb") as f2:
        etree.ElementTree(idized_input_mei_file_doc).write(
            f2,
            encoding='utf-8',
            xml_declaration=True,
            pretty_print=True
        )

    offsets_data = get_offsets_data(idized_input_mei_file_doc)

    # rdfize(
    #     "http://data-iremus.huma-num.fr/graph/mei",
    #     idized_input_mei_file_doc,
    #     args.input_mei_file_uuid,
    #     offsets_data["score_offsets"],
    #     offsets_data["elements"],
    #     args.output_ttl_file
    # )
