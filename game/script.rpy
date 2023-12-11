init python:
    # Загружаем yagames_sdk только в веб версии игры
    if renpy.emscripten:
        import yagames_sdk
        import emscripten

        emscripten.run_script('window.ya_player = null;')
        
        # Инициализируем SDK
        yagames_sdk.init(post_init='console.log(ysdk);')
        # Делаем запрос на получение информации о текущем игроке и записываем её в переменную window.ya_player для дальнейшего использования
        yagames_sdk.execute_method('getPlayer', then='window.ya_player = value; console.log(value)', catch='console.log(error);')
    else:
        yagames_sdk = None
    
    # Вспомагательная обёртка, которая не позволяет вызвать функцию более одного раза
    class run_once:
        def __init__(self, func):
            self.func = func
            self.called = False
        
        def __call__(self):
            if self.called:
                return
            self.called = True
            return self.func()
    
    # https://yandex.ru/dev/games/doc/ru/sdk/sdk-gameready
    @run_once
    def game_started():
        if yagames_sdk:
            yagames_sdk.execute_method('features.LoadingAPI?.ready')
    
label before_main_menu:
    # https://yandex.ru/dev/games/doc/ru/sdk/sdk-gameready
    $ game_started()
    return

label start:
    if not yagames_sdk:
        'Запустите через браузер.'
        return

    menu:
        'Показать рекламу':
            $ yagames_sdk.execute_method('adv.showFullscreenAdv')
        'У меня есть адблок':
            'Блин('
            return
    
    'Невероятный контент доступный после просмотра рекламы!'

    return