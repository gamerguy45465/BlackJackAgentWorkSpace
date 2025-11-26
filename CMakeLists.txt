cmake_minimum_required(VERSION 4.0)
project(BlackJackAgent)

set(CMAKE_CXX_STANDARD 26)

add_executable(BlackJackAgent main.cpp
        Player.cpp
        Player.h
        Dealer.cpp
        Dealer.h
        game.h
        game.cpp
        p_agent.cpp
        p_agent.h
        p_agent.h
        p_agent.h)
