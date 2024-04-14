__author__ = "Nick Brown"
__organization__ = "COSC343, University of Otago"
__email__ = "broni673@student.otago.ac.nz"

import numpy as np
import random
import itertools
import collections
from itertools import product
from mastermind import evaluate_guess
import json
import csv

class MastermindAgent():
    previous_guesses = []
    all_moves = [] # A list of all moves, generated once on startup
    possible_answers = [] # A list of all possible answers
    possible_moves = []

    max_moves = -5
    min_moves = 50
    
    all_scores = {}

    def __init__(self, code_length,  colours, num_guesses):
        self.code_length = code_length
        self.colours = colours
        self.num_guesses = num_guesses
        self.all_moves = self.generateAllCombos()
        self.generateScores()
        #print(self.all_scores)
    
    def generateScores(self):
        scores = {}
        for i in range(self.code_length+1):
            for j in range(self.code_length+1):
                if i + j <= self.code_length:
                    score = (i,j)
                    scores.update({score:0})
        self.all_scores = scores

    def generateAllCombos(self):
        colours = self.colours
        list_length = self.code_length
        combinations = list(product(colours, repeat=list_length))
        combo_list = [list(combination) for combination in combinations]
        return combo_list
    
    def generateFirstMove(self):
        if len(self.previous_guesses) > 0:
            return random.choice(self.possible_answers)
        i = 0
        j = 0
        colour_list = self.colours.copy()
        guess = []
        while i < self.code_length:
            #print(colour_list)
            guess.append(colour_list[j])
            i += 1
            if i % 2 == 0:
                j += 1
        return guess

    def pickGuess(self):
        if len(self.previous_guesses) > 0:
            recent_guess = self.previous_guesses[-1] # Save the most recent guess

            ## This block removes all answers that cannot give the feedback required for the most recent guess, narrowing down the possibilities
            temp_possible_answers = []
            for answer in self.possible_answers:
                recent_score = evaluate_guess(recent_guess["guess"],answer)
                if recent_score == recent_guess["score"]:
                    temp_possible_answers.append(answer)
            self.possible_answers = temp_possible_answers

        if len(self.previous_guesses) > 1: # If 2 or more guesses have been made
            guess_list = []
            #guesses_checked = []
            for guess in self.possible_answers:
                score_dict = self.all_scores.copy()
                for answer in self.possible_answers:
                    #if (guess, answer) not in guesses_checked and (answer, guess) not in guesses_checked:
                        if guess != answer:
                            score = evaluate_guess(guess,answer)
                            score_dict[score] += 1
                            #guesses_checked.append((guess,answer))
                #counts = collections.Counter(score_dict.values())
                worst = max(score_dict.values())
                guess_list.append((worst, guess))
            #print(guess_dict)
            minimum = min(guess_list)
            #print(minimum)
            return minimum[-1]
        else:    
            return self.generateFirstMove()


    def AgentFunction(self, percepts):
        guess_counter, last_guess, in_place, in_colour = percepts

        moves = guess_counter+1
        if moves > self.max_moves:
            self.max_moves = moves
        if moves < self.min_moves:
            self.min_moves = moves

        if guess_counter == 0:
            self.previous_guesses = []
            self.possible_answers = self.all_moves.copy()
        else:
            last_guess_dict = {"guess": last_guess, "score":(in_place,in_colour)}
            self.previous_guesses.append(last_guess_dict)

        move = self.pickGuess()
        self.possible_answers.remove(move)
        print('Max moves: {}, Min Moves: {}'.format(self.max_moves, self.min_moves))
        return move


