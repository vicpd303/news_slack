# Slack Auto-briefing System

이 저장소는 GitHub Actions와 Slack을 활용하여 매일 오전 9시(KST)에 국제정치 분석 프롬프트를 슬랙 채널로 전송하는 예제입니다.

## 구성
- **prompt.txt**: 슬랙으로 보낼 프롬프트가 담긴 파일입니다.
- **send_slack_notification.py**: Slack API를 이용해 메시지를 전송합니다.
- **.github/workflows/send-slack-notification.yml**: 매일 자동 실행되는 워크플로우 설정 파일입니다.

## Slack 연동 방법
1. Slack에서 봇 토큰을 발급받아 `SLACK_BOT_TOKEN` 값을 준비합니다.
2. 메시지를 전송할 채널 ID를 `SLACK_CHANNEL` 값으로 사용합니다.
3. 저장소의 **Settings > Secrets** 메뉴에서 `SLACK_BOT_TOKEN`, `SLACK_CHANNEL` 두 값을 등록합니다.
4. 위 값이 설정되지 않으면 스크립트는 메시지 전송을 건너뜁니다.

## 수동 실행
로컬 환경에서 테스트하려면 다음 명령어를 실행합니다.

```bash
export SLACK_BOT_TOKEN=your_token
export SLACK_CHANNEL=your_channel
python send_slack_notification.py
```

## 라이선스
MIT
