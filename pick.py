class SinglePick:

  def __init__(self, ticket_row: list) -> None:
    self.PB = ticket_row[-1]

    del ticket_row[-1]

    self.numbers = sorted(ticket_row)