class InvalidEnvironmentVariable(Exception):
    def __str__(self) -> str:
        return "無効な環境変数が含まれています"
