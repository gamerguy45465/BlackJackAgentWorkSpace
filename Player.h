//
// Created by Jordan Coleman on 11/15/2025.
//

#ifndef BLACKJACK_PLAYER_H
#define BLACKJACK_PLAYER_H

#include <iostream>
#include <vector>
#include <unordered_map>



struct Card
{
    std::string class_t;
    int value;
};



class Player
{
protected:
    std::vector<Card> cards;
    std::vector<Card> split;
    std::unordered_map<int, int> chips;
    int score;
    int bet;

public:
    Player();
    Player(bool isDealer);
    void placeBet(int amount);
    int getMoney();
    bool checkBlackJack();
    void SplitCards(std::istream& is, std::ostream& os);
    void Hit(const Card& dealt_card);
    int KeepScore();
    int getScore();
    void showCards(std::istream& is, std::ostream& os, bool Dealer);
    void ClearDeck();
    std::string HitOrStay(std::istream& is, std::ostream& os);

};


#endif //BLACKJACK_PLAYER_H