from src.game import Game
from src.config import INITIAL_CHIP
import matplotlib.pyplot as plt

def main():
    global temp_debug
    temp_debug = False
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

    print("BlackJackを終了します")
    print(f"{game.game_count}回ゲームをしました")
    print(balance_history)
    
    # 折れ線グラフで残高推移をプロット
    plt.plot(balance_history)
    plt.xlabel('Game Count')
    plt.ylabel('Balance')
    plt.title('Balance Transition')
    plt.savefig('result/balance_history.jpg')
    plt.close()

if __name__ == '__main__':
    main()
