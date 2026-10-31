# Business Requirements

NotifyNow is a small SaaS company. When something happens in the app (signup, order, payment, password reset, outage), people need to be told.

Today the app sends all of this itself. Every new notification type means changing the app, and if the email provider has a problem, the app has a problem too.

What they need:

- The app reports an event once and doesn't care who gets notified.
- One event can trigger several notifications.
- New notification types can be added without touching the app.
- If one channel fails, the app and the other channels keep working.
- Failed notifications get retried. If they keep failing, they are kept so someone can look at them.
- The team can see what was sent and what failed.
- It stays small and cheap.
