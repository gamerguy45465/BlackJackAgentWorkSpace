import sys
import os
import subprocess
import shutil
import math
import heapq


def Expectiminimax(current_depth, index, turn, last, scores, available_cards, target_depth):
    s: int = 0
    p: float = 0.0
    if(current_depth == target_depth):
        return 1

    if(turn == "Max"):
        return min(Expectiminimax(current_depth + 1, index, "Prob", "Max", scores, available_cards, target_depth), Expectiminimax(current_depth + 1, index + 1, "Prob", "Max", scores, available_cards, target_depth))

    elif(turn == "Min"):
        return max(Expectiminimax(current_depth + 1, index, "Prob", "Min", scores, available_cards, target_depth), Expectiminimax(current_depth + 1, index + 1, "Prob", "Max", scores, available_cards, target_depth))

    elif(turn == "Prob"):
        if(scores[index] == 1):
            p = available_cards["Ace"]/len(scores)
            if(available_cards["Ace"] > 0):
                available_cards["Ace"] -= 1
                scores.remove(scores[index])

        elif(scores[index] == 11):
            p = available_cards["Jack"]/len(scores)
            if(available_cards["Jack"] > 0):
                available_cards["Jack"] -= 1
                scores.remove(scores[index])

        elif(scores[index] == 12):
            p = available_cards["Queen"]/len(scores)
            if(available_cards["Queen"] > 0):
                available_cards["Queen"] -= 1
                scores.remove(scores[index])

        elif(scores[index] == 13):
            p = available_cards["King"]/len(scores)
            if(available_cards["King"] > 0):
                available_cards["King"] -= 1
                scores.remove(scores[index])

        else:
            p = available_cards[str(scores[index])]/len(scores)
            if(available_cards[str(scores[index])] > 0):
                available_cards[str(scores[index])] -= 1
                scores.remove(scores[index])


        if(last == "Max"):
            #return p * min(Expectiminimax(current_depth + 1, index, "Min", "Prob", scores, available_cards, target_depth), Expectiminimax(current_depth + 1, index + 1, "Min", "Prob", scores, available_cards, target_depth))
            return p * 1

        elif(last == "Min"):
            #return p * max(Expectiminimax(current_depth + 1, index, "Max", "Prob", scores, available_cards, target_depth), Expectiminimax(current_depth + 1, index + 1, "Max", "Prob", scores, available_cards, target_depth))
            return p * -1





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



            print(deck)

            target_depth = math.ceil(math.log(len(deck) - 1, 2))
            print("Target Depth: ",target_depth)
            temp_cards = available_cards.copy()
            temp_deck = deck.copy()
            s1 = Expectiminimax(0, 0, "Max", "Max", deck, available_cards, target_depth)
            available_cards = temp_cards.copy()
            deck = temp_deck.copy()


            print("S1: ", s1)
            if(s1 > .01):
                process.stdin.write("Hit\n")
                #process.stdin.flush()
                line = process.stdout.readline()
                print(line.strip())


    # Here is where YOU will add your logic to send moves:
    # process.stdin.write("y\n")
    # process.stdin.flush()

    process.wait()

if __name__ == "__main__":
    main()