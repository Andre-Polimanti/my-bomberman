import pygame

MOVE_DELAY = 150
TYPE = "PLAY"

def on_keydown(player, player_controls, event):
    if (event.key not in player_controls["move_keys"] and event.key != player_controls["bomb_key"]) \
    or player.lives == False:
        return
    
    p = player
    controls = player_controls

    if event.key in controls["move_keys"]:
        dx, dy = controls["move_keys"][event.key]
        
        p.face_to_dir(dx, dy)
        
        if controls["last_instr"] == event.key:
            p.walk()
    
        controls["last_time"] = pygame.time.get_ticks()
        controls["last_instr"] = event.key
            
    elif event.key == controls["bomb_key"]:
        target_pos = p.get_valid_target()

        if target_pos:
            return {"type": TYPE, "action": "BOMBING", "player": p, "pos": target_pos}

def on_keyhold(player, player_controls):
    p = player
    controls = player_controls

    if player.lives == False:
        return

    now = pygame.time.get_ticks()
    keys = pygame.key.get_pressed()

    for key in controls["move_keys"]:
        if keys[key]: 
            if key == controls["last_instr"]:
                if now - controls["last_time"] >= MOVE_DELAY:
                    p.walk()
                    controls["last_time"] = now
                    break