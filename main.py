import random
import sys


def header():
    print("=" * 70)


def is_it_draw(stock, main_snake, computer_hand, player_hand):
    if len(stock) == 0:
        for i in player_hand:
            if main_snake[0][0] in i or main_snake[-1][-1] in i:
                return True
        for i in computer_hand:
            if main_snake[0][0] in i or main_snake[-1][-1] in i:
                return True
        return False


def interface(stock, computer_hand, player_hand, snake, status):
    header()
    print("Stock size: ", len(stock))
    print("Computer pieces: {} \n".format(len(computer_hand)))
    if len(snake) >= 6:
        print("{}{}{}...{}{}{}".format(snake[0], snake[1], snake[2], snake[-3], snake[-2],
                                       snake[-1]))
    else:
        print(*snake)
    print(" ")
    print("Your pieces: ")
    for i in player_hand:
        print("{}:{}".format(player_hand.index(i) + 1, i))
    print("\n")
    if is_it_draw(stock, computer_hand, player_hand, snake):
        print("The game is over. It's a draw!")
        sys.exit(0)
    if status == "player":
        print("Status: It's your turn to make a move. Enter your command.")
    elif status == "computer":
        print("Status: Computer is about to make a move. Press Enter to continue...")


def shuffle_distribute_pieces():
    while True:
        domino = []
        player = []
        computer = []

        for i in range(7):
            for j in range(7):
                if i < j:
                    continue
                domino.append([i, j])
        for _ in range(7):
            player_choice = domino.pop(domino.index(random.choice(domino)))
            player.append(player_choice)
            computer_choice = domino.pop(domino.index(random.choice(domino)))
            computer.append(computer_choice)
        who_first = " "
        first_piece = []
        for i in range(7):
            if [7 - i, 7 - i] in player:
                first_piece = [player.pop(player.index([7 - i, 7 - i]))]
                who_first = "computer"
                break
            elif [7 - i, 7 - i] in computer:
                first_piece = [computer.pop(computer.index([7 - i, 7 - i]))]
                who_first = "player"
                break
        if who_first == "player" or who_first == "computer":
            break

    return domino, computer, player, first_piece, who_first


def player_turn(stock, player_hand, main_snake):
    while True:
        try:
            user_command = input()
            if user_command == "0":
                player_hand.append(stock.pop(stock.index(random.choice(stock))))
                break
            elif user_command[0] == "-":
                try:
                    if player_hand[int(user_command[1:]) - 1][1] == main_snake[0][0]:
                        main_snake.insert(0, player_hand.pop(int(user_command[1:]) - 1))
                        break
                    elif player_hand[int(user_command[1:]) - 1][0] == main_snake[0][0]:
                        main_snake.insert(0, player_hand[int(user_command[1:]) - 1][::-1])
                        player_hand.pop(int(user_command[1:]) - 1)
                        break
                    else:
                        print("Illegal move. Please try again.")
                except IndexError:
                    print("Invalid input. Please try again.")
            elif user_command[0] != "-":
                try:
                    if player_hand[int(user_command[0:]) - 1][0] == main_snake[-1][1]:
                        main_snake.append(player_hand.pop(int(user_command[0:]) - 1))
                        break
                    elif player_hand[int(user_command[0:]) - 1][1] == main_snake[-1][1]:
                        main_snake.append(player_hand[int(user_command[0:]) - 1][::-1])
                        player_hand.pop(int(user_command[0:]) - 1)
                        break
                    else:
                        print("Illegal move. Please try again.")
                except IndexError:
                    print("Invalid input. Please try again.")
            else:
                print("Invalid input. Please try again.")
        except IndexError:
            print("Invalid input. Please try again.")
        except ValueError:
            print("Invalid input. Please try again.")


def computer_turn(stock, computer_hand, main_snake):

    number_values = counting_numbers_rarity(main_snake, computer_hand)
    piece_rarity = counting_piece_rarity(computer_hand, number_values)

    for _ in range(len(piece_rarity)):
        playing_piece = computer_hand[int(piece_rarity.index(max(piece_rarity)))]
        if playing_piece[0] == main_snake[-1][1]:
            main_snake.append(playing_piece)
            computer_hand.pop(int(piece_rarity.index(max(piece_rarity))))
            return None
        elif playing_piece[1] == main_snake[0][0]:
            main_snake.insert(0, computer_hand.pop(int(piece_rarity.index(max(piece_rarity)))))
            return None
        elif playing_piece[0] == main_snake[0][0]:
            main_snake.insert(0, playing_piece[::-1])
            computer_hand.pop(int(piece_rarity.index(max(piece_rarity))))
            return None
        elif playing_piece[1] == main_snake[-1][1]:
            main_snake.append(playing_piece[::-1])
            computer_hand.pop(int(piece_rarity.index(max(piece_rarity))))
            return None
        piece_rarity[piece_rarity.index(max(piece_rarity))] = -1
    computer_hand.append(stock.pop(stock.index(random.choice(stock))))


def counting_numbers_rarity(main_snake, computer_hand):
    number_values = []
    for n in range(7):
        count = 0
        for i in main_snake + computer_hand:
            if n in i:
                count += 1
        number_values.append(count)
    return number_values


def counting_piece_rarity(computer_hand, number_values):
    piece_rarity = []
    for i in computer_hand:
        piece_rarity.append(number_values[int(i[0])] + number_values[int(i[1])])
    return piece_rarity


def turn(stock, computer_hand, player_hand, main_snake, status):

    interface(stock, computer_hand, player_hand, main_snake, status)

    if status == "player":
        player_turn(stock, player_hand, main_snake)
    else:
        computer_turn(stock, computer_hand, main_snake)
        input()


def game():

    domino_set, computer_set, player_set, domino_snake, status = shuffle_distribute_pieces()

    while True:
        turn(domino_set, computer_set, player_set, domino_snake, status)
        if len(player_set) == 0:
            status = "over"
            interface(domino_set, computer_set, player_set, domino_snake, status)
            print("Status: The game is over. You won!")
            break
        elif len(computer_set) == 0:
            status = "over"
            interface(domino_set, computer_set, player_set, domino_snake, status)
            print("Status: The game is over. The computer won!")
            break
        if status == "player":
            status = "computer"
        else:
            status = "player"


if __name__ == '__main__':
    game()
