from src.hand import Hand
from src.config import INITIAL_CHIP, IS_HUMAN

class Chip:
    """
    チップ管理クラス
    """
    def __init__(self, initial_chip=INITIAL_CHIP):
        self.balance = initial_chip
        self.bet = 0

    def bet_chip(self, bet):
        """
        ベット額を賭け、残高から減算する
        """
        self.balance -= bet
        self.bet = bet

    def pay_chip_win(self):
        """
        勝利時、ベット額の2倍を支払う
        """
        self.balance += self.bet * 2

    def pay_chip_blackjack(self):
        """
        ブラックジャック時、ベット額の2.5倍を支払う
        """
        self.balance += int(self.bet * 2.5)


    def pay_chip_lose(self):
        """
        敗北時は特に処理をしない
        """
        pass

    def pay_chip_push(self):
        """
        引き分け時、ベット額を返す
        """
        self.balance += self.bet


class Player:
    """
    プレイヤークラス
    """
    def __init__(self, initial_chip=INITIAL_CHIP):
        self.hand = Hand()
        self.chip = Chip(initial_chip)
        self.done = False         # ターン終了フラグ
        self.hit_flag = False     # 既にヒットしたかどうか
        self.is_human = IS_HUMAN      # True: 人間プレイヤー, False: 自動プレイヤー

    def init_player(self):
        self.hand = Hand()
        self.done = False
        self.hit_flag = False

    def deal(self, cards):
        self.hand.deal(cards)

    def hit(self, card):
        self.hand.hit(card)
        self.hit_flag = True

    def stand(self):
        self.done = True

    def double_down(self, card):
        self.chip.balance -= self.chip.bet
        self.chip.bet *= 2
        self.hand.hit(card)
        self.done = True  # ダブルダウン後は1回しかヒットできない

    def surrender(self):
        self.chip.bet = self.chip.bet // 2
        self.chip.balance += self.chip.bet
        self.done = True

    def insurance(self):
        # 未実装
        pass

    def split(self):
        # 未実装
        pass


class Dealer:
    """
    ディーラークラス
    """
    def __init__(self):
        self.hand = Hand()

    def init_dealer(self):
        self.hand = Hand()

    def deal(self, cards):
        self.hand.deal(cards)

    def hit(self, card):
        self.hand.hit(card)
