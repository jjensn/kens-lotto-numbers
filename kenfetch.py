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
      self.download_images(images)

  def download_images(self, images):
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
      except:
        pass

      
        
        

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

    #   # image downloading start
    #   download_images(images, folder_name)
 

  
 
# # DOWNLOAD ALL IMAGES FROM THAT URL
# def download_images(images, folder_name):
   
#     # initial count is zero
#     count = 0
 
#     # print total images found in URL
#     print(f"Total {len(images)} Image Found!")
 
#     # checking if images is not zero
#     if len(images) != 0:
#         for i, image in enumerate(images):
#             # From image tag ,Fetch image Source URL
 
#                         # 1.data-srcset
#                         # 2.data-src
#                         # 3.data-fallback-src
#                         # 4.src
 
#             # Here we will use exception handling
 
#             # first we will search for "data-srcset" in img tag
#             try:
#                 # In image tag ,searching for "data-srcset"
#                 image_link = image["data-srcset"]
                 
#             # then we will search for "data-src" in img
#             # tag and so on..
#             except:
#                 try:
#                     # In image tag ,searching for "data-src"
#                     image_link = image["data-src"]
#                 except:
#                     try:
#                         # In image tag ,searching for "data-fallback-src"
#                         image_link = image["data-fallback-src"]
#                     except:
#                         try:
#                             # In image tag ,searching for "src"
#                             image_link = image["src"]
 
#                         # if no Source URL found
#                         except:
#                             pass
 
#             # After getting Image Source URL
#             # We will try to get the content of image
#             try:
#                 r = requests.get(image_link).content
#                 try:
 
#                     # possibility of decode
#                     r = str(r, 'utf-8')
 
#                 except UnicodeDecodeError:
 
#                     # After checking above condition, Image Download start
#                     with open(f"{folder_name}/images{i+1}.jpg", "wb+") as f:
#                         f.write(r)
 
#                     # counting number of image downloaded
#                     count += 1
#             except:
#                 pass
 
#         # There might be possible, that all
#         # images not download
#         # if all images download
#         if count == len(images):
#             print("All Images Downloaded!")
             
#         # if all images not download
#         else:
#             print(f"Total {count} Images Downloaded Out of {len(images)}")
 
# # MAIN FUNCTION START
# def main(url):
   
#     # content of URL
#     r = requests.get(url)
 
#     # Parse HTML Code
#     soup = BeautifulSoup(r.text, 'html.parser')
 
#     # find all images in URL
#     images = soup.findAll('img')
 
#     # Call folder create function
#     folder_create(images)
 
 
# # take url
# url = input("Enter URL:- ")
 
# # CALL MAIN FUNCTION
# main(url)

pool = KensLottoPool("https://kenslottopool.com/ticketpicturesnov7/")

