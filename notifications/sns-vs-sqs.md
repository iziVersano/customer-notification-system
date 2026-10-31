# SNS vs SQS

- **Event:** something that happened, like "order ORD-1001 was created".
- **Publish/subscribe:** the sender publishes to a topic, and whoever is interested subscribes. They don't know each other.
- **Fan-out:** one message gets copied to every subscriber.

**SNS** pushes a message to all subscribers. It doesn't store messages. If a subscriber is down, it retries for a while and then drops the message, unless the subscription has a DLQ.

**SQS** is a queue. Messages wait there (up to 14 days) until one consumer reads them. If processing fails, the message comes back and is tried again. After too many tries it goes to a dead-letter queue.

So SNS is for getting one event to many places, and SQS is for not losing work and letting a consumer go at its own speed.

Together: SNS fans out, and each consumer gets its own queue. If one consumer breaks, only its queue fills up. The app and the other consumers don't notice, and nothing is lost.
