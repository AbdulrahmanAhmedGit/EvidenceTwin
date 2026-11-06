"""Private, atomic server configuration. Keys never enter public representations."""
import json
import os
from pathlib import Path
from urllib.parse import urlsplit
from uuid import uuid4
from werkzeug.exceptions import UnprocessableEntity
from ..contracts.ai import AISettingsInput, AISettingsPublic
from ..contracts.common import validate_contract
from .transports import make_provider

PROVIDER_NAMES = {'ollama':'Ollama','openai':'OpenAI','google':'Google Gemini','anthropic':'Anthropic','openrouter':'OpenRouter','deepseek':'DeepSeek'}

class AISettings:
    def __init__(self, root: Path, config: dict, lock):
        self.path=root/'provider-settings.json'
        self.base=dict(config)
        self.lock=lock
        self.saved={'activeProvider':config['AI_PROVIDER'],'providers':{}}
        if self.path.exists():
            # The file is local server configuration, never a browser download.
            self.path.chmod(0o600)
            self.saved=json.loads(self.path.read_text())
            if self.saved.get('activeProvider') not in PROVIDER_NAMES or not isinstance(self.saved.get('providers'),dict):
                raise ValueError('Invalid saved provider configuration')

    def effective(self, name: str | None = None, saved: dict | None = None) -> dict:
        state=self.saved if saved is None else saved
        name=name or state['activeProvider']
        entry=state['providers'].get(name,{})
        config={**self.base,'AI_PROVIDER':name}
        config['AI_MODEL']=entry.get('model',self.base['AI_MODEL'] if name==self.base['AI_PROVIDER'] else '')
        env_key=self.base.get('AI_PROVIDER_KEYS',{}).get(name,'')
        if name==self.base['AI_PROVIDER'] and not env_key: env_key=self.base['AI_API_KEY']
        key=entry.get('apiKey') or env_key
        config.update(AI_API_KEY=key,OLLAMA_API_KEY=key,OLLAMA_MODEL=config['AI_MODEL'])
        config['OLLAMA_HOST']=entry.get('ollamaHost',self.base['OLLAMA_HOST'])
        if 'ollamaHost' in entry:
            config['OLLAMA_SCHEMA_MODE']=urlsplit(config['OLLAMA_HOST']).hostname!='ollama.com'
        return config

    def public(self) -> dict:
        with self.lock:
            items=[]
            for name,label in PROVIDER_NAMES.items():
                config=self.effective(name)
                provider=make_provider(config)
                entry=self.saved['providers'].get(name,{})
                key=config['AI_API_KEY']
                item={'id':name,'name':label,'model':config['AI_MODEL'],'configured':provider.configured,
                      'keyConfigured':bool(key),'keySource':'server' if entry.get('apiKey') else 'environment' if key else 'none',
                      'requiresKey':name!='ollama' or urlsplit(config['OLLAMA_HOST']).hostname=='ollama.com'}
                if name=='ollama': item['ollamaHost']=config['OLLAMA_HOST']
                items.append(item)
            return validate_contract(AISettingsPublic,{'activeProvider':self.saved['activeProvider'],'providers':items})

    def save(self, payload: dict):
        data=validate_contract(AISettingsInput,payload)
        name=data['provider']
        if data.get('removeKey') and data.get('apiKey'): raise UnprocessableEntity()
        if name!='ollama' and 'ollamaHost' in data: raise UnprocessableEntity()
        if name=='ollama':
            host=data.get('ollamaHost',self.effective(name)['OLLAMA_HOST']).rstrip('/')
            url=urlsplit(host)
            try: _=url.port
            except ValueError: raise UnprocessableEntity() from None
            if url.scheme not in ('http','https') or not url.hostname or url.username or url.password or url.path or url.query or url.fragment or any(c.isspace() for c in host): raise UnprocessableEntity()
            if url.scheme=='http' and url.hostname not in ('localhost','127.0.0.1','::1'): raise UnprocessableEntity()
            data['ollamaHost']=host
        with self.lock:
            # Build/validate the whole replacement before touching the durable file.
            state=json.loads(json.dumps(self.saved))
            entry=state['providers'].setdefault(name,{})
            entry['model']=data['model']
            if data.get('removeKey'):
                if not entry.get('apiKey'): raise UnprocessableEntity()
                entry.pop('apiKey',None)
            if data.get('apiKey'): entry['apiKey']=data['apiKey']
            if name=='ollama': entry['ollamaHost']=data['ollamaHost']
            state['activeProvider']=name
            provider=make_provider(self.effective(name,state))
            temporary=self.path.with_name('.provider-settings-'+uuid4().hex)
            try:
                descriptor=os.open(temporary,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
                with os.fdopen(descriptor,'w') as stream:
                    json.dump(state,stream,ensure_ascii=False)
                    stream.flush();os.fsync(stream.fileno())
                os.replace(temporary,self.path)
            finally:
                temporary.unlink(missing_ok=True)
            self.saved=state
            return provider
