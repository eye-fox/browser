import asyncio
import os
import json
import shutil
from pathlib import Path
from browser_use import Agent, Browser, BrowserProfile, ChatGoogle


async def main():
    task = os.environ.get('TASK', 'Buka google.com dan screenshot')

    llm = ChatGoogle(model='gemini-3-flash-preview')

    profile = BrowserProfile(
        headless=True,
        args=['--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu'],
        chromium_sandbox=False,
    )
    browser = Browser(browser_profile=profile)

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

    history = await agent.run()

    output_dir = Path('output')
    output_dir.mkdir(exist_ok=True)

    # Copy screenshots
    for i, path in enumerate(history.screenshots()):
        if path and Path(path).exists():
            shutil.copy2(path, output_dir / f'screenshot_{i}.png')

    # Get final result
    final = history.final_result()

    result = {
        'task': task,
        'status': 'completed',
        'final_result': final,
    }

    output_dir.joinpath('result.json').write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))
    print('\n=== SELESAI ===')


if __name__ == '__main__':
    asyncio.run(main())
