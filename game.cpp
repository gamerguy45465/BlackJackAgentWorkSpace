//
// Created by Jordan Coleman on 11/24/2025.
//


#include "game.h"
#include "Player.h"
#include "Dealer.h"
#include <vector>
#include <iostream>



void startGame(std::istream& is, std::ostream& os, Dealer& dealer, Player& player)
{

    int new_bet;

    os << "Place your bets on the table: " << std::endl;
    is >> new_bet;

    player.placeBet(new_bet);

    player.Hit(dealer.DealCard());
    player.Hit(dealer.DealCard());

    dealer.Hit(dealer.DealCard());
    dealer.HitHole(dealer.DealCard());

    if (player.checkBlackJack())
    {
        os << "Player got a Blackjack!" << std::endl;
        return;
    }

    player.showCards(is, os, false);


    dealer.showCards(is, os, true);



    gameLoop(is, os, dealer, player);

}

void gameLoop(std::istream& is, std::ostream& os, Dealer& dealer, Player& player)
{
    for (;;)
    {
        os << "Hit or Stay? " << std::endl;

        std::string decision;

        is >> decision;


        if (decision == "Hit")
        {
            player.Hit(dealer.DealCard());
        }
        else if (decision == "Stay")
        {
            break;
        }

        player.KeepScore();
        if (player.getScore() > 21)
        {
            os << "Player Busts!" << std::endl;
            player.showCards(is, os, false);
            os << "Score: " << player.getScore() << std::endl;
            return;
        }
        player.showCards(is, os, false);
        os << "Score: " << player.getScore() << std::endl;


    }
    dealer.Hit(dealer.getHole());
    dealer.showCards(is, os, true);
    os << "Dealer Score: " << dealer.getScore() << std::endl;


    while (dealer.KeepScore() < 17)
    {
        dealer.Hit(dealer.DealCard());
        dealer.showCards(is, os, true);
        os << "Dealer Score: " << dealer.getScore() << std::endl;
    }


    if (dealer.getScore() > 21)
    {
        os << "Dealer Busts!" << std::endl;

    }
    else
    {
        if (dealer.getScore() > player.getScore())
        {
            os << "Dealer Wins!" << std::endl;
        }
        else if (dealer.getScore() == player.getScore())
        {
            os << "Push" << std::endl;
        }
        else
        {
            os << "You Win!" << std::endl;
        }
    }



}






