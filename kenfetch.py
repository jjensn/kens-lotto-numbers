from bs4 import *
import requests
import os 

class KensLottoPool:

  HEADER = {
      'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
      'accept': '*/*',
      'accept-encoding': 'gzip, deflate, br',
    }
  def __init__(self, page) -> None:
    self.url = page
    self.img_arr = []

    if self.url[-1] == "/":
      self.url = self.url[:-1]

    self.post = self.url.split("/")[-1]
    self.img_dir = "images/" + self.post

    if not self.create_dirs():
      return

    r = requests.get(page, headers=self.HEADER)

    if r.status_code != 200:
      print("Failed to get that blog post son")
      print(r)
      return

    soup = BeautifulSoup(r.text, 'html.parser')
 
    images = soup.findAll('img')

    if len(images) > 0:
      self.img_arr = self.download_images(images)

  def download_images(self, images):

    ret = []

    for i, image in enumerate(images):
      
      image_link = None
      image_name = None

      try:
        image_link = image.get("src")
        image_name = image_link.split("/")[-1]

      except Exception as e:
        print(e)
        return

      img_path = self.img_dir + "/" + image_name
      
      if os.path.exists(img_path):
        print(img_path + " exists, skipping")
        ret.append(img_path)
        continue

      try:
        print("Saving " + image_name + " to " + img_path)
        r = requests.get(image_link, headers=self.HEADER).content
        try:

          # possibility of decode
          r = str(r, 'utf-8')

        except UnicodeDecodeError:
          with open(img_path, "wb+") as f:
              f.write(r)
          ret.append(img_path)
      except:
        pass
    
    return ret

  def create_dirs(self):
    # path = "images/" + post

    if os.path.exists(self.img_dir):
      return True

    try:
      os.makedirs(self.img_dir)
    except Exception as e:
      print(e)
      return False

    if os.path.exists(self.img_dir):
      return True

    return False



