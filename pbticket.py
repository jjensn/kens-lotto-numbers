import cv2
import numpy as np
import re
import pytesseract

from pick import SinglePick
class PBLottoTicket:

  def __init__(self, image):
    # = image
    self.ticket_picks = []
    self.image = image

    rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 3))
    # apply a blackhat morphological operator to find dark
    # regions against a light background
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    tophat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, rectKernel)
  
    thresh = cv2.threshold(tophat, 60, 255, cv2.THRESH_BINARY)[1]
    # compute the Scharr gradient of the tophat image
    gradX = cv2.Sobel(tophat, ddepth=cv2.CV_32F, dx=1, dy=0,ksize=-1)
    gradX = np.absolute(gradX)
    (minVal, maxVal) = (np.min(gradX), np.max(gradX))
    gradX = (255 * ((gradX - minVal) / (maxVal - minVal)))
    gradX = gradX.astype("uint8")
    gradX = cv2.morphologyEx(gradX, cv2.MORPH_CLOSE, rectKernel)
    thresh = cv2.threshold(gradX, 0, 255,
      cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    #cv2.imshow("tophat", thresh)
    #cv2.waitKey(0)
    self.cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
      cv2.CHAIN_APPROX_SIMPLE)

  def crop_ticket(self, rect):
    # Get center, size, and angle from rect
    shape = (self.image.shape[1], self.image.shape[0])  # cv2.warpAffine expects shape in (length, height)
    center, size, theta = rect
    width, height = tuple(map(int, size))
    center = tuple(map(int, center))
    if width < height:
        theta -= 90
        width, height = height, width
      
    matrix = cv2.getRotationMatrix2D(center=center, angle=theta, scale=1.0)
    timage = cv2.warpAffine(src=self.image, M=matrix, dsize=shape  )

    x = int(center[0] - width // 2)
    y = int(center[1] - height // 2)

    image = timage[y-2: y + height+6, x - 3 : x + width + 3]

    return image

  def extract_numbers(self):
    # debug = self.image.copy()
    for (i, c) in enumerate(self.cnts[0]):

      # compute the bounding box of the contour
      (x, y, w, h) = cv2.boundingRect(c)

      if w < 120:
        continue

      rect = cv2.minAreaRect(c)  

      img = self.crop_ticket(rect)
      row_nums = self.ocr(img)
      p = SinglePick(row_nums)
    
      self.ticket_picks.append(p)

    return self.ticket_picks

  def ocr(self, img):
    
    ret = []
    
    try:
      resized = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    except:
      return ret

    blurred = cv2.medianBlur(resized, 1)    
    gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
    
    digitCnts = cv2.findContours(gray, cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)[0]

    cv2.drawContours(gray, digitCnts, 0, (0, 255, 0), 1)
    thresh = gray
    
    text = pytesseract.image_to_string(thresh, lang='eng', config='--psm 7 --oem 3 -c tessedit_char_whitelist=0123456789PB:\" \".')

    nums = text.split(" ")

    cleaned_nums = []

    for (i,n) in enumerate(nums):
      stripped = re.sub("[^0-9]", "", n)

      if not stripped:
        continue

      x = int(stripped)
      if x > 69:
        print("Have a bigger num than allowed - bad OCR read")
        print(x)
        numstr = str(x)
        if i == 0:
          print("Might be a misinterpretation of the row letter..")
          if numstr[0] == '8':
            print("Likely a B interpreted as an 8 ... correcting")
            x = int(numstr[1:])
          elif numstr[0] == '4':
            print("Likely an A interpreted as an 4 ... correcting")
            x = int(numstr[1:])
          else:
            print("No idea, skipping")
            print(x)
            return ret
        else:
          print("No real options I know of")
          cv2.imshow("Bad Parse", thresh)
          cv2.waitKey(0)
          return ret
    
      cleaned_nums.append(x)

    if len(cleaned_nums) != 6:
      if cleaned_nums[0] == 0:
        cleaned_nums = cleaned_nums[1:]
        print(cleaned_nums)
      else:
        print("Bad parse - not enough digits read")
        cv2.imshow("Bad Parse - not enough digits read", thresh)
        cv2.waitKey(0)
        return ret
    else:
      return cleaned_nums
    
    