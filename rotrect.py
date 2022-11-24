import numpy as np
import cv2

class RRect:
  def __init__(self, p0, s, ang):
    self.p0 = (int(p0[0]),int(p0[1]))
    (self.W, self.H) = s
    self.ang = ang
    self.p1,self.p2,self.p3 = self.get_verts(p0,s[0],s[1],ang)
    self.verts = [self.p0,self.p1,self.p2,self.p3]

  def get_verts(self, p0, W, H, ang):
    sin = np.sin(ang/180*3.14159)
    cos = np.cos(ang/180*3.14159)
    P1 = (int(self.H*sin)+p0[0],int(self.H*cos)+p0[1])
    P2 = (int(self.W*cos)+P1[0],int(-self.W*sin)+P1[1])
    P3 = (int(self.W*cos)+p0[0],int(-self.W*sin)+p0[1])
    return [P1,P2,P3]

  def draw(self, image):
    print(self.verts)
    for i in range(len(self.verts)-1):
      cv2.line(image, (self.verts[i][0], self.verts[i][1]), (self.verts[i+1][0],self.verts[i+1][1]), (0,255,0), 2)
    cv2.line(image, (self.verts[3][0], self.verts[3][1]), (self.verts[0][0], self.verts[0][1]), (0,255,0), 2)

  def to_contour(self):
    return np.array([
            [self.p0],
            [self.p1],
            [self.p2],
            [self.p3]]
      )
  
  def to_rect_tuple(self):
    return  (self.p0[0], self.p0[1], self.p2[0], self.p2[1])

  def cv2_min_area_rect(self):
    return cv2.minAreaRect(self.to_contour())
  
  def cv2_box_points(self):
    return cv2.boxPoints(self.cv2_min_area_rect())

  def topleft_corner(self):
    return (self.p0[0], self.p0[1])