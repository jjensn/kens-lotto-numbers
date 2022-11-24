
import cv2

from imutils import contours
import numpy as np
import argparse

from matcher import TemplateMatch
from imutils.object_detection import non_max_suppression # pip install imutils
import math

image_search = TemplateMatch('./images/full.jpeg', './images/template.png')

image_search.find_powerball_logos()

image_search.draw_contours()

first_ticket = image_search.first_ticket()
last_ticket = image_search.last_ticket()

if first_ticket:
  cv2.putText(image_search.tickets.original_image, "First Ticket!", first_ticket.topleft_corner(), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)

if last_ticket:
  cv2.putText(image_search.tickets.original_image, "Last Ticket!", last_ticket.topleft_corner(), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)

cv2.imshow("Logo Boxes", image_search.tickets.original_image)
cv2.waitKey(0)
# clone = src.copy()

# result = cv2.matchTemplate(clone, temp, cv2.TM_CCOEFF_NORMED)
# (yCoords, xCoords) = np.where(result >= 0.8)
# #cv2.imshow("After NMS", rotated)
# #cv2.waitKey(0)

# rects = []
# for (x, y) in zip(xCoords, yCoords):
#   # draw the bounding box on the image
#   #l.append([(x, y),(x + tW, y + tH)] )
#   rr = RRect((x,y),(tW,tH),0)

#   # rr.draw(src)

#   #print(rr.p1)
#   # l.append(rr)

#   cv2.circle(img, rr.p2, 5, (0, 255, 0), -1)
#   #print("bounding box: {}".format(box))
#   #cv2.drawContours(src, [box], 0, (0, 0, 255), 2)
#   # matrix = cv2.getRotationMatrix2D( center=rect[0], angle=-1.0*i, scale=1 )
#   #tttt = cv2.warpAffine( src=rotated, M=matrix, dsize=(tH, tW) )
#   #cv2.imshow("After NMS", src)
#   #cv2.waitKey(0)
#   #break
#   #a = {}
#   #a['rect'] = (x, y, x + tW, y + tH)
#  #a['rot'] = rr
  
#   rect = cv2.minAreaRect(rr.to_contour())
#   box = cv2.boxPoints(rect)
#   box = np.int0(box)

#   print("bounding box: {}".format(box))
#   cv2.drawContours(img, [box], 0, (0, 0, 255), 2)
#   #print(rect)
#   #exit(0)
#   #rects.append((x, y, x + template_w, y + template_h))
#   #cv2.rectangle(clone, (x, y), (x + tW + 2, y + tH + 2), (255, 0, 0), -1)


# ROT = 5.0
# counter = 0
# for i in np.arange(-1.0 * ROT, ROT, 0.5):
#   # M = cv2.getRotationMatrix2D((cX, cY), i, 1.0)
#   # rotated = cv2.warpAffine(temp, M, (tW, tH))
#   rotated = imutils.rotate_bound(temp, i)
#   result = cv2.matchTemplate(clone, rotated, cv2.TM_CCOEFF_NORMED)
#   (yCoords, xCoords) = np.where(result >= 0.45)
#   #cv2.imshow("After NMS", rotated)
#   #cv2.waitKey(0)
  
  
#   for (x, y) in zip(xCoords, yCoords):
#     # draw the bounding box on the image
#     #l.append([(x, y),(x + tW, y + tH)] )
#     rr = RRect((x,y),(tW,tH),-i)

#     # rr.draw(src)

#     #print(rr.p1)
#     # l.append(rr)
#     cv2.circle(img, rr.p2, 5, (0, 255, 0), -1)
#     cv2.rectangle(clone, (x, y), (x + tW + 2, y + tH + 2), (255, 0, 0), -1)

#     rect = cv2.minAreaRect(rr.to_contour())
#     box = cv2.boxPoints(rect)
#     box = np.int0(box)

#     print("bounding box: {}".format(box))
#     cv2.drawContours(img, [box], 0, (0, 0, 255), 2)
#     #print("bounding box: {}".format(box))
#     #cv2.drawContours(src, [box], 0, (0, 0, 255), 2)
#     # matrix = cv2.getRotationMatrix2D( center=rect[0], angle=-1.0*i, scale=1 )
#     #tttt = cv2.warpAffine( src=rotated, M=matrix, dsize=(tH, tW) )
#     #cv2.imshow("After NMS", src)
#     #cv2.waitKey(0)
#     #break
#     # a = {}
#     # a['rect'] = (x, y, x + tW, y + tH)
#     # a['rot'] = rr
#     rects.append(rr.to_rect())
    
# pick = non_max_suppression(np.array(rects))
#     #clone = cv2.rectangle(clone, (x, y), (x + tW + 2, y + tH + 2), (255, 0, 0), -1)
#     #counter += 1

#     # if counter > 90:
#     #   print("see ya")
#     #   exit(0)

# # start = (0.0, 0.0)
# # curr_dist = 9999999.0000
# # first_card = None

# for (startX, startY, endX, endY) in pick:
#     # dist = dist_to(start, (startX, startY))
    
#     # if dist < curr_dist:
#     #   #start = (startX, startY)
#     #   curr_dist = dist
#     #   first_card = (startX, startY, endX, endY)

#     cv2.rectangle(img, (startX, startY), (endX, endY),(0, 255, 0), 2)

# #print(first_card)
# #cv2.putText(img, "first", (first_card[0], first_card[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
# # for c in l:
# #   cv2.rectangle(img, c[0], c[1], (255, 0, 0), 3)
# # locs = sorted(l, key=lambda x:x.p2[0])

# # print(len(locs))

# # if len(locs) > 90:
# #   print("f this")
# #   exit(0)

# # bcount = 0

# # for i in locs:
# #   font = 
  
# #   # org
# #   org = i.p0
    
# #   # fontScale
# #   fontScale = 1
    
# #   # Blue color in BGR
# #   color = (255, 0, 0)
    
# #   # Line thickness of 2 px
# #   thickness = 2
    
# #   # Using cv2.putText() method
# #   cv2.putText(img, str(bcount), org, font, 
# #                     fontScale, color, thickness, cv2.LINE_AA)
# #   bcount += 1
# cv2.imshow("After NMS", img)
# cv2.waitKey(0)


# # (cX, cY) = (W // 2, H // 2)
# # # rotate our image by 45 degrees around the center of the image
# # M = cv2.getRotationMatrix2D((cX, cY), 3, 1.0)
# # rotated = cv2.warpAffine(temp, M, (W, H))
# # # show our output image *before* applying non-maxima suppression
# # cv2.imshow("Before NMS", rotated)
# # cv2.waitKey(0)
# # # for method in methods:
# # #    src2 = src.copy()
# # #    result = cv2.matchTemplate(src2, temp, method)
# # #    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
# # #    print(min_loc, max_loc)
# # #    if method in [cv2.TM_SQDIFF,cv2.TM_CCORR]:
# # #      lacation = min_loc
# # #    else:
# # #      location = max_loc
# # #    bottom_right = (location[0] + W, location[1] + H)
# # #    cv2.rectangle(img, location,bottom_right, (0, 0, 255), 1)
# # #    cv2.imshow("images", img)
# # #    cv2.waitKey(0)
# # #    cv2.destroyAllWindows() 