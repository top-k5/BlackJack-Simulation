from src.game import Game
from src.config import INITIAL_CHIP, MESSAGE_ON, ITERATION_NUM, BET_STRATEGY, ITITIAL_TIP_LIST, TARGET_PROFIT
import matplotlib.pyplot as plt
import numpy as np
import pickle

# 一定額(=TARGET_PROFIT)を稼ぐために必要な軍資金分析
def main():
    print(f'ゲーム回数: {ITERATION_NUM}')

    # 還元率(総リターン/総ベット)の計算用
    total_return = 0
    total_bet = 0

    # 勝率の計算用
    total_win_count = 0
    total_lose_count = 0
    for initial_chip in ITITIAL_TIP_LIST:
        max_balance_list = [] # 各回の最大残高を格納

        for i in range(ITERATION_NUM): 
            game = Game(initial_chip=initial_chip)
            balance_history = [initial_chip]
            while game.game_mode == 1:
                game.reset_game()   # 各種リセット
                game.bet()   # 賭け金を設定
                game.deal()         # カードを配る
                game.player_turn()  # プレイヤーのターン
                game.dealer_turn()  # ディーラーのターン
                game.judge()        # 勝敗判定
                total_bet += game.player.chip.bet # 通算ベット
                total_return += game.pay_chip() # 精算
                game.check_chip()   # 残高確認
                game.ask_next_game()# 続行確認
                game.check_deck()   # デッキの残枚数確認
                balance_history.append(game.player.chip.balance)

            if MESSAGE_ON:
                print("BlackJackを終了します")
                print(f"{game.game_count}回ゲームをしました")
            
            # 勝利数と敗北数をカウント
            total_win_count += game.win_count
            total_lose_count += game.lose_count

            max_balance_list.append(max(balance_history))
        
        # 結果をpickleで保存
        pickle.dump([max_balance_list], open(f'result/result_{BET_STRATEGY}_{ITERATION_NUM}_{initial_chip}.pkl', 'wb'))
            
        # 最大残高が、軍資金+TARGET_PROFITを超える割合
        ratio = len([i for i in max_balance_list if i > initial_chip + TARGET_PROFIT]) / len(max_balance_list)
        print(f"軍資金{initial_chip}で{TARGET_PROFIT}を稼ぐ割合: {ratio:3.0%}")
        with open(f'result/ititial_chip_analysis_{BET_STRATEGY}_{ITERATION_NUM}.txt', 'a') as f:
            f.write(f"軍資金{initial_chip}で{TARGET_PROFIT}を稼ぐ割合: {ratio:3.0%}\n")

    # 還元率(総リターン/総ベット)の計算
    pickle.dump([total_return, total_bet], open(f'result/return_rate_{BET_STRATEGY}_{ITERATION_NUM}.pkl', 'wb'))
    return_rate = total_return / total_bet
    print(f"還元率: {return_rate:3.0%}")

    # 勝率の計算
    pickle.dump([total_win_count, total_lose_count], open(f'result/win_rate_{BET_STRATEGY}_{ITERATION_NUM}.pkl', 'wb'))
    win_rate = total_win_count / (total_win_count + total_lose_count)
    print(f"勝率: {win_rate:3.0%}")



# 利確ポイント分析
# def main():
#     max_balance_list = [] # 各回の最大残高を格納
#     max_balance_time_list = [] # 各回の最大残高時のゲーム回数を格納
#     game_time_list = [] # 各回のゲーム回数を格納

#     print(f'ゲーム回数: {ITERATION_NUM}')
#     for i in range(ITERATION_NUM): 
#         game = Game()
#         balance_history = [INITIAL_CHIP]
#         while game.game_mode == 1:
#             game.reset_game()   # 各種リセット
#             game.bet()   # 賭け金を設定
#             game.deal()         # カードを配る
#             game.player_turn()  # プレイヤーのターン
#             game.dealer_turn()  # ディーラーのターン
#             game.judge()        # 勝敗判定
#             game.pay_chip()     # 精算
#             game.check_chip()   # 残高確認
#             game.ask_next_game()# 続行確認
#             game.check_deck()   # デッキの残枚数確認
#             balance_history.append(game.player.chip.balance)

#         if MESSAGE_ON:
#             print("BlackJackを終了します")
#             print(f"{game.game_count}回ゲームをしました")

#         max_balance_list.append(max(balance_history))
#         max_balance_time_list.append(balance_history.index(max(balance_history)))
#         game_time_list.append(len(balance_history))

#         if i <= 100: # 最初の100回は残高推移をプロット
#         # 折れ線グラフで残高推移をプロット
#             plt.plot(balance_history)
#             plt.xlabel('Game Count')
#             plt.ylabel('Balance')
#             plt.title('Balance Transition')
#             plt.savefig(f'result/balance_history_{BET_STRATEGY}_{i}.jpg')
#             plt.close()
    
#     # 最大収益率を計算
#     max_profit_list = [max_profit / INITIAL_CHIP - 1 for max_profit in max_balance_list]
    
#     # 結果をpickleで保存
#     with open(f'result/result_{BET_STRATEGY}_{ITERATION_NUM}.pkl', 'wb') as f:
#         pickle.dump([max_balance_list, max_balance_time_list, game_time_list, max_profit_list], f)
        
#     # 最大収益率の分布をプロット
#     plt.hist(max_profit_list, range = [1, 8], bins=20)
#     plt.xlabel('Profit Rate')
#     plt.ylabel('Frequency')
#     plt.title('Max Profit Distribution')
#     plt.savefig('result/max_profit_hist_{BET_STRATEGY}.jpg')
#     plt.close()

#     # 最大残高時のゲーム回数の分布をプロット
#     plt.hist(max_balance_time_list, range = [0, 1000], bins=20)
#     plt.xlabel('Game Count')
#     plt.ylabel('Frequency')
#     plt.title('Game Count at Max Balance')
#     plt.savefig('result/max_profit_time_hist_{BET_STRATEGY}.jpg')
#     plt.close()

#     # ゲーム回数の分布をプロット
#     plt.hist(game_time_list, range=[0, 1000], bins=20)
#     plt.xlabel('Game Count')
#     plt.ylabel('Frequency')
#     plt.title('Game Count Distribution')
#     plt.savefig('result/game_time_hist_{BET_STRATEGY}.jpg')
#     plt.close()

#     # 利確ポイントを分析し、txtファイルで出力
#     for profit in np.arange(0.1, 3.0, 0.2): # 収益率0.1 ~ 3.0で利確する場合
#         # 最大残高の収益率がprofitを超える割合
#         max_profit_list = [max_profit / INITIAL_CHIP - 1 for max_profit in max_balance_list]
#         ratio = len([i for i in max_profit_list if i > profit]) / len(max_profit_list)
#         print(f"収益率{profit:3.0%}以上の割合: {ratio:3.0%}")
#         with open(f'result/profit_analysis_{BET_STRATEGY}_{ITERATION_NUM}.txt', 'a') as f:
#             f.write(f"収益率{profit:3.0%}以上の割合: {ratio:3.0%}\n")


if __name__ == '__main__':
    main()
