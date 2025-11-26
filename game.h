//
// Created by Jordan Coleman on 11/24/2025.
//

#ifndef BLACKJACKAGENT_GAME_H
#define BLACKJACKAGENT_GAME_H
#include "Dealer.h"
#include "Player.h"
#include <iostream>

void startGame(std::istream& is, std::ostream& os, Dealer& dealer, Player& player);
void gameLoop(std::istream& is, std::ostream& os, Dealer& dealer, Player& player);



#endif //BLACKJACKAGENT_GAME_H