# Author: Marlos C. Machado

import argparse
import numpy as np


def argmax(vector):
    # This argmax breaks ties randomly
    return np.random.choice(np.flatnonzero(vector == vector.max()))


class ArgsParser:
    """
    Read the user's input and parse the arguments properly. When returning args, each value is properly filled.
    Ideally one shouldn't have to read this function to access the proper arguments, but I postpone this.
    """

    @staticmethod
    def read_input_args():
        # Parse command line
        parser = argparse.ArgumentParser(
            description='Define algorithm\'s parameters.')

        parser.add_argument('-s', '--seed', type=int, default=1, help='Seed to be used in the code.')
        parser.add_argument('-i', '--input', type=str, default='mdps/toy.mdp',
                            help='File containing the MDP definition (default: mdps/toy.mdp).')
        parser.add_argument('-n', '--num_episodes', type=int, default=1000,
                            help='For how many episodes we are going to learn.')
        parser.add_argument('-a', '--step_size', type=float, default=0.1,
                            help="Algorithm's step size. Alpha parameter in algorithms such as Sarsa.")
        parser.add_argument('-y', '--step_size_sr', type=float, default=0.1,
                            help="Step size to compute the SR with TD when using it in algorithms such as Sarsa.")
        parser.add_argument('-b', '--beta', type=float, default=1.0,
                            help="Real reward = Real reward + beta * Intrinsic Reward.")
        parser.add_argument('-g', '--gamma', type=float, default=0.95,
                            help='Gamma. Discount factor to be used by the algorithm.')
        parser.add_argument('-z ', '--gamma_sr', type=float, default=0.95,
                            help='Gamma value to compute the SR.')
        parser.add_argument('-e', '--epsilon', type=float, default=0.05,
                            help='Epsilon. This is the exploration parameter (trade-off).')
        parser.add_argument('-r', '--reward_structure', type=str, default="",
                            help="Valid values: 'dot-prod', 'diff', 'gamma-diff', 'norm' ")
        parser.add_argument('-d', '--divide', type=bool, default=False,
                            help="If true, the reward is equal to 1/reward_structure")
        parser.add_argument('-p', '--pmean', type=float, default=1,
                    help="The p factor in computing pmeans")
        parser.add_argument('-c', '--decay_steps', type=int, default=-1,
                    help="Decay in bonus")
        args = parser.parse_args()

        return args
    

def format_number(number, width):
    # Format with thousands separator
    formatted = f"{number:,}"
    # Left pad with spaces
    return formatted.rjust(width)