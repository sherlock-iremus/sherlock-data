from lxml import etree
from music21 import *


def get_offsets_data(score_xml):
    score = etree.tostring(score_xml, pretty_print=True)

    conv = mei.MeiToM21Converter(score)
    the_score = conv.run()

    for el in the_score.flatten().getElementsByClass(note.Note):
        print(el.pitch, el.measureNumber, el.duration.quarterLength, el.beat)
        # ./scripts/mt_mei.sh | grep " 96 "

    # identified_elements_offset_data = {}
    # score_offsets = set()

    # for el in the_score.recurse().sorted():
    #     if type(el.id) == str:
    #         if type(el.duration) == duration.Duration:
    #             score_offsets.add(el.offset)
    #             identified_elements_offset_data[el.id] = {
    #                 "from": el.offset,
    #                 "to": el.offset + el.duration.quarterLength,
    #                 "duration": el.duration.quarterLength,
    #                 "measureNumber": el.measureNumber,
    #                 "beat": el.beat
    #             }
    #             print(el.id, el.offset, el.measureNumber, el.beat)

    # for xmlid, data in identified_elements_offset_data.items():
    #     if not "offsets" in data:
    #         data["offsets"] = set()
    #         data["offsets"].add(data["from"])
    #     for _xmlid, _data in identified_elements_offset_data.items():
    #         if xmlid != _xmlid:
    #             if data["from"] <= _data["from"] and _data["from"] < data["to"]:
    #                 data["offsets"].add(_data["from"])

    # for xmlid, data in identified_elements_offset_data.items():
    #     if "offsets" in data:
    #         data["offsets"] = list(sorted(data["offsets"]))

    # return {
    #     "score_offsets": list(sorted(score_offsets)),
    #     "elements": identified_elements_offset_data
    # }