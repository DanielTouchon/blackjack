from game import Blackjack
from login import login_loop

def main():
    blackjack = Blackjack()
    login_loop()
    blackjack.play()

main()