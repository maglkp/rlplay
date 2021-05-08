from gym.envs.registration import register

register(
    id='ent-v0',
    entry_point='gym_ent.envs:EntEnv',
)