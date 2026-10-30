# Business Requirements

## The company

NotifyNow GmbH runs a small SaaS product. When something important happens in the app (a new customer signs up, an order is placed, a payment goes through, a password is reset, the service goes down), customers and staff need to be told.

## The problem today

The main application sends every notification itself: email, SMS and internal messages are all coded inside it. Each new notification type means changing the main app. If the email provider is slow or down, the app is slowed down or fails too.

## What the business needs

1. The app reports an event once ("order created") and doesn't care who gets notified.
2. One event can trigger several notifications (email, SMS, internal log).
3. A new notification type can be added without touching the main app.
4. If one notification channel fails, the app and the other channels keep working.
5. Failed notifications are retried, and the ones that keep failing are kept aside so nothing is lost silently.
6. The team can see what was sent and what failed.
7. It stays cheap and small, and it grows when the number of events grows.
