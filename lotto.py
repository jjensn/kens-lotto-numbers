
from pbticket import PBLottoTicket
from matcher import TemplateMatch
from kenfetch import KensLottoPool

pool = KensLottoPool("https://kenslottopool.com/ticketpicturesnov7/")

for p in pool.img_arr:

  image_search = TemplateMatch(p, './images/template_pb.png')

  image_search.find_powerball_logos()

  image_search.adjust_ticket_rectangles()

  tickets = []

  for v in image_search.logo_locations:
    i = v.crop_image(image_search.tickets.original_image)
    t = PBLottoTicket(i)
    t.extract_numbers()

    tickets.append(t)
