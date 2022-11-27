import numpy as np
import cv2

class RRect:
  def __init__(self, top_left, s, ang):
    self.top_left = (int(top_left[0]),int(top_left[1]))
    (self.W, self.H) = s
    self.ang = ang
    self.bottom_left,self.bottom_right,self.top_right = self.get_verts(top_left,s[0],s[1],ang)
    self.verts = [self.top_left,self.bottom_left,self.bottom_right,self.top_right]

  def get_verts(self, top_left, W, H, ang):
    sin = np.sin(ang/180*3.14159)
    cos = np.cos(ang/180*3.14159)
    bottom_left = (int(self.H*sin)+top_left[0],int(self.H*cos)+top_left[1])
    bottom_right = (int(self.W*cos)+bottom_left[0],int(-self.W*sin)+bottom_left[1])
    top_right = (int(self.W*cos)+top_left[0],int(-self.W*sin)+top_left[1])
    return [bottom_left,bottom_right,top_right]

  def draw(self, image):
    print(self.verts)
    for i in range(len(self.verts)-1):
      cv2.line(image, (self.verts[i][0], self.verts[i][1]), (self.verts[i+1][0],self.verts[i+1][1]), (0,255,0), 2)
    cv2.line(image, (self.verts[3][0], self.verts[3][1]), (self.verts[0][0], self.verts[0][1]), (0,255,0), 2)

  def to_contour(self):
    return np.array([
            [self.top_left],
            [self.bottom_left],
            [self.bottom_right],
            [self.top_right]]
      )
  
  def to_rect_tuple(self):
    return  (self.top_left[0], self.top_left[1], self.bottom_right[0], self.bottom_right[1])

  def cv2_min_area_rect(self):
    return cv2.minAreaRect(self.to_contour())
  
  def cv2_box_points(self):
    return cv2.boxPoints(self.cv2_min_area_rect())

  def center(self):
    return self.cv2_min_area_rect()[0]

  def extend_bottom_by(self, amount):
    self.bottom_left = (self.bottom_left[0], self.bottom_left[1] + amount)
    self.bottom_right = (self.bottom_right[0], self.bottom_right[1] + amount)

  def extend_right_by(self, amount):
    self.top_right = (self.top_right[0]+ amount, self.top_right[1])
    self.bottom_right = (self.bottom_right[0]+ amount, self.bottom_right[1])

  def rect_rotate(self, rect, angle=None):
  
    if angle is None:
        angle = rect[2]
    rad = np.deg2rad(np.abs(angle))
    rot_matrix_2d = np.array([[np.cos(rad), np.sin(rad)],
                              [np.sin(rad), np.cos(rad)]])

    # cal. center of rectangle
    center = np.sum(np.array(rect[1]).reshape(1, -1) * rot_matrix_2d, axis=-1) * .5
    center = np.abs(center)

    return tuple(center), rect[1], angle

  def crop_ticket(self, rect, image):
    # Get center, size, and angle from rect
    shape = (image.shape[1], image.shape[0])  # cv2.warpAffine expects shape in (length, height)
    center, size, theta = rect
    width, height = tuple(map(int, size))
    center = tuple(map(int, center))

    if width < height:
        theta -= 90
        width, height = height, width

    matrix = cv2.getRotationMatrix2D(center=center, angle=-theta, scale=1.0)
    timage = cv2.warpAffine(src=image, M=matrix, dsize=shape)

    x = int(center[0] - width // 2)
    y = int(center[1] - height // 2)

    return timage[y-5 : y + height, x-10 : x + width+5]

  def crop_image(self, image):
    # Get perspective transform and apply it
    W = self.W
    H = self.H
    #r = self.rect_rotate(s, self.ang)
    result = self.crop_ticket(self.cv2_min_area_rect(), image)
    # exit(0)
    return result
    # def topleft_corner(self):
    #   return (self.top_left[0], self.top_left[1])