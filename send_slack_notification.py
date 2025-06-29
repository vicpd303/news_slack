import os

try:
    from slack_sdk import WebClient
    from slack_sdk.errors import SlackApiError
except ModuleNotFoundError:
    WebClient = None
    SlackApiError = Exception


def main():
    token = os.environ.get("SLACK_BOT_TOKEN")
    channel = os.environ.get("SLACK_CHANNEL")
    if not token or not channel:
        print("Slack configuration missing. Skipping notification.")
        return

    if WebClient is None:
        print("slack_sdk is not installed. Skipping notification.")
        return

    client = WebClient(token=token)
    with open("prompt.txt", "r", encoding="utf-8") as f:
        message = f.read()

    try:
        client.chat_postMessage(channel=channel, text=message)
    except SlackApiError as e:
        print(f"Slack API error: {e.response['error']}")


if __name__ == "__main__":
    main()
