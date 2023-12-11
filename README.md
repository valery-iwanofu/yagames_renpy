# yagames_renpy
yagames_renpy - это скромная обёртка над Yandex Game SDK для Ren'Py.

## Задействованные JS переменные
* **ysdk** - во всём JS коде, который взаимодействует с SDK будет доступна эта переменная
* **value** - доступна в *then* callback'ах 
* **error** - доступна в *catch* callback'ах

## Установка
Перейдите [последнему релизу](https://github.com/valery-iwanofu/yagames_renpy/releases/latest), скачайте файл [yagames_sdk.py](https://github.com/valery-iwanofu/yagames_renpy/releases/latest/download/yagames_sdk.py) и поместите его в директорию game вашего Ren'Py проекта.

## Инициализация

```renpy
init python:
    if renpy.emscripten:
        import yagames_sdk
        import emscripten
        
        # Инициализируем SDK
        # Смотрите https://yandex.ru/dev/games/doc/ru/sdk/sdk-about#use и
        # https://yandex.ru/dev/games/doc/ru/sdk/sdk-about#extra
        yagames_sdk.init(params=..., post_init='console.log(ysdk);')
    else:
        yagames_sdk = None
```

## Использование
### Исполнение метода без обратного вызова
```renpy
$ yagames_sdk.execute_method('adv.showFullscreenAdv')
```

### Исполнение метода с обратным вызовом
```renpy
yagames_sdk.execute_method('getPlayer', then='window.ya_player = value; console.log(value)', catch='console.log(error);')
```

## Функции модуля yagames_sdk

### `def init(params=None, script_url='https://yandex.ru/games/sdk/v2', post_init='', failed='')`
Загружает скрипт SDK, а затем инициализирует его
* params - параметры инициализации (см. https://yandex.ru/dev/games/doc/ru/sdk/sdk-about#extra)
* script_url - ссылка на скрипт Yandex Game SDK для загрузки
* post_init - JS код для исполнения после успешной загрузки SDK
* failed - JS код для исполнения после неудачной загрузки SDK

### `def execute_raw(code)`
Исполняет JS код в контексте SDK
* code - код для исполнения(для взаимодействия с SDK доступная переменная ysdk)

### `def execute_method(method, args=(), then=None, catch=None)`
Вызывает метод SDK. Никаких проверок при вызове не происходит, так что будьте аккуратнее при использовании
* method - полный путь до метода(например `features.LoadingAPI?.ready`)
* args - аргументы передаваемые для вызова. Это может быть список или картеж, а также словарь
* * Кортеж и список будет форматирован так - `methodName(firstArg, secondArg)`
* * Словарь будет форматирован так - `methodName({firstKey: firstArg})`
* then - код, который будет вызван в случае успеха.
* catch - код, который будет вызван в случае провала.
Внимание! Не все методы поддерживают then или catch. Внимательно читайте документацию к Yandex Game SDK.

