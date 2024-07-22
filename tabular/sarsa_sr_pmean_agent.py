# Author: Marlos C. Machado

from agent import Agent
import numpy as np
from scheduler import Scheduler

class Sarsa_SR_PMean(Agent):

    def __init__(self, env, step_size, step_size_sr, gamma, gamma_sr, epsilon, beta, p=1, decay_steps=1000, stability_const=1.0e-3):
        super().__init__(env)
        self.gamma = gamma
        self.alpha = step_size
        self.epsilon = epsilon
        self.curr_s = self.env.get_current_state()

        # SR part
        self.beta = beta
        self.alpha_sr = step_size_sr
        self.gamma_sr = gamma_sr
        self.num_states = self.env.get_num_states()
        self.sr = np.zeros((self.num_states, self.num_states))

        # P mean part
        self.p = p
        self.stability_const = stability_const
        self.scheduler = Scheduler(decay_steps)

    def step(self):
        # SR step
        curr_a = self.epsilon_greedy(self.q[self.curr_s], epsilon=self.epsilon)
        r = self.env.act(curr_a)
        next_s = self.env.get_current_state()
        next_a = self.epsilon_greedy(self.q[next_s], epsilon=self.epsilon)

        # SR step
        self.update_sr_values(self.curr_s, next_s)

        # Sarsa step
        expl_bonus = self.norm(self.sr[self.curr_s]) 
        norm1_bonus = self.norm1(self.sr[self.curr_s])
        actual_r = r + self.beta * ((1./expl_bonus) * self.scheduler.get_bonus_rate() + (1./norm1_bonus) * (1.-self.scheduler.get_bonus_rate()))

        self.scheduler.step()

        self.update_q_values(self.curr_s, curr_a, actual_r, next_s, next_a)

        self.curr_s = next_s

        self.current_undisc_return += r
        if self.env.is_terminal():
            self.episode_count += 1
            self.total_undisc_return += self.current_undisc_return
            self.current_undisc_return = 0

    def update_q_values(self, s, a, r, next_s, next_a):
        self.q[s][a] = self.q[s][a] + self.alpha * (r + self.gamma * (1.0 - self.env.is_terminal()) *
                                                    self.q[next_s][next_a] - self.q[s][a])

    def update_sr_values(self, s, next_s):
        for i in range(self.num_states):
            cumulant = 1 if i == s else 0

            # print(self.sr[s][i], '+', self.alpha_sr, '* (', cumulant, '+', self.gamma_sr, '-
            # (',  1.0, '-',
            #       self.env.is_terminal(), ') *', self.sr[next_s][i], '-', self.sr[s][i], ')')
            self.sr[s][i] = self.sr[s][i] + self.alpha_sr * (cumulant + self.gamma_sr * (1.0 - self.env.is_terminal()) *
                                                             self.sr[next_s][i] - self.sr[s][i])

        # print(self.sr)
    
    def norm(self, sr):
        abs = np.abs(sr)
        if self.p < 0:
            abs += self.stability_const
        return self.num_states * ((np.mean(abs**self.p))**(1/self.p))

    def norm1(self, sr):
        return np.linalg.norm(self.sr[self.curr_s], ord=1)