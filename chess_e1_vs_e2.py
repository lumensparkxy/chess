import chess
import datetime
import time
import chess.engine
import chess.pgn
import chess.svg

import logging

logging.basicConfig(filename="chess.log", level=logging.INFO,format='%(asctime)s %(levelname)8s: %(message)s',datefmt='%Y-%m-%d %H:%M:%S')

sf    = '/usr/games/stockfish'
drofa = '/home/pi/chess/Drofa/Drofa_dev'
lc0   = '/home/pi/chess/lc0/build/release/lc0'

LIMIT = 1
TOTAL_GAMES = 1

def write_pgn(board, file_name, player_1, player_2, round, limit):
    import chess.pgn

    game = chess.pgn.Game()
    game.add_line(board.move_stack)

    game.headers["Event"] = "chess engines playing with limit: " + str(limit)
    game.headers["Site"] = "raspberry Pi4"
    game.headers["Date"] = datetime.datetime.now().strftime("%Y.%m.%d")
    game.headers["Round"] = round
    game.headers["White"] = player_1
    game.headers["Black"] = player_2
    game.headers["Result"] = board.result()

    f = open(file_name, mode="a")
    f.write("\n\n")
    f.write(str(game))
    return 0


def play_definite_game(player_1, player_2, limit, file_name):
    board = chess.Board()
    total_draws = -1

    while board.result() in ["1/2-1/2", "*"]:

        board = chess.Board()
        white = chess.engine.SimpleEngine.popen_uci(player_1)
        black = chess.engine.SimpleEngine.popen_uci(player_2)

        while not board.is_game_over():
            if board.turn:
                result = white.play(board, chess.engine.Limit(time=limit))
            else:
                result = black.play(board, chess.engine.Limit(time=limit))
            board.push(result.move)
            output = str(result.move)+ '    '  + str(board.fen())
            logging.info(output)
        total_draws += 1
        white.quit()
        black.quit()
    logging.info("total draw games played " + str(total_draws))
    return board


file_name = "chess_games_" + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".pgn"
for i in range(TOTAL_GAMES):
    logging.info("Game " + str(i + 1) + " of " + str(TOTAL_GAMES) + " is being played")
    board = play_definite_game(lc0,sf, LIMIT, file_name)
    write_pgn(board, file_name,'LEELA', "STOCKFISH", i + 1, LIMIT)
