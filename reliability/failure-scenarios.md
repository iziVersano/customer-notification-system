# Failure Scenarios

| What goes wrong | What happens | Tested |
|---|---|---|
| Bad event (missing field) | Lambda fails it 3 times, it moves to the DLQ, the alarm fires | Yes, see `tests/test-results.md` |
| Lambda has a bug or crashes | Same as above for every message: they retry, then pile up in the DLQ and the alarm fires | No, same path as above |
| Lambda is down or throttled | Messages wait in the queue (up to 4 days) and get processed when it's back | No |
| Same message delivered twice | It gets logged twice today. Fix planned: duplicate check on `eventId` in DynamoDB | No |
| Email subscriber not confirmed | SNS sends nothing to it. The queue still gets every event | Seen once, the old subscription expired |
| Terraform run against the wrong AWS account | The account guard stops the plan before anything changes | Yes, see `tests/test-results.md` |

The main idea: the queue sits between SNS and the Lambda, so when the Lambda has a problem, messages wait instead of getting lost.
