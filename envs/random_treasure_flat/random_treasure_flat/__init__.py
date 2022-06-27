from gym.envs.registration import register

register(
    id='random_treasure_flat-v2',
    entry_point='random_treasure_flat.envs:RandomTreasureFlat',
)