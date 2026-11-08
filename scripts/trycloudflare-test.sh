#!/usr/bin/env bash
set -euo pipefail
project_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
command -v cloudflared >/dev/null || { echo 'Install cloudflared first.'; exit 1; }
export EVIDENCETWIN_DATA_DIRECTORY
EVIDENCETWIN_DATA_DIRECTORY="$(mktemp -d "${TMPDIR:-/tmp}/evidencetwin-public-test.XXXXXX")"
export EVIDENCETWIN_ACCOUNTS=1 EVIDENCETWIN_SECURE_COOKIES=1
pids=()
cleanup() {
  for pid in "${pids[@]}"; do kill "$pid" 2>/dev/null || true; done
}
trap cleanup EXIT
trap 'exit 130' INT TERM
printf 'Separate test workspace saved at %s\n' "$EVIDENCETWIN_DATA_DIRECTORY"
cd "$project_dir/backend"
echo 'Create the tester login with a password of 12–256 characters. Typing stays hidden.'
until .venv/bin/python -m evidencetwin_backend.accounts invite-researcher --name tester --operator; do
  read -r -p 'Try creating the login again? [Y/n] ' retry_account
  case "$retry_account" in
    n|N|no|NO) exit 1 ;;
  esac
done
cloudflared tunnel --url http://127.0.0.1:5204 >"$EVIDENCETWIN_DATA_DIRECTORY/tunnel.log" 2>&1 &
pids+=("$!")
tunnel_url=''
for attempt in {1..60}; do
  tunnel_url="$(sed -nE 's@.*(https://[a-z0-9-]+\.trycloudflare\.com).*@\1@p' "$EVIDENCETWIN_DATA_DIRECTORY/tunnel.log" | head -1)"
  [[ -n "$tunnel_url" ]] && break
  kill -0 "${pids[0]}" 2>/dev/null || { cat "$EVIDENCETWIN_DATA_DIRECTORY/tunnel.log"; exit 1; }
  sleep 1
done
[[ -n "$tunnel_url" ]] || { echo 'Tunnel URL unavailable. Check tunnel.log in the test workspace.'; exit 1; }
export EVIDENCETWIN_CORS_ORIGINS="$tunnel_url"
.venv/bin/python -m flask --app evidencetwin_backend:create_app run --host 127.0.0.1 --port 5004 --no-debugger --no-reload >"$EVIDENCETWIN_DATA_DIRECTORY/backend.log" 2>&1 &
pids+=("$!")
cd "$project_dir/frontend"
FLASK_DEV_ORIGIN=http://127.0.0.1:5004 VITE_API_BASE_URL=/api __VITE_ADDITIONAL_SERVER_ALLOWED_HOSTS="${tunnel_url#https://}" npm run dev -- --host 127.0.0.1 --port 5204 --strictPort >"$EVIDENCETWIN_DATA_DIRECTORY/frontend.log" 2>&1 &
pids+=("$!")
for attempt in {1..30}; do
  if curl --fail --silent http://127.0.0.1:5004/api/health >/dev/null && curl --fail --silent http://127.0.0.1:5204/app >/dev/null; then
    printf '\nOpen %s/app\nSign in as tester with the password you just set.\nPress Ctrl+C to stop. Test data remains in %s\n' "$tunnel_url" "$EVIDENCETWIN_DATA_DIRECTORY"
    wait -n "${pids[@]}"
    exit $?
  fi
  for pid in "${pids[@]}"; do
    kill -0 "$pid" 2>/dev/null || { echo "Startup failed. Read logs in $EVIDENCETWIN_DATA_DIRECTORY"; exit 1; }
  done
  sleep 1
done
echo "Startup timed out. Read logs in $EVIDENCETWIN_DATA_DIRECTORY"
exit 1
