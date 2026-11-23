"""Demo UI for the notification project. The app is simulated, AWS is real."""
import json
import os
import subprocess
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ACCOUNT = os.environ.get('AWS_ACCOUNT_ID', '272423022449')
PROFILE = os.environ.get('AWS_PROFILE', 'dci')
REGION = 'eu-central-1'
TOPIC = f'arn:aws:sns:{REGION}:{ACCOUNT}:customer-events'
AWS = os.environ.get('AWS_BIN', 'aws')
PORT = int(os.environ.get('PORT', '8790'))
DIST = Path(__file__).resolve().parent / 'frontend' / 'dist'

EVENT = {'type': 'order.shipped', 'orderId': 'A-2001', 'customer': 'Lena Hoffmann', 'email': 'lena@example.com'}
sent = {'good': None}
lock = threading.Lock()


def aws(*args):
    cmd = [AWS, *args, '--profile', PROFILE, '--region', REGION, '--output', 'json', '--no-cli-pager']
    done = subprocess.run(cmd, capture_output=True, text=True, timeout=25)
    if done.returncode:
        raise RuntimeError(done.stderr.strip() or 'AWS call failed')
    return json.loads(done.stdout) if done.stdout.strip() else {}


def was_logged():
    if not sent['good']:
        return False
    logs = aws('logs', 'filter-log-events', '--log-group-name', '/aws/lambda/notification-lambda',
               '--start-time', str(int((sent['good'] - 2) * 1000)), '--filter-pattern', '"messageId"')
    for entry in logs.get('events', []):
        text = entry['message']
        try:
            line = json.loads(text[text.index('{'):])
        except ValueError:
            continue
        if line.get('orderId') == EVENT['orderId']:
            return True
    return False


def state():
    return {**sent, 'logged': was_logged()}


def ship():
    with lock:
        started = time.time()
        aws('sns', 'publish', '--topic-arn', TOPIC, '--message', json.dumps(EVENT))
        sent['good'] = started


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
        if self.path != '/api/good':
            return self.reply(404, {'error': 'not found'})
        try:
            ship()
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
