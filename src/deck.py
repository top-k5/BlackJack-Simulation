import random
from copy import deepcopy
from src.card import Card
from src.config import NUM_DECK

class Deck:
    """
    デッキクラス（複数デッキを含む山札の管理）
    """
    def __init__(self):
        # 1デッキ分のカードリストを作成
        self.cards = [Card(suit, rank) for suit in Card.SUITS for rank in Card.RANKS]
        # 複数デッキの場合はカードリストを複製
        if NUM_DECK > 1:
            temp_cards = deepcopy(self.cards)
            for _ in range(NUM_DECK - 1):
                self.cards.extend(temp_cards)
        random.shuffle(self.cards)

    def draw(self, n=1):
        """
        デッキからn枚のカードを引き、リストで返す
        """
        drawn = self.cards[:n]
        del self.cards[:n]
        return drawn

    def shuffle(self):
        """
        デッキをシャッフルする
        """
        random.shuffle(self.cards)

    def count_cards(self):
        """
        残りのカード枚数を返す
        """
        return len(self.cards)
