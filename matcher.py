from lotto_image import LottoImage
from rotrect import RRect

import cv2
import numpy as np
import math

class TemplateMatch:

  SAFE_LOGO_DIST = 5.0

  def __init__(self, tickets: str, template: str):
    self.tickets = LottoImage(tickets)
    self.template = LottoImage(template)

    self.ticket_copy = self.tickets.gray.copy()
    self.template_copy = self.template.gray.copy()

    self.logo_locations = {}

  def have_bounds_nearby(self, haystack, topleft_coords) ->bool:
    
    x_nearby = False
    y_nearby = False

    corner_x = topleft_coords[0]
    corner_y = topleft_coords[1]

    for k, v in haystack.items():
      x = k[0]
      y = k[1]

      if corner_x <= x <= corner_x+self.SAFE_LOGO_DIST or corner_x-self.SAFE_LOGO_DIST <= x <= corner_x:
        x_nearby = True

      if corner_y <= y <= corner_y+self.SAFE_LOGO_DIST or corner_y-self.SAFE_LOGO_DIST <= y <= corner_y:
        y_nearby = True

      if x_nearby and y_nearby:
        break

    return x_nearby and y_nearby

  def find_logo_bounds(self, template_image, threshold, rotation = 0) ->dict:

    bounds_dict = {}

    result = cv2.matchTemplate(self.ticket_copy, template_image, cv2.TM_CCOEFF_NORMED)

    (yCoords, xCoords) = np.where(result >= threshold)

    for (x, y) in zip(xCoords, yCoords):
      rot = RRect((x,y), (self.template.width, self.template.height), rotation)

      if not rot.topleft_corner() in bounds_dict and not self.have_bounds_nearby(bounds_dict, rot.topleft_corner()):
        bounds_dict[rot.topleft_corner()] = rot

        # we cheat and just draw a rectangle over the logo we found already so we don't find it again
        cv2.rectangle(self.ticket_copy, (x, y), (x + self.template.width + 2, y + self.template.height + 2), (255, 0, 0), -1)

    return bounds_dict


  def find_rotated_logos(self, consider_degrees, step = 0.5) ->dict:
    
    bounds_dict = {} 

    for i in np.arange(-1.0 * consider_degrees, consider_degrees, step):      
      rotated_logo = self.template.rotate(i)

      bounds_dict.update(self.find_logo_bounds(rotated_logo, 0.45, -i))

    return bounds_dict

  def find_powerball_logos(self):

    self.logo_locations.clear()

    # perform a straight match (without rotating) first to identify the easy logos
    non_rotated_logos = self.find_logo_bounds(self.template_copy, 0.8)

    # rotate the logo by -5 and +5 degrees to find others (because Ken can't be assed to do it right)
    rotated_logos = self.find_rotated_logos(5.0)

    # prefer the non-rotated ones before the rotated ones in the dict
    rotated_logos.update(non_rotated_logos)

    self.logo_locations = rotated_logos.copy()

    print(f'Found {len(self.logo_locations)} markers in the image')

  def tickets_per_row(self) -> int:
    pass

  def tickets_per_column(self) -> int:
    pass

  def first_ticket(self) -> RRect:
    start = (0.0, 0.0)
    curr_dist = 9999999.0000
    ticket = None

    for k,v in self.logo_locations.items():
      dist = math.dist(start, v.topleft_corner())
    
      if dist < curr_dist:
        curr_dist = dist
        ticket = k

    if ticket:
      return self.logo_locations[ticket]
    else:
      return None


  def last_ticket(self) -> RRect:
    start = (self.tickets.width, self.tickets.height)

    print(start)
    curr_dist = 9999999.0000
    ticket = None

    for k,v in self.logo_locations.items():
      dist = math.dist(start, v.topleft_corner())
    
      if dist < curr_dist:
        curr_dist = dist
        ticket = k

    if ticket:
      return self.logo_locations[ticket]
    else:
      return None

  def draw_contours(self):
    for k,v in self.logo_locations.items():

      pts = v.to_rect_tuple()
      #cv2.rectangle(self.tickets.original_image,(pts[0], pts[1]), (pts[2], pts[3]), (255, 125, 0), 2)

      box = np.int0(v.cv2_box_points())
      cv2.drawContours(self.tickets.original_image, [box],0, (124, 0, 255), 2)

    