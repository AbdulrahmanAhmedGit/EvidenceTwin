"""Invite-only local account boundary. No public registration or legacy import."""
from datetime import timedelta
import hashlib
import os
import secrets
import time
import click
from flask import g, jsonify, request, session
from werkzeug.exceptions import Unauthorized, Forbidden, NotFound, TooManyRequests, UnprocessableEntity
from werkzeug.security import generate_password_hash, check_password_hash
from .store import new_id, now


def principal():
    return getattr(g, 'researcher', {'id': 'local', 'role': 'operator', 'name': 'Local workspace'})


def operator():
    if principal()['role'] != 'operator':
        raise Forbidden()


def can_read(record):
    actor = principal()
    # Legacy records stay unassigned; only the operator can inspect them.
    return record.get('ownerId') == actor['id'] or (not record.get('ownerId') and actor['role'] == 'operator')


def owned(store, kind, record_id):
    record = store.get(kind, record_id)
    if not can_read(record):
        raise NotFound()
    return record


def install_access(app, store):
    enabled = app.config['ACCOUNTS_ENABLED']
    if not app.secret_key:
        key = store.root / 'session.key'
        if not key.exists():
            with open(key, 'x', opener=lambda path, flags: os.open(path, flags, 0o600)) as file:
                file.write(secrets.token_hex(48))
        app.secret_key = key.read_text().strip()
        key.chmod(0o600)
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=12)
    dummy_hash = generate_password_hash(secrets.token_hex(24)) if enabled else ''

    def session_info():
        actor = getattr(g, 'researcher', None)
        return jsonify({'accountsEnabled': enabled, 'authenticated': actor is not None,
                        'operator': actor is not None and actor['role'] == 'operator',
                        'name': actor['name'] if actor else None, 'workspaceId': actor['id'] if actor else None})

    @app.before_request
    def authorize():
        if not enabled:
            g.researcher = {'id': 'local', 'role': 'operator', 'name': 'Local workspace'}
        else:
            uid = session.get('uid')
            try:
                user = store.get('account', uid) if isinstance(uid, str) else None
            except NotFound:
                user = None
            if user and user.get('active') and session.get('version') == user.get('version', 1):
                g.researcher = {k: user[k] for k in ('id', 'role', 'name')}
            if request.path.startswith('/api/') and request.endpoint not in {
                'system.health', 'system.capabilities', 'access.session_info', 'access.login'
            } and not getattr(g, 'researcher', None) and request.method != 'OPTIONS':
                raise Unauthorized()
        # Role checks apply even when an external authorization hook is installed.
        if request.path.startswith('/api/settings/ai'):
            operator()

    def login():
        if not enabled:
            raise Forbidden()
        data = request.get_json(silent=True)
        if not isinstance(data, dict) or set(data) != {'name', 'password'} or not all(isinstance(v, str) for v in data.values()):
            raise UnprocessableEntity()
        if not 1 <= len(data['name']) <= 100 or not 1 <= len(data['password']) <= 256:
            raise UnprocessableEntity()
        # Persist throttling across application restarts; no password/IP is logged.
        identity = hashlib.sha256((request.remote_addr or '').encode()).hexdigest()
        with store.lock:
            try:
                throttle = store.get('login_limit', identity)
            except NotFound:
                throttle = {'id': identity, 'start': time.time(), 'failures': 0}
            if time.time() - throttle['start'] > 900:
                throttle.update(start=time.time(), failures=0)
            if throttle['failures'] >= 10:
                raise TooManyRequests()
            users = [u for u in store.all('account') if u['name'].casefold() == data['name'].casefold()]
            user = users[0] if users else None
            valid = check_password_hash(user['passwordHash'] if user else dummy_hash, data['password'])
            if not user or not valid or not user['active']:
                throttle['failures'] += 1
                store.put('login_limit', throttle)
                raise Unauthorized()
            throttle.update(failures=0)
            store.put('login_limit', throttle)
            session.clear()
            session.permanent = True
            session.update(uid=user['id'], version=user.get('version', 1))
            g.researcher = {k: user[k] for k in ('id', 'role', 'name')}
        return session_info()

    def logout():
        session.clear()
        g.researcher = None
        return '', 204

    app.add_url_rule('/api/session', 'access.session_info', session_info, methods=['GET'])
    app.add_url_rule('/api/session/login', 'access.login', login, methods=['POST'])
    app.add_url_rule('/api/session/logout', 'access.logout', logout, methods=['POST'])

    register_account_commands(app.cli, store)


def register_account_commands(cli, store):
    """Shared CLI commands; standalone entry point does not acquire a worker lock."""
    @cli.command('invite-researcher')
    @click.option('--name', prompt=True)
    @click.option('--operator', 'is_operator', is_flag=True)
    @click.password_option(confirmation_prompt=True)
    def invite(name, is_operator, password):
        """Provision an account without exposing passwords in arguments or logs."""
        if not 1 <= len(name.strip()) <= 100 or not 12 <= len(password) <= 256:
            raise click.ClickException('Use a name of 1–100 characters and a password of 12–256 characters.')
        with store.lock:
            if any(u['name'].casefold() == name.strip().casefold() for u in store.all('account')):
                raise click.ClickException('That account name already exists.')
            store.put('account', {'id': new_id(), 'name': name.strip(), 'role': 'operator' if is_operator else 'researcher',
                                 'active': True, 'version': 1, 'createdAt': now(), 'passwordHash': generate_password_hash(password)})
        click.echo('Account created. No legacy records were assigned.')

    @cli.command('disable-researcher')
    @click.option('--name', prompt=True)
    def disable(name):
        with store.lock:
            user = next((u for u in store.all('account') if u['name'].casefold() == name.casefold()), None)
            if not user:
                raise click.ClickException('Account not found.')
            user.update(active=False, version=user.get('version', 1) + 1)
            store.put('account', user)
        click.echo('Account disabled; existing sessions are revoked.')
