from .commands import on_keydown

def game_on_keydown(event):
    actions = []

    act = on_keydown(event)
    if act:
        actions.append(act)

    return actions