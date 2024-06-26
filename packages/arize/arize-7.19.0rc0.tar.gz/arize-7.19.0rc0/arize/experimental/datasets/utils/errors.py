from abc import ABC, abstractmethod


class DatasetError(Exception, ABC):
    def __str__(self) -> str:
        return self.error_message()

    @abstractmethod
    def error_message(self) -> str:
        pass


class InvalidSessionError(DatasetError):
    @staticmethod
    def error_message() -> str:
        return (
            "Credentials not provided or invalid. Please pass in the correct api_key when "
            "initiating a new ArizeExportClient. Alternatively, you can set up credentials "
            "in a profile or as an environment variable"
        )


class InvalidConfigFileError(DatasetError):
    @staticmethod
    def error_message() -> str:
        return "Invalid/Misconfigured Configuration File"
