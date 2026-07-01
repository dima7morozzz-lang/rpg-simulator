import random
import flet as ft


def main(page: ft.Page):
    # Настройки окна-смартфона
    page.title = "RPG Heist Simulator"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 380
    page.window_height = 800

    # Игровое состояние
    state = {
        "level": 1,
        "money": 0,
        "luck": 1,
        "charisma": 1,
        "smoke_bombs": 0,
        "secret_code": random.randint(1, 4),
        "attempts": 2,
        "phase": "intro",
    }

    # --- ЭЛЕМЕНТЫ ЧИТ-МЕНЮ ---
    def check_dev_code(e):
        if dev_input.value == "2123":
            dev_input.visible = False
            dev_submit_btn.visible = False
            cheat_level_box.visible = True
            log_text.value = "🔓 Режим разработчика! Введите уровень от 1 до 50."
        else:
            log_text.value = "❌ Неверный секретный код."
        dev_input.value = ""
        page.update()

    def jump_to_level_cheat(e):
        try:
            target_lvl = int(cheat_level_input.value)
            if not (1 <= target_lvl <= 50):
                log_text.value = "❌ Введите число строго от 1 до 50!"
                cheat_level_input.value = ""
                page.update()
                return
        except ValueError:
            log_text.value = "❌ Введите корректное целое число!"
            cheat_level_input.value = ""
            page.update()
            return

        # Начисляем деньги за все пропущенные уровни
        skipped_levels = target_lvl - state["level"]
        if skipped_levels > 0:
            total_bonus = sum(i * 1000 for i in range(state["level"], target_lvl))
            state["money"] += total_bonus
        else:
            total_bonus = 0

        state["level"] = target_lvl
        state["phase"] = "shop"
        state["secret_code"] = random.randint(1, 3 + state["level"])

        cheat_level_box.visible = False
        dev_box.visible = False
        cheat_level_input.value = ""

        status_text.value = "ЧЕРНЫЙ РЫНОК"
        log_text.value = (
            f"⚡ Чит-код успешно активирован!\nВы прыгнули на уровень {target_lvl}.\n"
            f"Вам начислено ${total_bonus} бонуса."
        )

        shop_box.visible = True
        action_button.visible = True
        action_button.text = "Идти на следующее ограбление"

        update_stats()

    dev_btn = ft.TextButton(
        "КОД",
        on_click=lambda _: setattr(dev_box, "visible", not dev_box.visible) or page.update(),
    )

    dev_input = ft.TextField(
        label="Пароль",
        password=True,
        can_reveal_password=True,
        width=120,
        height=40,
        text_size=12,
    )
    dev_submit_btn = ft.ElevatedButton("ОК", on_click=check_dev_code, height=40)
    dev_box = ft.Row([dev_input, dev_submit_btn], visible=False, alignment=ft.MainAxisAlignment.CENTER)

    cheat_level_input = ft.TextField(
        label="Уровень (1-50)",
        width=140,
        height=40,
        text_size=12,
        text_align=ft.TextAlign.CENTER
    )
    cheat_level_btn = ft.ElevatedButton("Прыжок", on_click=jump_to_level_cheat, height=40)
    cheat_level_box = ft.Row([cheat_level_input, cheat_level_btn], visible=False, alignment=ft.MainAxisAlignment.CENTER)

    # --- ОСНОВНЫЕ ЭЛЕМЕНТЫ ИНТЕРФЕЙСА ---
    status_text = ft.Text(
        "СТАДИЯ 1: Кооператив 'Крестьянский Капитал'",
        size=16,
        weight=ft.FontWeight.BOLD,
        color="amber",
        text_align=ft.TextAlign.CENTER,
    )

    stats_text = ft.Text(
        "Баланс: $0 | Удача: 1 | Харизма: 1 | Шашки: 0",
        size=12,
        color="grey400",
        text_align=ft.TextAlign.CENTER,
    )

    log_text = ft.Text(
        "Вы стоите перед входом в банк. Пора начать ограбление века!",
        size=14,
        text_align=ft.TextAlign.CENTER,
    )

    code_input = ft.TextField(
        label="Введите цифру", visible=False, width=150, text_align=ft.TextAlign.CENTER
    )
    custom_submit_btn = ft.ElevatedButton("Ввод кода", visible=False, width=150)

    action_button = ft.ElevatedButton(
        "Войти в банк", color="black", bgcolor="amber", width=250
    )

    shop_box = ft.Column(visible=False, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    # --- ЛОГИКА ИГРЫ ---
    def update_stats():
        stats_text.value = f"Баланс: ${state['money']} | Удача: {state['luck']} | Харизма: {state['charisma']} | Шашки: {state['smoke_bombs']}"
        page.update()

    def buy_item(item_type):
        if item_type == "luck" and state["money"] >= 500:
            state["money"] -= 500
            state["luck"] += 1
            log_text.value = "Куплен талисман удачи! Теперь сейфы взламывать легче."
        elif item_type == "charisma" and state["money"] >= 500:
            state["money"] -= 500
            state["charisma"] += 1
            log_text.value = "Вы прошли экспресс-курсы дипломатии. Охранникам сложнее вас поймать."
        elif item_type == "smoke" and state["money"] >= 300:
            state["money"] -= 300
            state["smoke_bombs"] += 1
            log_text.value = "Куплена дымовая шашка! Она автоматически спасет от одной ошибки."
        else:
            log_text.value = "Ошибка: Недостаточно денег на балансе!"
        update_stats()

    def reset_game():
        state["level"] = 1
        state["money"] = 0
        state["luck"] = 1
        state["charisma"] = 1
        state["smoke_bombs"] = 0
        state["secret_code"] = random.randint(1, 4)
        state["phase"] = "intro"
        status_text.color = "amber"
        status_text.value = "СТАДИЯ 1: Кооператив 'Крестьянский Капитал'"
        log_text.value = "Новая попытка! Вы снова стоите перед дверями первого банка."
        action_button.text = "Войти в банк"
        shop_box.visible = False
        code_input.visible = False
        custom_submit_btn.visible = False
        update_stats()

    def handle_action(e):
        if state["phase"] == "game_over" or state["phase"] == "victory":
            reset_game()
            return

        max_digit = 3 + state["level"]
        guard_power = 2 + state["level"]

        if state["phase"] == "intro":
            state["phase"] = "guard"
            status_text.value = f"Уровень {state['level']}/50: Пост охраны"
            log_text.value = f"Вас окликнул охранник (Сложность: {guard_power}). Пытаемся заговорить ему зубы..."
            action_button.text = "Проверить Харизму (Бросить кубик)"

        elif state["phase"] == "guard":
            roll = random.randint(1, 6) + state["charisma"]
            if roll >= guard_power:
                state["phase"] = "safe"
                state["attempts"] = 2
                status_text.value = f"Уровень {state['level']}/50: Взлом сейфа"

                hint = ""
                if state["luck"] >= 3:
                    wrong = random.choice([i for i in range(1, max_digit + 1) if i != state["secret_code"]])
                    hint = f"\n(Интуиция подсказывает, что код точно НЕ {wrong})"

                log_text.value = f"Успех! Охранник поверил вашей лжи (Бросок: {roll}).\nВы пробрались к сейфу. Угадайте число от 1 до {max_digit}.{hint}"

                action_button.visible = False
                code_input.visible = True
                code_input.label = f"Число (1-{max_digit})"
                custom_submit_btn.visible = True
            else:
                loss = int(state["money"] * 0.3)
                state["money"] -= loss
                state["phase"] = "game_over"
                status_text.value = "ЗАДЕРЖАНИЕ"
                status_text.color = "red"
                log_text.value = f"Вас раскусили и скрутили! Пришлось отдать ${loss} на адвокатов."
                action_button.text = "Начать заново"

        elif state["phase"] == "shop":
            state["level"] += 1
            state["phase"] = "intro"
            state["secret_code"] = random.randint(1, 3 + state["level"])
            shop_box.visible = False
            action_button.text = "Войти в следующий банк"
            status_text.value = f"СТАДИЯ {state['level']}"
            log_text.value = f"Вы перешли к банку уровня {state['level']}. Системы защиты стали сложнее!"

        page.update()

    def handle_code_submit(e):
        loot = state["level"] * 1000

        try:
            val = int(code_input.value)
        except ValueError:
            log_text.value = "Ошибка: Введите корректное ЦЕЛОЕ число!"
            code_input.value = ""  # Очищаем поле ввода при неверном типе данных
            page.update()
            return

        if val == state["secret_code"]:
            state["money"] += loot
            code_input.visible = False
            custom_submit_btn.visible = False
            code_input.value = ""

            # ПРОВЕРКА НА ПОБЕДУ В ИГРЕ
            if state["level"] >= 50:
                state["phase"] = "victory"
                status_text.value = "🏆 ПОБЕДА! 🏆"
                status_text.color = "green"
                log_text.value = f"Вы успешно взломали финальный 50-й сейф и забрали ${loot}!\n\nПоздравляем, вы прошли! Продолжение следует..."
                action_button.visible = True
                action_button.text = "Играть снова"
                shop_box.visible = False
            else:
                state["phase"] = "shop"
                status_text.value = "ЧЕРНЫЙ РЫНОК"
                log_text.value = f"Отлично! Сейф открыт, вы забрали ${loot}.\nПрокачайте навыки перед следующим делом."
                action_button.visible = True
                action_button.text = "Идти на следующее ограбление"
                shop_box.visible = True
        else:
            state["attempts"] -= 1
            code_input.value = ""  # ОЧИСТКА СТРОКИ УГАДЫВАНИЯ ЧИСЛА при неверной попытке

            if state["smoke_bombs"] > 0 and state["attempts"] > 0:
                state["smoke_bombs"] -= 1
                state["attempts"] += 1
                log_text.value = "Неверно! Но вы бросили дымовую шашку, выиграв себе еще одну попытку!"
            elif state["attempts"] > 0:
                log_text.value = f"Код не подходит! Сейф издает писк. Осталось попыток: {state['attempts']}"
            else:
                code_input.visible = False
                custom_submit_btn.visible = False
                state["phase"] = "game_over"
                status_text.value = "ФИНИШ ИГРЫ"
                status_text.color = "red"
                log_text.value = f"🚨 Сработала сигнализация! Приехал спецназ.\nВы дошли до {state['level']} уровня и накопили ${state['money']}."
                action_button.visible = True
                action_button.text = "Начать заново"

        update_stats()

    action_button.on_click = handle_action
    custom_submit_btn.on_click = handle_code_submit

    shop_box.controls = [
        ft.Text("Доступные улучшения:", size=14, weight=ft.FontWeight.W_500),
        ft.Container(height=5),
        ft.Column(
            [
                ft.ElevatedButton("Удача ($500)", on_click=lambda x: buy_item("luck"), width=180),
                ft.ElevatedButton("Харизма ($500)", on_click=lambda x: buy_item("charisma"), width=180),
                ft.ElevatedButton("Шашка ($300)", on_click=lambda x: buy_item("smoke"), width=180),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8,
        ),
        ft.Container(height=15),
    ]

    # Сборка интерфейса
    page.add(
        ft.Row(
            [
                ft.Container(
                    content=ft.Column(
                        [
                            dev_btn,
                            dev_box,
                            cheat_level_box,
                            ft.Divider(),
                            status_text,
                            stats_text,
                            ft.Container(
                                content=log_text,
                                padding=15,
                                bgcolor="#252830",
                                border_radius=10,
                                height=160,
                            ),
                            ft.Container(height=10),
                            code_input,
                            custom_submit_btn,
                            shop_box,
                            action_button,
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    padding=20,
                    border_radius=25,
                    bgcolor="#101216",
                    width=350,
                    height=750,
                    alignment=ft.Alignment(0, -1),
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )


if __name__ == "__main__":
    ft.app(target=main)