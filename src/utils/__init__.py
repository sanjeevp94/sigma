def get_config_path(filename: str) -> str:
    """
    Constructs the path to a configuration file based on the DEPLOY_ENV environment variable.
    """
    import os

    env = os.environ.get("DEPLOY_ENV", "dev")  # Default to dev if not set

    # Path is relative to the root directory where the scripts are executed via Jenkins
    return os.path.join("deploy", env, filename)
