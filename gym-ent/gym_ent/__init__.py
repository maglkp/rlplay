from gym.envs.registration import register

register(
    id='ent-v1',
    entry_point='gym_ent.envs:EntEnv',
)