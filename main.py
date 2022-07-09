from ai.AI import AI
from controller.ChessGame import ChessGame
from controller.SaveLoad import SaveLoad
from model.Color import Color
from model.GameStatus import GameStatus
from view.ConsoleChessField import ConsoleChessField


def ask_for_input(question, option1='Y', option2='N') -> bool:
    while True:
        x = input(question + ' (' + option1 + '/' + option2 + ')').upper()
        if x == option1:
            return True
        if x == option2:
            return False


class ConsoleGuide:

    def display_piece_art(self):
        print("                                                       .::.")
        print("                                            _()_       _::_")
        print("                                  _O      _/____\_   _/____\_")
        print("           _  _  _     ^^__      / //\    \      /   \      /")
        print("          | || || |   /  - \_   {     }    \____/     \____/")
        print("          |_______| <|    __<    \___/     (____)     (____)")
        print("    _     \__ ___ / <|    \      (___)      |  |       |  |")
        print("   (_)     |___|_|  <|     \      |_|       |__|       |__|")
        print("  (___)    |_|___|  <|______\    /   \     /    \     /    \ ")
        print("  _|_|_    |___|_|   _|____|_   (_____)   (______)   (______)")
        print(" (_____)  (_______) (________) (_______) (________) (________)")
        print(" /_____\  /_______\ /________\ /_______\ /________\ /________\ ")
        print("_________________________________________________________________")
        print("|             Congratulations you                               |")

    def run(self) -> None:

        game_finish = False
        vs_bot = False
        save_load = SaveLoad()

        while not game_finish:
            if save_load.save_exists() and ask_for_input('there is an old game. do you want to load it?'):
                gameboard = save_load.load()
            else:
                vs_bot = ask_for_input('do you want to play against a bot or local against a friend?', 'B', 'F')
                if not vs_bot:
                    console_field = ConsoleChessField(vs_bot)
                    gameboard = ChessGame(console_field)
                else:
                    playercolor = Color.BLACK
                    playercolor_result = ask_for_input('What color do you want to play?', 'W', 'B')
                    if playercolor_result:
                        playercolor = Color.WHITE
                    console_field = ConsoleChessField(vs_bot, playercolor, AI(playercolor.get_other_color()))
                    gameboard = ChessGame(console_field)

            status = gameboard.main()

            if status == GameStatus.SAVE:
                SaveLoad().save(gameboard)
                print('Game is Saved!')
            elif status == GameStatus.QUIT:
                print('Quit!')
            elif status == GameStatus.WON_WHITE or status == GameStatus.WON_BLACK:
                if vs_bot:
                    if (status == GameStatus.WON_WHITE and playercolor == Color.BLACK) or (
                            status == GameStatus.WON_BLACK and playercolor == Color.WHITE):
                        print('The time of man has come to an end.! Human lost')
                    else:
                        self.display_piece_art()
                        print("|                                                               |")
                        print("|                      WIN                                      |")
                        print("|_______________________________________________________________|")

                else:
                    if (status == GameStatus.WON_BLACK and playercolor == Color.BLACK) or (
                            status == GameStatus.WON_WHITE and playercolor == Color.WHITE):
                        self.display_piece_art()
                        if status == GameStatus.WON_WHITE:
                            print("|                   White Player                                |")
                            print("|                      WIN                                      |")
                            print("|_______________________________________________________________|")
                        elif status == GameStatus.WON_BLACK:
                            print("|                   Black Player                                |")
                            print("|                      WIN                                      |")
                            print("|_______________________________________________________________|")
            elif status == GameStatus.DRAW:
                print("Draw!")
            if not ask_for_input('Do you want to start a new game?'):
                print("Finish the game by closing the console. If you want to play again send (Y)")
                game_finish = True


if __name__ == "__main__":
    ConsoleGuide().run()

