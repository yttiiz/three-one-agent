from src.models.client import GoogleAIClient


def main():
    client = GoogleAIClient()
    client.ask(input("Je vous écoute... :\n"))


if __name__ == "__main__":
    main()
