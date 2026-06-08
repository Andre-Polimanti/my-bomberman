import pygame
from collections import deque

MOVE_DELAY = 200
BOMB_DANGER_TIME = 1500
BOMB_RANGE = 5


class BotPlayer:
    def __init__(self, player):
        self.player = player
        self.last_move_time = -MOVE_DELAY

    def update(self, app):
        if not self.player.is_alive or app.champion:
            return None

        now = pygame.time.get_ticks()
        if now - self.last_move_time < MOVE_DELAY:
            return None

        player = self.player
        map_ = player.map

        danger_tiles = self._get_danger_tiles(app.bomb_manager)
        enemies = [p for p in app.player_manager.players if p.is_alive and p != player]

        if not enemies:
            return None

        # Priority 1: flee if standing on a dangerous tile
        if player.position in danger_tiles:
            safe_pos = self._bfs_find_safe(player.position, danger_tiles, map_, app.bomb_manager)
            if safe_pos:
                next_step = self._bfs_next_step(player.position, safe_pos, map_, app.bomb_manager)
                if next_step:
                    self._step_to(player, next_step)
                    self.last_move_time = now
            return None

        # Priority 2: bomb an enemy in line of sight if no active bomb from this bot
        has_own_bomb = any(b.team == player.team for b in app.bomb_manager.active_bombs)
        if not has_own_bomb:
            for enemy in enemies:
                target_pos = self._can_bomb_enemy(player, enemy, map_)
                if target_pos:
                    self.last_move_time = now
                    return {"type": "PLAY", "action": "BOMBING", "player": player, "pos": target_pos}

        # Priority 3: move towards nearest enemy
        nearest = min(
            enemies,
            key=lambda e: abs(e.position[0] - player.position[0]) + abs(e.position[1] - player.position[1])
        )
        next_step = self._bfs_next_step(player.position, nearest.position, map_, app.bomb_manager)
        if next_step:
            self._step_to(player, next_step)
            self.last_move_time = now

        return None

    # --- movement helpers ---

    def _step_to(self, player, target):
        dx = target[0] - player.position[0]
        dy = target[1] - player.position[1]
        player.face_to_dir(dx, dy)
        player.walk()

    # --- pathfinding ---

    def _bfs_next_step(self, start, goal, map_, bomb_manager):
        """Return the first step of the shortest walkable path from start to goal."""
        if start == goal:
            return None

        bomb_positions = {b.position for b in bomb_manager.active_bombs if b.state == "TICKING"} if bomb_manager else set()

        queue = deque([(start, None)])
        visited = {start}

        while queue:
            current, first_step = queue.popleft()
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = current[0] + dx, current[1] + dy
                next_pos = (nx, ny)
                if next_pos in visited:
                    continue

                pixel = map_.get_pixel(nx, ny)
                if not pixel or pixel.obstructed or next_pos in bomb_positions:
                    continue

                step = first_step if first_step else next_pos

                if next_pos == goal:
                    return step

                if not pixel.occupied:
                    visited.add(next_pos)
                    queue.append((next_pos, step))

        return None

    def _bfs_find_safe(self, start, danger_tiles, map_, bomb_manager):
        """Return the nearest tile that is not in danger_tiles."""
        if start not in danger_tiles:
            return start

        bomb_positions = {b.position for b in bomb_manager.active_bombs if b.state == "TICKING"}
        queue = deque([start])
        visited = {start}

        while queue:
            current = queue.popleft()
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = current[0] + dx, current[1] + dy
                next_pos = (nx, ny)
                if next_pos in visited:
                    continue

                pixel = map_.get_pixel(nx, ny)
                if not pixel or pixel.obstructed or next_pos in bomb_positions:
                    continue

                if next_pos not in danger_tiles:
                    return next_pos

                visited.add(next_pos)
                queue.append(next_pos)

        return None

    # --- danger & bombing ---

    def _get_danger_tiles(self, bomb_manager):
        danger = set()
        now = pygame.time.get_ticks()

        for bomb in bomb_manager.active_bombs:
            if bomb.state == "TICKING":
                time_left = 2000 - (now - bomb.creation_time)
                if time_left <= BOMB_DANGER_TIME:
                    danger.update(self._predicted_blast(bomb))
            elif bomb.state in ("EXPLODING", "LINGERING"):
                danger.update(bomb.fire_coords)

        return danger

    def _predicted_blast(self, bomb):
        coords = {bomb.position}
        x, y = bomb.position
        for i, (dx, dy) in enumerate([(1, 0), (0, 1), (-1, 0), (0, -1)]):
            for r in range(1, bomb.ranges[i] + 1):
                coords.add((x + dx * r, y + dy * r))
        return coords

    def _can_bomb_enemy(self, player, enemy, map_):
        """
        Return a valid bomb placement position if enemy is reachable by blast,
        otherwise return None.
        """
        px, py = player.position
        ex, ey = enemy.position

        # same row
        if py == ey and px != ex:
            dx = 1 if ex > px else -1
            dist = abs(ex - px)
            if dist <= BOMB_RANGE + 1 and self._clear_line(map_, px, py, dx, 0, dist):
                player.face_to_dir(dx, 0)
                target = player.get_valid_target()
                if target:
                    return target

        # same column
        if px == ex and py != ey:
            dy = 1 if ey > py else -1
            dist = abs(ey - py)
            if dist <= BOMB_RANGE + 1 and self._clear_line(map_, px, py, 0, dy, dist):
                player.face_to_dir(0, dy)
                target = player.get_valid_target()
                if target:
                    return target

        return None

    def _clear_line(self, map_, px, py, dx, dy, dist):
        """Check that tiles between player and enemy (exclusive of both) are not obstructed."""
        for i in range(2, dist):
            pixel = map_.get_pixel(px + dx * i, py + dy * i)
            if pixel is None or pixel.obstructed:
                return False
        return True
