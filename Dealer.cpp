//
// Created by Jordan Coleman on 11/24/2025.
//

#include "Dealer.h"
#include <vector>
#include <algorithm>
#include <random>



Dealer::Dealer()
    :Player(true){
    createDeck();


}

Card Dealer::DealCard()
{
    Card card = deck.back();
    deck.pop_back();
    return card;
}


void Dealer::createDeck()
{
    std::vector<std::string> suits = {"Clubs", "Diamonds", "Spades", "Hearts"};

    for (const auto& suit : suits)
    {
        for (int i = 1; i <= 13; i++)
        {
            Card card;
            card.value = i;
            card.class_t = suit;
            deck.push_back(card);

        }

    }

    std::random_device rd;
    std::mt19937 g(rd());

    std::shuffle(deck.begin(), deck.end(), g);
    std::shuffle(deck.begin(), deck.end(), g);
    std::shuffle(deck.begin(), deck.end(), g); //Called three times to ensure best randomization results

}


void Dealer::HitHole(const Card& hole)
{
    mHole = hole;

}


Card Dealer::getHole()
{
    return mHole;
}
