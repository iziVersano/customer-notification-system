"""Demo UI for the notification project. The app is simulated, AWS is real."""
import json
import os
import subprocess
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ACCOUNT = os.environ.get('AWS_ACCOUNT_ID', '272423022449')
PROFILE = os.environ.get('AWS_PROFILE', 'dci')
REGION = 'eu-central-1'
TOPIC = f'arn:aws:sns:{REGION}:{ACCOUNT}:customer-events'
DLQ = f'https://sqs.{REGION}.amazonaws.com/{ACCOUNT}/notifications-dlq'
AWS = os.environ.get('AWS_BIN', 'aws')
PORT = int(os.environ.get('PORT', '8790'))
DIST = Path(__file__).resolve().parent / 'frontend' / 'dist'

EVENTS = {
    'good': {'type': 'order.shipped', 'orderId': 'A-2001', 'customerId': 'C-2001'},
    'bad': {'type': 'order.shipped', 'orderId': 'A-2002'},
}
sent = {'good': None, 'bad': None, 'purged': None}
lock = threading.Lock()


def aws(*args):
    cmd = [AWS, *args, '--profile', PROFILE, '--region', REGION, '--output', 'json', '--no-cli-pager']
    done = subprocess.run(cmd, capture_output=True, text=True, timeout=25)
    if done.returncode:
        raise RuntimeError(done.stderr.strip() or 'AWS call failed')
    return json.loads(done.stdout) if done.stdout.strip() else {}


def queue_and_alarm():
    with ThreadPoolExecutor() as pool:
        queue = pool.submit(aws, 'sqs', 'get-queue-attributes', '--queue-url', DLQ,
                            '--attribute-names', 'ApproximateNumberOfMessages')
        alarm = pool.submit(aws, 'cloudwatch', 'describe-alarms', '--alarm-names', 'notifications-dlq-not-empty')
        count = int(queue.result()['Attributes']['ApproximateNumberOfMessages'])
        return count, alarm.result()['MetricAlarms'][0]['StateValue']


def bad_blocked(count, alarm):
    now = time.time()
    if count and sent['bad']:
        return 'Sent. Reset before you run it again.'
    if count:
        return 'Reset first: an old message is in the dead-letter queue.'
    if sent['purged'] and now - sent['purged'] < 60:
        return 'The reset takes up to a minute.'
    if alarm != 'OK':
        return 'Wait for the alarm to show OK (3 to 5 minutes).'
    if sent['bad'] and now - sent['bad'] < 600:
        return 'Sent. The alert takes about 5 minutes.'
    return ''


def lambda_results():
    result = {'logged': False, 'tries': 0}
    times = [t for t in (sent['good'], sent['bad']) if t]
    if not times:
        return result
    logs = aws('logs', 'filter-log-events', '--log-group-name', '/aws/lambda/notification-lambda',
               '--start-time', str(int((min(times) - 2) * 1000)), '--filter-pattern', '"messageId"')
    failures = {}
    for entry in logs.get('events', []):
        text, at = entry['message'], entry['timestamp'] / 1000 + 2
        try:
            line = json.loads(text[text.index('{'):])
        except ValueError:
            continue
        if sent['good'] and at >= sent['good'] and line.get('orderId') == 'A-2001':
            result['logged'] = True
        if sent['bad'] and at >= sent['bad'] and line.get('level') == 'error':
            failures[line['messageId']] = failures.get(line['messageId'], 0) + 1
    result['tries'] = min(3, max(failures.values(), default=0))
    return result


def state():
    count, alarm = queue_and_alarm()
    return {**sent, **lambda_results(), 'dlq': count, 'alarm': alarm, 'blocked': bad_blocked(count, alarm)}


def act(name):
    with lock:
        if name in EVENTS:
            if name == 'bad':
                reason = bad_blocked(*queue_and_alarm())
                if reason:
                    raise RuntimeError(reason)
            started = time.time()
            aws('sns', 'publish', '--topic-arn', TOPIC, '--message', json.dumps(EVENTS[name]))
            sent[name] = started
        else:
            aws('sqs', 'purge-queue', '--queue-url', DLQ)
            sent.update(good=None, bad=None, purged=time.time())


class Handler(BaseHTTPRequestHandler):
    def reply(self, code, body, kind='application/json'):
        data = body if isinstance(body, bytes) else json.dumps(body).encode()
        self.send_response(code)
        self.send_header('Content-Type', kind)
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Frame-Options', 'DENY')
        self.end_headers()
        self.wfile.write(data)

    def local(self):
        return self.headers.get('Host') in (f'localhost:{PORT}', f'127.0.0.1:{PORT}')

    def do_GET(self):
        if not self.local():
            return self.reply(403, {'error': 'local only'})
        if self.path == '/':
            return self.reply(200, (DIST / 'index.html').read_bytes(), 'text/html; charset=utf-8')
        for asset in (DIST / 'assets').glob('*'):
            if self.path == f'/assets/{asset.name}':
                kind = 'text/css' if asset.suffix == '.css' else 'text/javascript'
                return self.reply(200, asset.read_bytes(), kind)
        if self.path != '/api/state':
            return self.reply(404, {'error': 'not found'})
        try:
            self.reply(200, state())
        except Exception as error:
            self.reply(502, {'error': str(error)})

    def do_POST(self):
        # The custom header stops other websites from pressing the buttons.
        if not self.local() or self.headers.get('X-Demo') != '1':
            return self.reply(403, {'error': 'local only'})
        name = self.path.replace('/api/', '', 1)
        if name not in ('good', 'bad', 'reset'):
            return self.reply(404, {'error': 'not found'})
        try:
            act(name)
            self.reply(200, {'ok': True})
        except Exception as error:
            self.reply(502, {'error': str(error)})

    def log_message(self, *args):
        pass


if __name__ == '__main__':
    if aws('sts', 'get-caller-identity')['Account'] != ACCOUNT:
        raise SystemExit('Wrong AWS account, not starting.')
    print(f'http://localhost:{PORT}', flush=True)
    ThreadingHTTPServer(('127.0.0.1', PORT), Handler).serve_forever()
