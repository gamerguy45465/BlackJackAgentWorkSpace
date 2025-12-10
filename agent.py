import sys
import os
import subprocess
import shutil
import math
import heapq

def Max_Probability(probability: dict, scores, score, card_values):
    m = -math.inf
    s: str = ""


    for card in probability:
        if probability[card] > m and scores[card] + score <= 21 and card_values[card] > 0:
            m = probability[card]
            s = card

    return m, s


def Min_Probability(probability: dict, scores, score, card_values):
    m = math.inf
    s: str = ""


    for card in probability:
        if probability[card] < m and scores[card] + score <= 21 and card_values[card] > 0:
            m = probability[card]
            s = card

    return m, s


def probability(available_cards: dict, total_cards: int) -> list:
    p = []
    for card in available_cards:
        p.append(available_cards[card]/total_cards)

    return p


def Expectimax(score, scores, turn, available_cards, deck, values, probabilities, q = 1.0):
    if(score > 21):
        return q
    if(turn == "Max"):
        temp_deck = deck.copy()
        tempc = available_cards.copy()
        q = max(q, Expectimax(score, scores, "Chance",  available_cards, deck, values, probabilities, q))
        deck = temp_deck.copy()
        available_cards = tempc.copy()


    else:
        p = probability(available_cards, len(deck))

        probs = {}

        for i in range(len(p)):
            if(i == 0):
                probs["Ace"] = p[i]

            elif(i == 10):
                probs["Jack"] = p[i]

            elif(i == 11):
                probs["Queen"] = p[i]

            elif(i == 12):
                probs["King"] = p[i]

            else:
                probs[str(i + 1)] = p[i]

        E_x = 0.0
        index = 1
        for s in probs:
            E_x += index * probs[s]
            index += 1


        q = E_x

        if(score + q > 21):
            return q

        else:
            q = max(q, Expectimax(score + q, scores, "Max", available_cards, deck, values, probabilities, q))


    return q



def Expectiminimax(score, turn, prev, scores, available_cards, deck, values):
    q = 0
    if(score >= 21):
        return score
    if(turn == "Max"):
        temp_deck = deck.copy()
        tempc = available_cards.copy()
        q = Expectiminimax(score, "Chance", "Max", scores, available_cards, deck, values)
        deck = temp_deck.copy()
        available_cards = tempc.copy()


    elif(turn == "Min"):
        temp_deck = deck.copy()
        tempc = available_cards.copy()
        q = Expectiminimax(score, "Chance", "Min", scores, available_cards, deck, values)
        deck = temp_deck.copy()
        available_cards = tempc.copy()

    else:
        p = probability(available_cards, len(deck))

        probs = {}

        for i in range(len(p)):
            if(i == 0):
                probs["Ace"] = p[i]

            elif(i == 10):
                probs["Jack"] = p[i]

            elif(i == 11):
                probs["Queen"] = p[i]

            elif(i == 12):
                probs["King"] = p[i]

            else:
                probs[str(i + 1)] = p[i]




        if(prev == "Max"):
            m, s = Max_Probability(probs, scores, score, available_cards)




            if(s == "Ace"):
                temp_deck = deck.copy()
                tempc = available_cards.copy()
                deck.remove(1)
                available_cards[s] -= 1
                if (score + 11) > 21:
                    q = m
                    Expectiminimax(score + 1, "Min", "Chance", scores, available_cards, deck, values)
                    deck = temp_deck.copy()
                    available_cards = tempc.copy()

                else:
                    q = m
                    Expectiminimax(score + 11, "Min", "Chance", scores, available_cards, deck, values)
                    deck = temp_deck.copy()
                    available_cards = tempc.copy()


            else:
                temp_deck = deck.copy()
                tempc = available_cards.copy()
                deck.remove(values[s])
                available_cards[s] -= 1
                q = m
                Expectiminimax(score + scores[s], "Min", "Chance", scores, available_cards, deck, values)
                deck = temp_deck.copy()
                available_cards = tempc.copy()

        elif(prev == "Min"):
            m, s = Min_Probability(probs, scores, score, available_cards)
            print(m)
            print(s)

            if(m == math.inf):
                return q

            if(s == "Ace"):
                temp_deck = deck.copy()
                tempc = available_cards.copy()
                deck.remove(1)
                available_cards[s] -= 1
                if (score + 11) > 21:
                    q = m * Expectiminimax(score + 1, "Min", "Chance", scores, available_cards, deck, values)
                    deck = temp_deck.copy()
                    available_cards = tempc.copy()

                else:
                    q = m * Expectiminimax(score + 11, "Min", "Chance", scores, available_cards, deck, values)
                    deck = temp_deck.copy()
                    available_cards = tempc.copy()


            else:
                temp_deck = deck.copy()
                tempc = available_cards.copy()
                deck.remove(values[s])
                available_cards[s] -= 1
                q = m * Expectiminimax(score + scores[s], "Min", "Chance", scores, available_cards, deck, values)
                deck = temp_deck.copy()
                available_cards = tempc.copy()



    return q






def Sum_of_Cards(cards):
    sum = 0
    for card in cards:
        print("Card: ", card)
        if card == "Ace":
            if(sum + 11 == 21):
                sum += 11

            else:
                sum += 1

        elif card == "Jack":
            sum += 10

        elif card == "Queen":
            sum += 10

        elif card == "King":
            sum += 10


        else:
            sum += int(card)



    return sum






def run_cmd(cmd, cwd=None):
    print(f"\n>> Running: {' '.join(cmd)}")
    process = subprocess.Popen(cmd, cwd=cwd)
    process.communicate()
    if process.returncode != 0:
        print(f"Command failed: {' '.join(cmd)}")
        sys.exit(process.returncode)

def main():
    # Folder containing this script (your project root)
    project_root = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(project_root, "cmake-build-debug")

    # If build dir contains a stale CMakeCache from Ninja, clear it
    if os.path.exists(build_dir):
        cache_file = os.path.join(build_dir, "CMakeCache.txt")
        if os.path.exists(cache_file):
            with open(cache_file, "r") as f:
                cache = f.read()
            if "Ninja" in cache or "MinGW" in cache:
                print(">> Old generator detected — deleting build directory")
                shutil.rmtree(build_dir)

    # Recreate fresh build dir if missing
    if not os.path.exists(build_dir):
        os.makedirs(build_dir)

    cmake_path = r"C:\Program Files\CMake\bin\cmake.exe"

    # Step 1: Configure — always use Visual Studio generator on Windows
    run_cmd([
        cmake_path,
        "-G", "Visual Studio 17 2022",
        ".."
    ], cwd=build_dir)

    # Step 2: Build
    run_cmd([
        cmake_path,
        "--build", ".",
        "--config", "Debug"
    ], cwd=build_dir)

    # Step 3: Find the executable inside cmake-build-debug/Debug/
    debug_dir = os.path.join(build_dir, "Debug")
    exe_path = None

    if os.path.isdir(debug_dir):
        for f in os.listdir(debug_dir):
            if f.lower().endswith(".exe"):
                exe_path = os.path.join(debug_dir, f)
                break

    if exe_path is None:
        raise FileNotFoundError(
            f"No .exe found inside {debug_dir}. "
            "Did the build succeed?"
        )

    exe_path = os.path.normpath(exe_path)
    print(f">> Executable found: {exe_path}")

    # Step 4: Run the executable (NOTE: does NOT send input yet)
    # This is where you will build your agent − reading output and sending input.
    process = subprocess.Popen(
        [exe_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )

    # Example: read the first line only (you will replace this with your AI loop)
    #first_output = process.stdout.readline()
    #print("Ran Here")
    #print("Program said:", first_output.strip())
    while True:
        deck = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        available_cards = {"Ace": 4, "2": 4, "3": 4, "4": 4, "5": 4, "6": 4, "7": 4, "8": 4, "9": 4, "10": 4, "Jack": 4, "Queen": 4, "King": 4}
        scores = {"Ace": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6":6, "7":7, "8":8, "9":9, "10":10, "Jack":10, "Queen":10, "King":10}
        values = {"Ace": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6":6, "7":7, "8":8, "9":9, "10":10, "Jack":11, "Queen":12, "King":13}
        line = process.stdout.readline()
        if not line:
            break

        print("GAME:", line.strip())
        if(line.strip() == "Play again? (y, n)"):
            process.stdin.write("y\n")

        line = process.stdout.readline()


        if("Place your bets on the table" in line):
            process.stdin.write("100\n")



        line = process.stdout.readline()
        cards = []
        dealer_cards = []

        if "Player got a Blackjack!" in line:
            print("GAME:", line.strip())
            continue


        else:
            print("GAME:", line.strip())
            dealer = False
            while line:
                line = process.stdout.readline()
                if("Hit or Stay?" in line):
                    break
                if("Dealer Cards:" not in line):
                    if(dealer == False):
                        cards.append(line.strip())
                        print("GAME:", line.strip())

                    else:
                        dealer_cards.append(line.strip())
                        print("GAME:", line.strip())

                else:
                    dealer = True

        print("Cards:",cards)
        print("Dealer Cards:",dealer_cards)

        if("Hit or Stay?" in line):
            print("GAME:",line.strip())
            for card in cards:
                available_cards[card] -= 1
                if("Ace" in card):
                    deck.remove(1)

                elif("Jack" in card):
                    deck.remove(11)

                elif("Queen" in card):
                    deck.remove(12)

                elif("King" in card):
                    deck.remove(13)

                else:
                    deck.remove(int(card))

            for card in dealer_cards:
                available_cards[card] -= 1
                if("Ace" in card):
                    deck.remove(1)

                elif("Jack" in card):
                    deck.remove(11)

                elif("Queen" in card):
                    deck.remove(12)

                elif("King" in card):
                    deck.remove(13)

                else:
                    deck.remove(int(card))




        while True:
            temp_cards = available_cards.copy()
            temp_deck = deck.copy()
            probabilities = []
            s_cards = Sum_of_Cards(cards)
            s1 = Expectimax(s_cards, scores, "Max", available_cards, deck, values, probabilities)
            print(probabilities)
            #s1 = Expectiminimax(0, "Max", "Max", scores, available_cards, deck, values)
            available_cards = temp_cards.copy()
            deck = temp_deck.copy()
            print(s1)

            if(s1 + s_cards <= 21):
                process.stdin.write("Hit\n")
                line = process.stdout.readline()
                cards.append(line.strip())
                deck.remove(int(line.strip()))
                available_cards[line.strip()] -= 1
                print("GAME: ", line.strip())
                print(cards)

            else:
                print("Stay")
                process.stdin.write("Stay\n")
                while("Play again? (y, n)" not in line):
                    line = process.stdout.readline()
                    print("GAME: ", line)

                print("GAME: ", line)
                process.stdin.write("y\n")


            line = process.stdout.readline()
            if("Player Busts!" in line):
                print("GAME: ", line.strip())
                break

            while("Score:" not in line.strip()):
                print("GAME: ", line.strip())
                line = process.stdout.readline()


            print("GAME: ", line.strip())



            line = process.stdout.readline()
            print("GAME: ", line.strip())








    process.wait()

if __name__ == "__main__":
    main()