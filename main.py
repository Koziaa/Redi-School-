import telebot
from telebot import types

bot = telebot.TeleBot()


games = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Welcome to Tic-Tac-Toe game! To start a new game, enter /play.")

@bot.message_handler(commands=['play'])
def play(message):
    chat_id = message.chat.id
    if chat_id not in games or games[chat_id]['status'] == 'ended':
        games[chat_id] = {'status': 'playing', 'board': [' '] * 9, 'current_player': 'X'}
        show_board(chat_id)
    else:
        bot.send_message(chat_id, "The game is already in progress. Finish the current one to start a new game.")

@bot.message_handler(func=lambda message: True)
def handle_move(message):
    chat_id = message.chat.id
    if chat_id in games and games[chat_id]['status'] == 'playing':
        try:
            move = int(message.text)
            if 1 <= move <= 9 and games[chat_id]['board'][move - 1] == ' ':
                make_move(chat_id, move)
            else:
                bot.send_message(chat_id, "Invalid move. Please try again.")
        except ValueError:
            bot.send_message(chat_id, "Enter a number from 1 to 9.")
        except Exception as e:
            bot.send_message(chat_id, f"An error occurred: {e}")

def show_board(chat_id):
    board = games[chat_id]['board']
    markup = types.ReplyKeyboardMarkup(row_width=3)
    for i in range(0, 9, 3):
        row = [types.KeyboardButton(str(j + 1)) for j in range(i, i + 3)]
        markup.add(*row)

    board_str = ""
    for i in range(0, 9, 3):
        row = "|".join(['❌' if cell == 'X' else '⭕' if cell == 'O' else str(index + 1) for index, cell in enumerate(board[i:i+3])])
        board_str += f"{row}\n" + "-----\n" if i < 6 else row

    bot.send_message(chat_id, f"{board_str}", reply_markup=markup)

def make_move(chat_id, move):
    games[chat_id]['board'][move - 1] = games[chat_id]['current_player']
    show_board(chat_id)
    if check_winner(games[chat_id]['board'], games[chat_id]['current_player']):
        bot.send_message(chat_id, f"The game is over! Player {games[chat_id]['current_player']} wins!")
        games[chat_id]['status'] = 'ended'
    elif ' ' not in games[chat_id]['board']:
        bot.send_message(chat_id, "The game is over! It's a draw.")
        games[chat_id]['status'] = 'ended'
    else:
        games[chat_id]['current_player'] = 'O' if games[chat_id]['current_player'] == 'X' else 'X'
        bot.send_message(chat_id, f"Player {games[chat_id]['current_player']}'s turn.")

def check_winner(board, player):
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # horizontal lines
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # vertical lines
        [0, 4, 8], [2, 4, 6]              # diagonal lines
    ]
    for combination in winning_combinations:
        if all(board[i] == player for i in combination):
            return True
    return False

if __name__ == "__main__":
    bot.polling(none_stop=True)
