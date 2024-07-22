# Author: Marlos C. Machado

import utils
import random
import numpy as np
import environment as env
from sarsa_sr_pmean_agent import Sarsa_SR_PMean

actions = ["right", "left"]

if __name__ == "__main__":
    # Read arguments:
    args = utils.ArgsParser.read_input_args()

    random.seed(args.seed)
    np.random.seed(args.seed)

    # Instantiate objects I'll need
    environment = env.MDP(args.input)

    ep_rs = []
    # Actual learning algorithm
    for ep in range(args.num_episodes):
        agent = Sarsa_SR_PMean(environment, args.step_size, args.step_size_sr,
                         args.gamma, args.gamma_sr, args.epsilon, args.beta, args.pmean, args.decay_steps)
        time_step = 1
        while not environment.is_terminal():
            agent.step()
            time_step += 1
        environment.reset()
        ep_r = agent.get_avg_undisc_return()
        print(f"{str(ep).ljust(2)},{utils.format_number(ep_r, 12)}")
        ep_rs.append(ep_r)
    print(f"total rs: {np.sum(np.array(ep_rs)):,}")
    
