from random import choice,uniform
import keyboard

class Deck:
    def __init__(self):
        self.cards = [
            {"face": "A", "value": 11},
            {"face": "2", "value": 2},
            {"face": "3", "value": 3},
            {"face": "4", "value": 4},
            {"face": "5", "value": 5},
            {"face": "6", "value": 6},
            {"face": "7", "value": 7},
            {"face": "8", "value": 8},
            {"face": "9", "value": 9},
            {"face": "10", "value": 10},
            {"face": "J", "value": 10},
            {"face": "Q", "value": 10},
            {"face": "K", "value": 10}
        ]
        self.quantity = 4
        self.build_deck()

    def build_deck(self):
        self.deck = []
        for card in self.cards:
            self.deck.extend([card] * self.quantity)

    def draw_card(self):
        if not self.deck:
            raise ValueError("No more cards in the deck.")
        
        card = choice(self.deck)
        self.deck.remove(card)
        return card

class AI_Player:
    def __init__(self, deck):
        self.hand = []
        self.sumOfPts = 0
        self.acesCount = 0
        for _ in range(2): self.add_card(deck.draw_card())
        self.risk_level = round(uniform(0.2,0.8),1)

    def add_card(self, card):
        self.hand.append(card)
        self.sumOfPts += card["value"]
        if card["face"] == "A":
            self.acesCount += 1
        self.act_on_aces()

    def act_on_aces(self):
        while self.sumOfPts > 21 and self.acesCount > 0:
            self.sumOfPts -= 10
            self.acesCount -= 1

    def display_hand(self):
        return ", ".join(card["face"] for card in self.hand)

    def should_hit(self,deck,dealer):
        potential_bust_threshold = 21
        current_sum = self.sumOfPts

        beneficial_cards = 0
        total_remaining_cards = sum(deck.deck.count(card) for card in deck.deck)

        if total_remaining_cards == 0:
            return False
        
        for card in deck.deck:
            new_sum = current_sum + card["value"]
            if new_sum <= potential_bust_threshold:
                beneficial_cards += 1

        probability_of_beneficial = beneficial_cards / total_remaining_cards
        
        decision = probability_of_beneficial >= self.risk_level or dealer.sumOfPts > self.sumOfPts
        return decision

class Human_Player:
    def __init__(self, deck):
        self.hand = []
        self.sumOfPts = 0
        self.acesCount = 0
        for _ in range(2): self.add_card(deck.draw_card())
        
    def add_card(self, card):
        self.hand.append(card)
        self.sumOfPts += card["value"]
        if card["face"] == "A":
            self.acesCount += 1
        self.act_on_aces()        
    
    def act_on_aces(self):
        while self.sumOfPts > 21 and self.acesCount > 0:
            self.sumOfPts -= 10
            self.acesCount -= 1        
        
    def display_hand(self):
        return ", ".join(card["face"] for card in self.hand)        
        
def play():
    deck = Deck()
    dealer = AI_Player(deck)
    ai_players = [AI_Player(deck) for _ in range(3)]
    player = Human_Player(deck)

    print(f"\n--- Player 1 ---")
    print("Initial hand:", player.display_hand(), "| Total points:", player.sumOfPts)

    for i, ai_player in enumerate(ai_players):
        print(f"\n--- AI_Player {i + 2} ---")
        print("Initial hand:", ai_player.display_hand(), "| Total points:", ai_player.sumOfPts)

    print(f"\n--- Dealer ---")
    print("Initial hand:", dealer.display_hand(), "| Total points:", dealer.sumOfPts)

    for round in range(1, 6):
        print(f"\n--- Round {round} ---")
        all_stood = True
        
        if player.sumOfPts <= 21:
            while True:
                print("\nPress 'SPACE' to hit and 'ESC' to stand\n")
                keyboard.read_key()
                if keyboard.is_pressed('space'):
                    all_stood = False
                    print(f"\n--- Player 1 decides to hit ---")
                    card = deck.draw_card()
                    player.add_card(card)
                    print(f"Player 1 drew:", card["face"])
                    print("Current hand:", player.display_hand(), "| Total points:", player.sumOfPts)
                    
                    if player.sumOfPts > 21:
                        print(f"Player 1 busts! Total points:", player.sumOfPts)
                    break
                elif keyboard.is_pressed('esc'):
                    print(f"\n--- Player 1 decides to stand ---")
                    break
        else:
            print(f"\n--- Player 1 is already bust and cannot play. ---")        
        
        for i, ai_player in enumerate(ai_players):
            if ai_player.sumOfPts <= 21:
                if ai_player.should_hit(deck,dealer):
                    all_stood = False
                    print(f"\n--- AI_Player {i + 2} decides to hit ---")
                    card = deck.draw_card()
                    ai_player.add_card(card)
                    print(f"AI_Player {i + 2} drew:", card["face"])
                    print("Current hand:", ai_player.display_hand(), "| Total points:", ai_player.sumOfPts)
                    
                    if ai_player.sumOfPts > 21:
                        print(f"AI_Player {i + 2} busts! Total points:", ai_player.sumOfPts)
                else:
                    print(f"\n--- AI_Player {i + 2} decides to stand ---")
            else:
                print(f"\n--- AI_Player {i + 2} is already bust and cannot play. ---")

        if not all_stood:
            if dealer.sumOfPts > 21:
                print(f"\n--- Dealer is already bust and cannot play. ---")
            elif dealer.sumOfPts >= 17:
                print(f"\n--- Dealer stands ---")
            else:
                card = deck.draw_card()
                dealer.add_card(card)
                print(f"\n--- Dealer hits ---")
                print("Dealer drew:", card["face"])
                print("Dealer's current hand:", dealer.display_hand(), "| Total points:", dealer.sumOfPts)
        else:
            print("\n--- Final Hands ---")
            print(f"Player 1: Final hand: {player.display_hand()}, Total points: {player.sumOfPts}")
            for i, ai_player in enumerate(ai_players):
                print(f"AI_Player {i + 1}: Final hand: {ai_player.display_hand()}, Total points: {ai_player.sumOfPts}")
                
            print("Dealer: Final hand:", dealer.display_hand(), "| Total points:", dealer.sumOfPts)

            print("\n--- Results ---")
            dealer_bust = dealer.sumOfPts > 21
            if player.sumOfPts <= 21:
                if dealer_bust:
                    print(f"Player 1 wins! Dealer busts.")
                elif player.sumOfPts > dealer.sumOfPts:
                    print(f"Player 1 wins! Total points: {player.sumOfPts} vs Dealer's {dealer.sumOfPts}.")
                elif player.sumOfPts < dealer.sumOfPts:
                    print(f"Player 1 loses. Total points: {player.sumOfPts} vs Dealer's {dealer.sumOfPts}.")
                else:
                    print(f"Player 1 ties with the dealer. Total points: {player.sumOfPts}.")
            else:
                print(f"Player 1 busts and cannot win.")
                
            for i, ai_player in enumerate(ai_players):
                if ai_player.sumOfPts <= 21:
                    if dealer_bust:
                        print(f"AI_Player {i + 1} wins! Dealer busts.")
                    elif ai_player.sumOfPts > dealer.sumOfPts:
                        print(f"AI_Player {i + 1} wins! Total points: {ai_player.sumOfPts} vs Dealer's {dealer.sumOfPts}.")
                    elif ai_player.sumOfPts < dealer.sumOfPts:
                        print(f"AI_Player {i + 1} loses. Total points: {ai_player.sumOfPts} vs Dealer's {dealer.sumOfPts}.")
                    else:
                        print(f"AI_Player {i + 1} ties with the dealer. Total points: {ai_player.sumOfPts}.")
                else:
                    print(f"AI_Player {i + 1} busts and cannot win.")
            break
    
play()