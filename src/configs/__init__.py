class Environment:
    def __init__(self, env: str):
        """
        Initialize the environment with a name and description.
        :param env: The name of the environment (e.g., "dev", "prod").
        """
        self.name = "Production" if env == "prod" else "Development"
        self.description = (
            "Production environment" if env == "prod" else "Development environment"
        )
        self.env = self.get_env(env)

    def __repr__(self):
        return f"Environment(name={self.name}, description={self.description})"

    def get_env(self, env: str):
        """
        Get the environment configuration based on the provided environment name.
        :param env: The name of the environment (e.g., "dev", "prod").
        :return: The environment configuration class.
        """
        if env == "prod":
            from src.configs.prodEnv import ProdConfig

            return ProdConfig()
        else:
            from src.configs.devEnv import DevConfig

            return DevConfig()
