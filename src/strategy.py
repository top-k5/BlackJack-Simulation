import random
from src.config import INITIAL_BET

def dealer_upcard_value(card):
    """
    ディーラーのアップカード(Cardクラスのインスタンス)を受け取り、
    ベーシックストラテジー用に 1～10 の値に変換して返す。
    Ace(エース)は 1 とする。
    J, Q, K は 10 とする。
    """
    rank = card.rank  # rank は 1(A)～13(K)
    if rank == 1:
        return 1   # Ace
    elif rank >= 10:
        return 10  # 10, J, Q, K
    else:
        return rank
      
class Strategy:
    """

    """

    def select_basic_strategy(self, 
                              player_total, 
                              dealer_up, 
                              is_soft_hand,
                              can_surrender=True, 
                              first_action=True):
        """
        ベーシックストラテジーに基づいて行動を選択する。
        
        Parameters:
        -----------
        player_total : int
            プレイヤー手札の最終的な合計値 (Hand.calc_final_point() などで取得)
        dealer_up : int
            ディーラーのアップカード (1=Ace, 2～10)
        is_soft_hand : bool
            ソフトハンド（Aを11としてカウントできる状態）なら True
        can_surrender : bool
            サレンダー可能かどうか
        first_action : bool
            今回のターンで最初のアクションかどうか（Double Down, Surrender が可能かに影響）
        
        Returns:
        --------
        str
            'h' (Hit), 's' (Stand), 'd' (Double Down), 'r' (Surrender)
        """

        # =======================
        # サレンダー
        # =======================
        # 代表例として:
        #  - ハード 16 vs ディーラー 9,10,A のとき
        #  - ハード 15 vs ディーラー 10 のとき
        # などがよく言われる。詳細はルールにより異なる。
        # ここでは first_action かつ can_surrender=True ならサレンダーを返す。
        if can_surrender and first_action and not is_soft_hand:
            # ハードハンドで 15 vs 10、16 vs 9/10/A
            if player_total == 15 and dealer_up == 10:
                return 'r'
            if player_total == 16 and dealer_up in [9, 10, 1]:
                return 'r'

        # =======================
        # ソフトハンドの処理
        # =======================
        if is_soft_hand:
            # （player_total は Aを11と数えた合計値を想定）
            if player_total <= 14:  # A2, A3 (13,14)
                if dealer_up in [5, 6] and first_action:
                    return 'd'
                else:
                    return 'h'
            elif player_total <= 16:  # A4, A5 (15,16)
                if dealer_up in [4, 5, 6] and first_action:
                    return 'd'
                else:
                    return 'h'
            elif player_total == 17:  # A6
                # ディーラー3～6ならダブル、それ以外はヒット
                if dealer_up in [3, 4, 5, 6] and first_action:
                    return 'd'
                else:
                    return 'h'
            elif player_total == 18:  # A7
                # ディーラー3～6ならダブル、2/7/8はスタンド、9/10/Aはヒット
                if dealer_up in [3, 4, 5, 6] and first_action:
                    return 'd'
                elif dealer_up in [2, 7, 8]:
                    return 's'
                else:
                    return 'h'
            elif player_total >= 19:  # A8, A9
                return 's'
            else:
                return 'error'
            
        # =======================
        # ハードハンドの処理
        # =======================
        else:
            if player_total <= 8:
                # 常にヒット
                return 'h'
            elif player_total == 9:
                # ディーラー3～6ならダブル、他はヒット
                if dealer_up in [3, 4, 5, 6] and first_action:
                    return 'd'
                else:
                    return 'h'
            elif player_total == 10:
                # ディーラー2～9ならダブル、他はヒット
                if dealer_up in range(2, 10) and first_action:
                    return 'd'
                else:
                    return 'h'
            elif player_total == 11:
                if first_action:
                    return 'd'
                else:
                    return 'h'
            elif player_total == 12:
                if dealer_up in [4, 5, 6]:
                    return 's'
                else:
                    return 'h'
            elif 13 <= player_total <= 16:
                if dealer_up in range(2, 7):
                    return 's'
                else:
                    return 'h'
            else:
                return 's'
            
def get_bet_amount(balance, last_bet, last_judge, bet_strategy):
    """
    引数のベット戦略に応じて次のベット額を返す。
    """
    if bet_strategy == 'mg':
        if last_judge == -1:
            return min(last_bet*2, balance) # 負けたターンの次はベットを2倍にする(残高不足なら全額)
        elif last_judge == 1:
            return INITIAL_BET # 買ったターンの次は初期ベット額
        else:
            return min(last_bet, balance) # 引き分けor初回の場合は前回と同じ額をベットする
           
