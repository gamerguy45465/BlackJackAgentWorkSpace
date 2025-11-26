//
// Created by Jordan Coleman on 11/24/2025.
//

#ifndef BLACKJACKAGENT_DEALER_H
#define BLACKJACKAGENT_DEALER_H

#include "Player.h"
#include <vector>


class Dealer : public Player
{
protected:
    std::vector<Card> deck;
    Card mHole;
public:
    Dealer();
    Card DealCard();
    void createDeck();
    void HitHole(const Card& hole);
    Card getHole();


};


#endif //BLACKJACKAGENT_DEALER_H