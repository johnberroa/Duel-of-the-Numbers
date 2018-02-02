from game import Mod5Game, QuantumMod5Game


def main():
    game = Mod5Game(n_players=2)
    another_game = True
    while another_game:
        another_game = game.play()


if __name__ == '__main__':
    main()
