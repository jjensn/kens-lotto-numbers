
import cv2

from imutils import contours
import numpy as np
import argparse
from pbticket import PBLottoTicket
from matcher import TemplateMatch
from imutils.object_detection import non_max_suppression # pip install imutils
import math

image_search = TemplateMatch('./images/test/full2.jpeg', './images/template_pb.png')

image_search.find_powerball_logos()

image_search.adjust_ticket_rectangles()

tickets = []

for v in image_search.logo_locations:
  i = v.crop_image(image_search.tickets.original_image)
  t = PBLottoTicket(i)
  t.extract_numbers()

  tickets.append(t)
