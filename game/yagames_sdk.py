# coding=utf-8
from __future__ import unicode_literals
import emscripten
import json

__version__ = '0.0.1'

LOAD_INIT_JS_CODE = """
let script = document.createElement('script');
window.yagames_script = script;
script.onload = function () {{
    window.yagames_script = null;
    YaGames
        .init({params})
        .then(ysdk => {{
            console.log('Yandex SDK initialized');
            {post_init}
        }}).catch(error => {{ {failed} }});
}};
script.async = false;
script.src = {script_url};
document.head.appendChild(script);
"""
EXECUTE_INIT_JS_CODE = """
if(window.yagames_script){{
    window.yagames_script.addEventListener('load', () => {{
        YaGames.init().then(ysdk => {{ {code} }})
    }}, {{once: true}});
}}
else{{
    YaGames.init().then(ysdk => {{ {code} }});
}}
"""

DEFAULT_SCRIPT_URL = 'https://yandex.ru/games/sdk/v2'


def js_value(string):
    return json.dumps(string, ensure_ascii=False)


def init(params=None, script_url=DEFAULT_SCRIPT_URL, post_init='', failed=''):
    if params is None:
        params_code = ''
    else:
        params_code = js_value(params)
    emscripten.run_script(
        LOAD_INIT_JS_CODE.format(params=params_code, script_url=js_value(script_url), post_init=post_init, failed=failed)
    )


def execute_raw(code):
    emscripten.run_script(EXECUTE_INIT_JS_CODE.format(code=code))


def execute_method(method, args=(), then=None, catch=None):
    if isinstance(args, dict):
        args_code = js_value(args)
    elif isinstance(args, (list, tuple)):
        args_code = ', '.join(js_value(arg) for arg in args)
    else:
        args_code = ''

    code = 'ysdk.%s(%s)' % (method, args_code)
    if then:
        code += '.then(value => {%s})' % then
    if catch:
        code += '.catch(error => {%s})' % catch

    execute_raw(code)


__all__ = ['init', 'execute_raw', 'execute_method', 'js_value']
