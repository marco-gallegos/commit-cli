from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env.

# Code of your application, which uses environment variables (e.g. from `os.environ` or
# `os.getenv`) as if they came from the actual environment.


class EnviromentConfiguration(object):

    def __init__(self) -> None:
        self.current_environment = "production"
        
        file_environment = os.getenv("environment")
        
        # print(file_environment)

        if file_environment :
            self.current_environment = file_environment

    def can_log_data(self) -> bool:
        should_log:bool = False if self.current_environment == "production" else True
        # print(f"should log {should_log}")
        return should_log


current_environment_configuration:EnviromentConfiguration = EnviromentConfiguration()
