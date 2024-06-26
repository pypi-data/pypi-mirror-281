from gym.envs.registration import register

register(
     id="WSNRouting-v0",
     entry_point="gym_examples.envs:WSNRoutingEnv",
     max_episode_steps=50,
)

__version__ = "2.0.139"
