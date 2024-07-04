from random import choice


def cls():
  return print("\x1bc\x1b[3J", end="")

class Blackjack:

  def __init__(self):
    self.original_deck = {
        "A": 4,
        "2": 4,
        "3": 4,
        "4": 4,
        "5": 4,
        "6": 4,
        "7": 4,
        "8": 4,
        "9": 4,
        "10": 4,
        "J": 4,
        "Q": 4,
        "K": 4
    }
    self.deck = {k: v for k, v in self.original_deck.items() if v != 0}
    self.player_hand = []
    self.dealer_hand = []

  def draw_card(self):
    return choice(list(self.deck.keys()))

  def draw_hand(self, hand):
    hand.append(self.draw_card())
    hand.append(self.draw_card())

  def get_hand_value(self, hand):
    hand_value = 0
    aces = 0

    for card in hand:
      if card in ["J", "Q", "K"]:
        hand_value += 10
      elif card == "A":
        aces += 1
        hand_value += 11
      else:
        hand_value += int(card)

      while hand_value > 21 and aces:
        hand_value -= 10
        aces -= 1

    return hand_value

  def show_player_hand(self):
    print(f"Your hand: {self.player_hand}")

  def show_dealer_hand(self):
    print(f"Dealer's hand: {self.dealer_hand[0]}, ?")

  def check_game_result(self):
    player_hand_value = self.get_hand_value(self.player_hand)
    dealer_hand_value = self.get_hand_value(self.dealer_hand)

    if player_hand_value > 21:
      print(
          f"Score: {player_hand_value} x {dealer_hand_value}\nYou busted! Dealer wins."
      )
    elif player_hand_value > dealer_hand_value:
      print(f"Score: {player_hand_value} x {dealer_hand_value}\nYou win!")
    elif player_hand_value == dealer_hand_value:
      print(f"Score: {player_hand_value} x {dealer_hand_value}\nIt's a draw.")
    else:
      print(f"Score: {player_hand_value} x {dealer_hand_value}\nDealer wins.")

  def play(self):
    self.draw_hand(self.player_hand)
    self.draw_hand(self.dealer_hand)
    call_it = False
    while self.get_hand_value(self.player_hand) <= 21 and not call_it:
      self.show_player_hand()
      self.show_dealer_hand()
      chosen = input("Do you want to hit or call it? (h/c): ")
      cls()
      if chosen.lower() == "h":
        self.player_hand.append(self.draw_card())
      elif chosen.lower() == "c":
        call_it = True
      else:
        print("Invalid choice. Please enter 'h' or 'c'.")
    self.check_game_result()
