# Current Architecture Analysis

## How it works today

```
Customer action
      |
      v
Main application
      |
      +--> send email
      +--> send SMS
      +--> send internal notification
```

The main app does the business work and then calls every notification channel itself, one after the other, while the customer waits.

## Problems

| Problem | What it means in practice |
|---|---|
| Tight coupling | The app knows every channel, its API and its credentials. A new channel means changing and redeploying the main app. |
| Failures spread | If the SMS provider is down, the request can fail or hang, even though the order itself was fine. |
| Slow responses | The customer waits until all notifications are sent. |
| No retries | If a send fails, it is simply lost unless someone wrote retry code in the app. |
| No visibility | There is no single place to see what was sent and what failed. |
| Hard to scale | A busy day means the app does more notification work on top of its real work. |

## What coupling means

Two parts are coupled when one has to know about the other and changes or failures in one hit the other. Here the main app is coupled to every notification channel. The goal is that the app only says "this happened" and does not know or care who reacts to it.
