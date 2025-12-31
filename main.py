import json
import random

file = open("game_log.txt", "w")
file.close()

with open("odds.json") as f:
    odds_data = json.load(f)

odds = odds_data.get("symbols", odds_data)
bet = odds_data.get("bet", 10)

weights = []
symbols = []
emojis = []
three_of_a_kind_payouts = []
two_of_a_kind_payouts = []

for symbol, info in odds.items():
    symbols.append(symbol)
    emojis.append(info["emoji"])
    weights.append(info["weight"])
    three_of_a_kind_payouts.append(info["payouts"]["three_of_a_kind"])
    two_of_a_kind_payouts.append(info["payouts"]["two_of_a_kind"])

def get_set():
    set = []
    for i in range(3):
        randint = random.randint(1,100)
        num = 0
        count = 0
        while(randint>num):
            num += weights[count]
            if(randint <= num):
                num+=100
            else:
                count+=1
        set.append(count)
    return set

def get_board():
    return [get_set(), get_set(), get_set()]


def get_result(board):
    mid = board[1]
    if (mid[0]==mid[1] and mid[2]==mid[1]):
        return ["Three of a kind", three_of_a_kind_payouts[mid[0]]]
    if (mid[0]==mid[1]):
        return ["Two of a kind", two_of_a_kind_payouts[mid[0]]]
    if (mid[1]==mid[2]):
        return ["Two of a kind", two_of_a_kind_payouts[mid[1]]]
    if (mid[0]==mid[2]):
        return ["Two of a kind", two_of_a_kind_payouts[mid[0]]]
    else:
        return ["Unlucky", 0]

def print_board(board):
    for set in board:
        for element in set:
            print(emojis[element], end="")
        print("")

def keep_playing():
    ans = input("Do you wish to keep playing? (press enter for yes and 1 for no)")
    if (ans == ""):
        return True
    if (ans == "1"):
        return False
    else:
        print("Answer is not clear. Try again.")
        return keep_playing()

balance = 1000
playing = True
print(f"Welcome to the Slot Machine! Each bet is ${bet}, and your starting balance is $100. Good Luck!")

while(playing):
    print("---------------------------------------------------")

    if(balance < bet):
        print("Insufficient funds")
        print("Thanks for playing! Final Balance: $", balance, sep = '')
        break

    print("Current Balance: $", balance, sep = '')
    balance -= bet
    print("---------------------------------------------------")

    board = get_board()
    print_board(board)
    result = get_result(board)

    print(result[0], "!", sep = '')
    if(result[1]<0):
        print("No Win!")
    else:
        print("You Win: $", result[1], sep = '')

    balance += result[1]
    print("New Balance: $", balance, sep = '')

    file = open("game_log.txt", "a")
    file.write("Earnings:"+ str(result[1]) + " Balance:" + str(balance))
    
    playing = keep_playing()
    print("---------------------------------------------------")

f.close()
file.close()