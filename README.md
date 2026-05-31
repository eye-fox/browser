# Browser Agent

GitHub Actions runner sebagai cloud browser-use.

## Trigger dari HP

```bash
curl -X POST https://api.github.com/repos/eye-fox/browser/dispatches \
  -H "Authorization: Bearer ghp_token_anda" \
  -H "Accept: application/vnd.github.v3+json" \
  -d '{"event_type":"run-task","client_payload":{"task":"Login ke shopify dengan email {{shopify_email}} dan password {{shopify_pass}}, screenshot dashboard"}}'
```

Atau pake script:

```bash
./trigger.sh "Login ke shopify dengan email {{shopify_email}} dan password {{shopify_pass}}, screenshot dashboard"
```

## Cek hasil

1. Buka https://github.com/eye-fox/browser/actions
2. Klik workflow yang running
3. Download artifacts (screenshot, result.json)

## Format task

Gunakan `{{shopify_email}}` dan `{{shopify_pass}}` di task untuk kredensial.
