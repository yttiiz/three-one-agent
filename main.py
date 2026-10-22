from src.client.index import GoogleAIClient


def main():
    client = GoogleAIClient()

    user_id = input("Identifiant (Entree = guest) > ").strip() or "guest"
    print(f"Agent pret pour '{user_id}'. Tapez 'quit' pour sortir.")

    while True:
        message = input("Vous > ").strip()
        if message.lower() in {"quit", "exit", "q"}:
            break
        if message:
            try:
                print(f"Agent > {client.ask(message, user_id)}")
            except Exception as error:
                print(f"Erreur : {error}")


if __name__ == "__main__":
    main()
