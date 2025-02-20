from deck import Deck
from player import Player, Dealer
from strategy import Strategy, dealer_upcard_value
from config import INITIAL_CHIP, MINIMUM_BET, NUM_PLAYER

class Game:
    def __init__(self):
        self.game_mode = 0   # 0: 開始待ち, 1: ゲーム中, 2: ゲーム終了
        self.deck = Deck()
        self.player = Player(INITIAL_CHIP)
        self.dealer = Dealer()
        self.judgment = 0    # 勝敗判定（1: 勝ち, -1: 負け, 0: 引分）
        self.game_count = 0
        self.message_on = True  # コンソールにメッセージを表示するか否か
        self.start()

    def start(self):
        self.deck.shuffle()
        self.game_mode = 1
        self.player = Player(INITIAL_CHIP)
        self.dealer = Dealer()
        self.game_count = 0

    def reset_game(self):
        self.player.init_player()
        self.dealer.init_dealer()
        self.game_count += 1

    def bet(self, bet):
        self.player.chip.bet_chip(bet)
        if self.message_on:
            print(f"${self.player.chip.bet} 賭けました")
            print(f"残りは ${self.player.chip.balance}")

    def deal(self, n=2):
        # プレイヤーにカードを配る
        cards = self.deck.draw(n)
        self.player.deal(cards)
        # ディーラーにカードを配る
        cards = self.deck.draw(n)
        self.dealer.deal(cards)
        self.judgment = 0
        self.player.done = False
        self.show_card()

    def player_turn(self):
        if self.player.hand.calc_final_point() == 21:
            self.player.done = True

        while not self.player.done and not self.player.hand.is_bust():
            if self.player.is_human:
                action = input("Hit(h) or Stand(s) or Double down(d) or Surrender(r): ")
            else:
                # ベーシックストラテジー
                action = Strategy().select_basic_strategy(player_total = player.hand.calc_final_point(), 
                                                          dealer_up = dealer_upcard_value(self.dealer.hand.hand[0]),　 
                                                          is_soft_hand = self.player.hand.is_soft_hand,
                                                          can_surrender=True, 
                                                          first_action = (len(self.player.hand.hand) == 2 and not self.player.hit_flag)
                                                         )
            self.player_step(action)

    def player_step(self, action):
        if action == 'h':  # Hit
            card = self.deck.draw(1)
            self.player.hit(card)
            self.show_card()
            if self.player.hand.calc_final_point() == 21:
                self.player.done = True
            if self.player.hand.is_bust():
                self.player.done = True
                self.judgment = -1
                if self.message_on:
                    print("Player BUST")
        elif action == 's':  # Stand
            self.player.stand()
        elif action == 'd' and not self.player.hit_flag:  # Double down（初回のみ許可）
            card = self.deck.draw(1)
            if self.player.chip.balance >= self.player.chip.bet:
                self.player.double_down(card)
                self.show_card()
                if self.message_on:
                    print("Double down が選択されました．掛け金を倍にしました")
                    print(f"残りは ${self.player.chip.balance}")
                if self.player.hand.is_bust():
                    self.player.done = True
                    self.judgment = -1
                    if self.message_on:
                        print("Player BUST")
            else:
                print("チップが足りないためHitします")
                self.player.hit(card)
                self.show_card()
                if self.player.hand.calc_final_point() == 21:
                    self.player.done = True
                if self.player.hand.is_bust():
                    self.player.done = True
                    self.judgment = -1
                    if self.message_on:
                        print("Player BUST")
        elif action == 'r' and not self.player.hit_flag:  # Surrender（初回のみ許可）
            self.player.surrender()
            self.judgment = -1
            if self.message_on:
                print("Surrender が選択されました")
        else:
            if self.message_on:
                print("正しい選択肢を選んでください")

    def show_card(self):
        if self.message_on:
            print("Playerのターン")
            print(f"Player : {self.player.hand.hand} = {self.player.hand.sum_point()} , soft card : {self.player.hand.is_soft_hand}")
            # ディーラーは1枚のみ表示
            print(f"Dealer : {self.dealer.hand.hand[0]}, ?")

    def dealer_turn(self):
        if self.judgment == -1:
            return
        self.open_dealer()
        while self.dealer.hand.calc_final_point() < 17 and self.judgment == 0:
            card = self.deck.draw(1)
            self.dealer.hit(card)
            self.open_dealer()
        if self.dealer.hand.calc_final_point() > 21:
            self.judgment = 1
            if self.message_on:
                print("Dealer BUST")

    def open_dealer(self):
        if self.message_on:
            print("Dealerのターン")
            print(f"Player : {self.player.hand.hand} = {self.player.hand.calc_final_point()}")
            print(f"Dealer : {self.dealer.hand.hand} = {self.dealer.hand.calc_final_point()}")

    def judge(self):
        if self.judgment == 0:
            if self.player.hand.calc_final_point() > self.dealer.hand.calc_final_point():
                self.judgment = 1
            elif self.player.hand.calc_final_point() < self.dealer.hand.calc_final_point():
                self.judgment = -1
            else:
                self.judgment = 0

        if self.message_on:
            self.show_judgement()

    def show_judgement(self):
        if self.message_on:
            print("")
            if self.judgment == 1:
                print("Playerの勝ち")
            elif self.judgment == -1:
                print("Playerの負け")
            elif self.judgment == 0:
                print("引き分け")
            print("")

    def pay_chip(self):
        previous_chip = self.player.chip.balance
        if self.judgment == 1:  # 勝ちの場合
            self.player.chip.pay_chip_win()
        elif self.judgment == -1:  # 負けの場合
            self.player.chip.pay_chip_lose()
        elif self.judgment == 0:  # 引き分けの場合
            self.player.chip.pay_chip_push()
        if self.message_on:
            print(f"Playerの所持チップは ${self.player.chip.balance}")
        reward = self.player.chip.balance - previous_chip
        return reward

    def check_chip(self):
        if self.player.chip.balance < MINIMUM_BET:
            self.game_mode = 2
            if self.message_on:
                print("チップがMinimum Betを下回ったのでゲームを終了します")

    def ask_next_game(self):
        if self.player.is_human:
            while self.game_mode == 1:
                player_input = input("続けますか？ y/n: ")
                if player_input == 'y':
                    break
                elif player_input == 'n':
                    self.game_mode = 2
                    break
                else:
                    print("y/nを入力してください")
        print(f"残りカード枚数は {self.deck.count_cards()}")
        print("")

    def check_deck(self):
        if self.deck.count_cards() < NUM_PLAYER * 10 + 5:
            from deck import Deck
            self.deck = Deck()
            if self.message_on:
                print("デッキを初期化しました")
                print(f"残りカード枚数は {self.deck.count_cards()}")
                print("")
