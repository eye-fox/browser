import asyncio
import os
import json
import shutil
import subprocess
import time
import tempfile
import urllib.request
from pathlib import Path
from browser_use import Agent, Browser, ChatGoogle


def find_chrome():
    candidates = [
        '/usr/bin/google-chrome-stable',
        '/usr/bin/google-chrome',
        '/usr/bin/chromium-browser',
        '/usr/bin/chromium',
    ]
    for p in candidates:
        if Path(p).exists():
            return p
    return None


async def main():
    task = os.environ.get('TASK', 'Buka google.com dan screenshot')

    llm = ChatGoogle(model='gemini-2.0-flash-001')

    port = 9222
    user_dir = tempfile.mkdtemp(prefix='chrome-')

    chrome_path = find_chrome()
    print(f'Chrome: {chrome_path}')

    proc = subprocess.Popen(
        [
            chrome_path,
            f'--remote-debugging-port={port}',
            f'--user-data-dir={user_dir}',
            '--headless=new',
            '--no-sandbox',
            '--disable-dev-shm-usage',
            '--disable-gpu',
            '--no-first-run',
            '--no-default-browser-check',
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    print(f'Chrome PID: {proc.pid}')

    for i in range(30):
        try:
            r = urllib.request.urlopen(f'http://127.0.0.1:{port}/json/version', timeout=2)
            if r.status == 200:
                print(f'CDP ready on port {port}')
                break
        except Exception:
            pass
        time.sleep(1)
    else:
        proc.kill()
        raise RuntimeError('Chrome failed to start')

    cdp_url = f'http://127.0.0.1:{port}'
    browser = Browser(cdp_url=cdp_url)

    sensitive_data = {}
    if os.environ.get('SHOPIFY_EMAIL'):
        sensitive_data['shopify_email'] = os.environ['SHOPIFY_EMAIL']
    if os.environ.get('SHOPIFY_PASS'):
        sensitive_data['shopify_pass'] = os.environ['SHOPIFY_PASS']

    agent = Agent(
        task=task,
        llm=llm,
        browser=browser,
        sensitive_data=sensitive_data if sensitive_data else None,
    )

    try:
        history = await agent.run()

        output_dir = Path('output')
        output_dir.mkdir(exist_ok=True)

        for i, path in enumerate(history.screenshots()):
            if path and Path(path).exists():
                shutil.copy2(path, output_dir / f'screenshot_{i}.png')

        final = history.final_result()

        result = {
            'task': task,
            'status': 'completed',
            'final_result': final,
        }

        output_dir.joinpath('result.json').write_text(json.dumps(result, indent=2))
        print(json.dumps(result, indent=2))
        print('\n=== SELESAI ===')
    finally:
        proc.kill()
        try:
            shutil.rmtree(user_dir, ignore_errors=True)
        except Exception:
            pass


if __name__ == '__main__':
    asyncio.run(main())
