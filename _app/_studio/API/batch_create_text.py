import hiero.ui as hui
import hiero.core as hcore
from pprint import pprint
import csv

active_seq = hui.activeSequence()
active_tl = hui.getTimelineEditor(active_seq)
track_item_list = active_tl.selection()

csv_file = r"D:\xyao\shot_name.csv"
with open(csv_file) as rf:
    data = list(csv.reader(rf))

for item in track_item_list:
    if not isinstance(item, hcore.TrackItem):
        continue
    item_name = item.name()
    for index, row in enumerate(data):
        if not row:
            continue
        reel_name = '%s' % (row[0])
        if reel_name == item_name:
            text_item = item.parent().createEffect(effectType='Text2', trackItem=item)
            text_node = text_item.node()
            text_node['message'].setValue(row[1])
            text_node['global_font_scale'].setValue(0.5)
            text_node['font'].setValue('KaiTi', 'Regular')


