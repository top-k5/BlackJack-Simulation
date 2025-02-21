from src.game import Game

def main():
    game = Game()
    while game.game_mode == 1:
        game.reset_game()   # 各種リセット
        game.bet(bet=100)   # 賭け金を設定
        game.deal()         # カードを配る
        game.player_turn()  # プレイヤーのターン
        game.dealer_turn()  # ディーラーのターン
        game.judge()        # 勝敗判定
        game.pay_chip()     # 精算
        game.check_chip()   # 残高確認
        game.ask_next_game()# 続行確認
        game.check_deck()   # デッキの残枚数確認

    print("BlackJackを終了します")
    print(f"{game.game_count}回ゲームをしました")

if __name__ == '__main__':
    main()
