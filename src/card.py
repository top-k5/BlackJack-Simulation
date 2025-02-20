class Card:
    """
    カードクラス
    数字: A, 2～10, J, Q, K
    スート: ♠, ♥, ♦, ♣
    """
    SUITS = '♠♥♦♣'
    RANKS = range(1, 14)
    SYMBOLS = ("A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K")
    POINTS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.index = suit + self.SYMBOLS[rank - 1]
        self.point = self.POINTS[rank - 1]

    def __repr__(self):
        return self.index
