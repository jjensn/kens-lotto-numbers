import cv2
import imutils

class LottoImage:

  def __init__(self, path):
    self.original_image = cv2.imread(path)
    self.height, self.width = self.original_image.shape[:2]
    self.centerX = self.width // 2
    self.centerY = self.height // 2

    self.gray = cv2.cvtColor(self.original_image, cv2.COLOR_RGB2GRAY)

  def rotate(self, angle, image = None):
    img = self.gray.copy()
    
    if image:
      img = image

    return imutils.rotate_bound(img, angle)


    