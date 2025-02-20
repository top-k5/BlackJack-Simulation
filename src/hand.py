class Hand:
    """
    手札クラス
    """
    def __init__(self):
        self.hand = []
        self.is_soft_hand = False

    def add_card(self, card):
        self.hand.append(card)

    def check_soft_hand(self):
        """
        ソフトハンド（Aを含む手札）かチェックする
        """
        hand_points = [card.point for card in self.hand]
        hand_points.sort()
        if hand_points and hand_points[0] == 1 and sum(hand_points[1:]) < 11:
            self.is_soft_hand = True
        else:
            self.is_soft_hand = False

    def sum_point(self):
        """
        手札のポイント合計（Aを1とした場合と11とした場合）をリストで返す
        """
        self.check_soft_hand()
        hand_points = [card.point for card in self.hand]
        s1 = sum(hand_points)
        if self.is_soft_hand:
            # Aを11としてカウントする場合
            sorted_points = sorted(hand_points)
            s2 = 11 + sum(sorted_points[1:])
            return [s1, s2]
        else:
            return [s1]

    def calc_final_point(self):
        """
        BUSTしていない最終的なポイントを返す
        """
        possible = self.sum_point()
        if max(possible) > 21:
            return min(possible)
        else:
            return max(possible)

    def is_bust(self):
        """
        手札がBUST（どちらのカウントも21を超える）か判定する
        """
        return min(self.sum_point()) > 21

    def deal(self, cards):
        """
        Dealされたカードを手札に加える
        """
        for card in cards:
            self.add_card(card)

    def hit(self, card):
        """
        ヒットでカードを1枚追加する（cardは1枚のカードが入ったリストを想定）
        """
        if isinstance(card, list) and len(card) == 1:
            self.add_card(card[0])
        else:
            print("カードの枚数が正しくありません")
