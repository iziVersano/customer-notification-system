# Current Setup

```
Customer action
      |
      v
Main app
      |
      +--> email
      +--> SMS
      +--> internal notification
```

The app does its work, then calls each channel itself while the customer waits.

Problems:

- **Tight coupling.** The app knows every channel, its API and its credentials. A new channel means changing and redeploying the app.
- **Failures spread.** If SMS is down, the request can fail even though the order was fine.
- **Slow.** The customer waits for all the sends.
- **No retries.** A failed send is just lost.
- **No overview.** Nowhere to see what was sent or what failed.

Coupling means one part has to know about another, so its changes and failures hit you too. The goal is that the app only says "this happened" and doesn't know who reacts.
