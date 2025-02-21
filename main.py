from src.game import Game
from src.config import INITIAL_CHIP, MESSAGE_ON
import matplotlib.pyplot as plt
import numpy as np

def main():
    max_balance_list = [] # 各回の最大残高を格納
    max_balance_time_list = [] # 各回の最大残高時のゲーム回数を格納
    game_time_list = [] # 各回のゲーム回数を格納

    for i in range(1000): 
        game = Game()
        balance_history = [INITIAL_CHIP]
        while game.game_mode == 1:
            game.reset_game()   # 各種リセット
            game.bet()   # 賭け金を設定
            game.deal()         # カードを配る
            game.player_turn()  # プレイヤーのターン
            game.dealer_turn()  # ディーラーのターン
            game.judge()        # 勝敗判定
            game.pay_chip()     # 精算
            game.check_chip()   # 残高確認
            game.ask_next_game()# 続行確認
            game.check_deck()   # デッキの残枚数確認
            balance_history.append(game.player.chip.balance)

        if MESSAGE_ON:
            print("BlackJackを終了します")
            print(f"{game.game_count}回ゲームをしました")

        max_balance_list.append(max(balance_history))
        max_balance_time_list.append(balance_history.index(max(balance_history)))
        game_time_list.append(len(balance_history))

        if i <= 100: # 最初の100回は残高推移をプロット
        # 折れ線グラフで残高推移をプロット
            plt.plot(balance_history)
            plt.xlabel('Game Count')
            plt.ylabel('Balance')
            plt.title('Balance Transition')
            plt.savefig(f'result/balance_history_{i}.jpg')
            plt.close()
    
    # 最大収益率を計算
    max_profit_list = [max_profit / INITIAL_CHIP - 1 for max_profit in max_balance_list]
    
    # 最大収益率の分布をプロット
    plt.hist(max_profit_list, bins=10)
    plt.xlabel('Balance')
    plt.ylabel('Frequency')
    plt.title('Max Balance Distribution (profit ratio)')
    plt.savefig('result/max_balance_hist.jpg')
    plt.close()

    # 最大残高時のゲーム回数の分布をプロット
    plt.hist(max_balance_time_list, bins=10)
    plt.xlabel('Game Count')
    plt.ylabel('Frequency')
    plt.title('Game Count at Max Balance')
    plt.savefig('result/max_balance_time_hist.jpg')
    plt.close()

    # ゲーム回数の分布をプロット
    plt.hist(game_time_list, bins=10)
    plt.xlabel('Game Count')
    plt.ylabel('Frequency')
    plt.title('Game Count Distribution')
    plt.savefig('result/game_time_hist.jpg')
    plt.close()

    # 利確ポイントを分析
    for profit in np.arange(0.1, 3.0, 0.2): # 収益率0.1 ~ 3.0で利確する場合
        # 最大残高の収益率がprofitを超える割合
        max_profit_list = [max_profit / INITIAL_CHIP - 1 for max_profit in max_balance_list]
        ratio = len([i for i in max_profit_list if i > profit]) / len(max_profit_list)
        print(f"収益率{profit:3.0%}以上の割合: {ratio:3.0%}")

if __name__ == '__main__':
    main()
