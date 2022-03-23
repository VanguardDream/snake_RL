# Import the RL algorithm (Trainer) we would like to use.
from ray.rllib.agents.ppo import PPOTrainer
from ray.rllib.agents.pg import PGTrainer

# Configure the algorithm.
config = {
    # Environment (RLlib understands openAI gym registered strings).
    "env": "bongSnake-v0",
    # Use 2 environment workers (aka "rollout workers") that parallelly
    # collect samples from their own environment clone(s).
    # Change this to "framework: torch", if you are using PyTorch.
    # Also, use "framework: tf2" for tf2.x eager execution.
    "framework": "torch",
    # Tweak the default model provided automatically by RLlib,
    # given the environment's observation- and action spaces.
    "model": {
        "fcnet_hiddens": [64, 64],
        "fcnet_activation": "relu",
    },
    # Set up a separate evaluation worker set for the
    # `trainer.evaluate()` call after training (see below).
    "evaluation_num_workers": 1,
    # Only for evaluation runs, render the env.
    "evaluation_config": {
        "render_env": True,
    }
}

# Create our RLlib Trainer.
trainer = PPOTrainer(config=config)
# trainer = PGTrainer(config=config)