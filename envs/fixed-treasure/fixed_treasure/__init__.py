from gym.envs.registration import register

register(
    id='fixed_treasure-v1',
    entry_point='fixed_treasure.envs:FixedTreasure',
)