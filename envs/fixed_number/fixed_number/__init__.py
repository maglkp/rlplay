from gym.envs.registration import register

register(
    id='fixed_number-v1',
    entry_point='fixed_number.envs:FixedNumber',
)