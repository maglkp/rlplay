from gym.envs.registration import register

register(
    id='random_treasure-v1',
    entry_point='random_treasure.envs:RandomTreasure',
)