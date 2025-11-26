//
// Created by Jordan Coleman on 11/24/2025.
//

#include "Player.h"


//
// Created by Jordan Coleman on 11/15/2025.
//

#include "Player.h"


#include <iostream>
#include <unordered_map>


Player::Player()
    :score(0), bet(0){
    chips[1] = 10;
    chips[5] = 10;
    chips[10] = 10;
    chips[20] = 10;
    chips[50] = 10;
    chips[100] = 10;


}

Player::Player(bool isDealer)
    :score(0), bet(0){
    chips[1] = 0;
    chips[5] = 0;
    chips[10] = 0;
    chips[20] = 0;
    chips[50] = 0;
    chips[100] = 0;

}



void Player::placeBet(int amount)
{
    if (amount == 1 || amount == 5 || amount == 10 || amount == 20 || amount == 50 || amount == 100)
    {
        bet = chips[amount];
        --chips[amount];
    }
    else
    {
        std::cout << "Invalid Input" << std::endl;
    }


}


int Player::getMoney()
{
    int sum = 0;

    std::unordered_map<int, int> mons;
    mons[0] = 1;
    mons[1] = 5;
    mons[2] = 10;
    mons[3] = 20;
    mons[4] = 50;
    mons[5] = 100;

    for(int i = 0; i <= 5; ++i)
    {
        sum += chips[i] * mons[i];
    }

    return sum;
}



bool Player::checkBlackJack()
{
    int score = KeepScore();

    if (score == 21)
    {
        return true;
    }

    return false;
}



void Player::SplitCards(std::istream& is, std::ostream& os)
{
    if (cards.size() == 2)
    {
        if (cards[0].value == cards[1].value)
        {
            std::string decision;
            os << "Would you like to Split? ";
            is >> decision;

            if (decision == "Yes")
            {
                Card split_card = cards.back();
                split.push_back(split_card);
                cards.pop_back();
            }

        }
    }
}







void Player::Hit(const Card& dealt_card)
{
    cards.push_back(dealt_card);

    //showCards();

}

int Player::KeepScore()
{
    score = 0;
    for (int i = 0; i < cards.size(); i++)
    {
        if (cards[i].value != 1 && cards[i].value != 11 && cards[i].value != 12 && cards[i].value != 13)
            score += cards[i].value;

        else if (cards[i].value == 1)
        {
            if ((score + 10) == 21)
            {
                score += 10;
            }
            else
            {
                score += 1;
            }
        }
        else
        {
            score += 10;
        }
    }
    return score;
}


int Player::getScore()
{
    return score;
}



void Player::showCards(std::istream& is, std::ostream& os, bool Dealer)
{
    if (Dealer == true)
        os << "Dealer Cards: " << std::endl;
    else
        os << "Player Cards: " << std::endl;
    for (const auto card : cards)
    {
        if (card.value > 1 && card.value < 11)
            os << card.value << std::endl;
        else if (card.value == 1)
            os << "Ace" << std::endl;
        else if (card.value == 11)
            os << "Jack" << std::endl;
        else if (card.value == 12)
            os << "Queen" << std::endl;
        else if (card.value == 13)
            os << "King" << std::endl;
    }

    //os << std::endl << std::endl;

}

void Player::ClearDeck()
{
    cards.clear();
}

std::string Player::HitOrStay(std::istream& is, std::ostream& os)
{

    std::string decision;

    is >> decision;

    while (decision != "Hit" && decision != "Stay")
    {
        os << "Error: Invalid input. Please try again. Type Hit or Stay.";
        is >> decision;
    }

    return decision;


}