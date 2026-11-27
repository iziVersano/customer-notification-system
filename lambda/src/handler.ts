import type { SQSBatchResponse, SQSHandler } from 'aws-lambda'

// The event as published to the customer-events topic. Raw delivery puts it in the SQS body as it is.
interface CustomerEvent {
  type: string
  orderId: string
  customerId: string
}

function parse(body: string): CustomerEvent {
  const event = JSON.parse(body) as Partial<CustomerEvent>
  if (!event.type || !event.orderId || !event.customerId) {
    throw new Error('event needs type, orderId and customerId')
  }
  return event as CustomerEvent
}

// Only the messages that fail go back to the queue; the rest of the batch is deleted.
export const handler: SQSHandler = async (sqsEvent): Promise<SQSBatchResponse> => {
  const batchItemFailures: SQSBatchResponse['batchItemFailures'] = []

  for (const record of sqsEvent.Records) {
    try {
      const event = parse(record.body)
      console.log(JSON.stringify({ level: 'info', messageId: record.messageId, type: event.type, orderId: event.orderId, customerId: event.customerId }))
    } catch (error) {
      console.error(JSON.stringify({ level: 'error', messageId: record.messageId, error: String(error) }))
      batchItemFailures.push({ itemIdentifier: record.messageId })
    }
  }

  return { batchItemFailures }
}
