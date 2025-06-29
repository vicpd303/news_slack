import os
import logging

try:
    from slack_sdk import WebClient
    from slack_sdk.errors import SlackApiError
except ModuleNotFoundError:  # pragma: no cover - optional dependency
    WebClient = None
    SlackApiError = Exception

try:
    import google.generativeai as genai
except ModuleNotFoundError:  # pragma: no cover - optional dependency
    genai = None


def configure_logging() -> None:
    level = os.environ.get("LOG_LEVEL", "INFO").upper()
    logging.basicConfig(level=level, format="%(levelname)s: %(message)s")


def send_error(client: WebClient, channel: str, error: str) -> None:
    try:
        client.chat_postMessage(channel=channel, text=f"Error: {error}")
    except Exception as exc:  # pragma: no cover - best effort
        logging.error("Failed to send error report: %s", exc)


def load_message() -> str:
    gemini_key = os.environ.get("GEMINI_API_KEY")
    if gemini_key:
        if genai is None:
            raise RuntimeError("google-generativeai is not installed")
        genai.configure(api_key=gemini_key)
        model = genai.GenerativeModel("gemini-pro")
        prompt = open("prompt.txt", "r", encoding="utf-8").read()
        response = model.generate_content(prompt)
        return response.text
    with open("prompt.txt", "r", encoding="utf-8") as f:
        return f.read()


def main():
    configure_logging()

    token = os.environ.get("SLACK_BOT_TOKEN")
    channel = os.environ.get("SLACK_CHANNEL")
    error_channel = os.environ.get("SLACK_ERROR_CHANNEL", channel)

    if not token or not channel:
        logging.warning("Slack configuration missing. Skipping notification.")
        return

    if WebClient is None:
        logging.warning("slack_sdk is not installed. Skipping notification.")
        return

    client = WebClient(token=token)
    try:
        message = load_message()
    except Exception as exc:
        logging.error("Gemini API error: %s", exc)
        if error_channel:
            send_error(client, error_channel, f"Gemini API error: {exc}")
        return

    try:
        client.chat_postMessage(channel=channel, text=message)
    except SlackApiError as e:
        logging.error("Slack API error: %s", e.response.get('error', e))
        if error_channel:
            send_error(client, error_channel, f"Slack API error: {e.response.get('error', e)}")


if __name__ == "__main__":
    main()
