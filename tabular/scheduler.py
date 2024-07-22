class Scheduler:
    def __init__(self,decay_steps=1000):
        self.num_steps = 0
        self.decay_steps = decay_steps # -2 for removing, -1 for no decay

    def step(self):
        self.num_steps += 1

    def get_bonus_rate(self):
        if self.decay_steps < -1:
            return 0
        if self.decay_steps < 0:
            return 1
        if self.num_steps > self.decay_steps:
            return 0
        return 1.0 - float(self.num_steps)/self.decay_steps