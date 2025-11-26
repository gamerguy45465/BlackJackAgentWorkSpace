#include <iostream>
#include "game.h"
#include "Dealer.h"
#include "Player.h"
#include <string>

int main()
{
    Dealer dealer;
    Player player;


    std::istream& is = std::cin;
    std::ostream& os = std::cout;



    for (;;)
    {
        std::string play_again;
        os << "Play again? (y, n) " << std::endl;
        is >> play_again;
        if (play_again == "y" || play_again == "Y")
            startGame(is, os, dealer, player);

        else if (play_again == "s" || play_again == "S")
            os << std::to_string(player.getMoney()) << std::endl;

        else if (play_again == "n" || play_again == "N")
            break;
    }

    return 0;


}