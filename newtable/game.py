import arcade
import math
import random

SCREEN_WIDTH = 1289
SCREEN_HEIGHT = 726
SCREEN_TITLE = "Space Shooter"

PLAYER_SPEED = 4
PLAYER_TURN_SPEED = 4
PLAYER_SHOOT_COOLDOWN = 0.1

BULLET_SPEED = 9
BULLET_SCALE = 0.8

ENEMY_SPEED_MIN = 1
ENEMY_SPEED_MAX = 2
ENEMY_SPAWN_RATE = 4
ENEMY_SCALE = 0.3

ENEMY_TYPES = ["normal", "shooter"]
ENEMY_SHOOT_COOLDOWN = 3
ENEMY_BULLET_SPEED = 8
ENEMY_BULLET_COLOR = arcade.color.PARIS_GREEN

PARTICLE_COUNT = ([5,6,7,8])
PARTICLE_SPEED = 3
PARTICLE_FADE_RATE = 8

PowerUp_SPAWN_RATE = 6
SHIELD_TIMER = random.randint(8, 14)
HEALTH_TIMER = 2
BOMB_TIMER = 2
PowerUp_RADIUS = 12

PowerUp_SPAWN_RATE = 6
PowerUp_RADIUS = 12

#class crate for game

class PowerUp:
    def __init__(self, x, y, power_type):
        self.x = x
        self.y = y
        self.radius = PowerUp_RADIUS
        self.speed = 1.3

        self.shield_sprite = arcade.Sprite(
            r"C://Users\Admin//vs code//newtable//assets\sheild.png",
            scale=0.75
        )

        self.bomb_sprite = arcade.Sprite(
            r"C://Users\Admin//vs code//newtable//assets\bomb.png",
            scale=0.75
        )

        self.health_sprite = arcade.Sprite(
            r"C://Users//Admin//vs code//newtable//assets//health.png",
            scale=0.75
        )


        if power_type == "shield":
            self.sprite = self.shield_sprite
        elif power_type == "bomb":
            self.sprite = self.bomb_sprite
        else:
            self.sprite = self.health_sprite

        self.power_type = power_type

        
        if power_type == "shield":
            self.color = arcade.color.LIGHT_GOLDENROD_YELLOW
        elif power_type == "bomb":
            self.color = arcade.color.IMPERIAL_RED
        else:
            self.color = arcade.color.UNBLEACHED_SILK

    def draw(self):
        self.sprite.center_x = self.x
        self.sprite.center_y = self.y

        arcade.draw_sprite(self.sprite)

    def update(self):
        self.y -= self.speed

    def is_off_screen(self):
        return (
        self.x < -50 or
        self.x > SCREEN_WIDTH + 50 or
        self.y < -50 or
        self.y > SCREEN_HEIGHT + 50
    )

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.radius = random.uniform(2, 6)

        self.color = random.choice([
            arcade.color.RED,
            arcade.color.ORANGE,
            arcade.color.YELLOW
        ])

        self.speed_x = random.uniform(-PARTICLE_SPEED, PARTICLE_SPEED)
        self.speed_y = random.uniform(-PARTICLE_SPEED, PARTICLE_SPEED)

        self.alpha = 255

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y

        self.alpha -= PARTICLE_FADE_RATE

        return self.alpha > 0

    def draw(self):
        arcade.draw_circle_filled(
            self.x,
            self.y,
            self.radius,
            (*self.color[:3], max(0, self.alpha))
        )


class EnemyBullet:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle

        self.sprite = arcade.Sprite(
            r"C://Users\Admin//vs code//newtable//assets//enemy_bullet.png",
            scale=0.55
        )
        
        self.radius = 6
        self.speed = ENEMY_BULLET_SPEED
        self.color = ENEMY_BULLET_COLOR
        self.damage = 10

    def update(self):
        self.x += math.cos(math.radians(self.angle)) * self.speed
        self.y += math.sin(math.radians(self.angle)) * self.speed

    def draw(self):
        self.sprite.center_x = self.x
        self.sprite.center_y = self.y
        arcade.draw_sprite(self.sprite)

    def is_off_screen(self):
        return (
            self.x < 0 or self.x > SCREEN_WIDTH or
            self.y < 0 or self.y > SCREEN_HEIGHT
        )


class Enemy:
    def __init__(self):
        side = random.choice(["top", "right", "bottom", "left"])

        if side == "top":
            self.x = random.uniform(0, SCREEN_WIDTH)
            self.y = SCREEN_HEIGHT + 20

        elif side == "right":
            self.x = SCREEN_WIDTH + 20
            self.y = random.uniform(0, SCREEN_HEIGHT)

        elif side == "bottom":
            self.x = random.uniform(0, SCREEN_WIDTH)
            self.y = -20

        else:
            self.x = -20
            self.y = random.uniform(0, SCREEN_HEIGHT)

        self.enemy_type = random.choice(ENEMY_TYPES)

        if self.enemy_type == "shooter":
            image = r"C://Users//Admin//vs code//newtable//assets//shooter_enemy.png"
        else:
            image = r"C:/Users//Admin//vs code//newtable//assets//non_shooter_enemy.png"

        self.sprite = arcade.Sprite(image, scale=0.6)

        self.speed = random.uniform(ENEMY_SPEED_MIN, ENEMY_SPEED_MAX)
        if self.enemy_type == "shooter":
            self.sprite.angle = self.angle =+ 360 + 90
        else:
            self.sprite.angle = self.angle =+ 360 + 90

        self.radius = 150 * ENEMY_SCALE

        self.max_health = 3
        self.health = 3

        self.shoot_cooldown = ENEMY_SHOOT_COOLDOWN
 
    def update(self, player_x, player_y, delta_time):
        dx = player_x - self.x
        dy = player_y - self.y

        self.angle = math.degrees(math.atan2(dy, dx))

        self.x += math.cos(math.radians(self.angle)) * self.speed
        self.y += math.sin(math.radians(self.angle)) * self.speed

        if self.enemy_type == "shooter":
            self.shoot_cooldown -= delta_time

    def shoot(self):
        if self.enemy_type == "shooter" and self.shoot_cooldown <= 0:

            bullet_x = self.x + math.cos(math.radians(self.angle)) * self.radius
            bullet_y = self.y + math.sin(math.radians(self.angle)) * self.radius

            self.shoot_cooldown = ENEMY_SHOOT_COOLDOWN

            return EnemyBullet(
                bullet_x,
                bullet_y,
                self.angle
            )

        return None

    def draw(self):

        self.sprite.center_x = self.x
        self.sprite.center_y = self.y

        self.sprite.angle = self.angle - 90

        arcade.draw_sprite(self.sprite)

        self.draw_health_bar()

        self.draw_health_bar()

    def draw_health_bar(self):
        bar_width = 40
        bar_height = 6

        health_ratio = self.health / self.max_health
        current_width = bar_width * health_ratio

        x = self.x
        y = self.y + self.radius + 15

        arcade.draw_line(
            x - bar_width / 2,
            y,
            x + bar_width / 2,
            y,
            arcade.color.RED,
            bar_height
        )

        arcade.draw_line(
            x - bar_width / 2,
            y,
            x - bar_width / 2 + current_width,
            y,
            arcade.color.GREEN,
            bar_height
        )

    def is_off_screen(self):
        return (
            self.x < -50 or self.x > SCREEN_WIDTH + 50 or
            self.y < -50 or self.y > SCREEN_HEIGHT + 50
        )


class BossBullet:
    def __init__(self, x, y, angle, is_big=False):
        self.x = x
        self.y = y

        if is_big:

            self.radius = 12

            self.sprite = arcade.Sprite(
                r"C://Users\Admin//vs code//newtable//assets//big_boss_bullet.png",
                scale=0.83
            )

        else:

            self.radius = 6

            self.sprite = arcade.Sprite(
                r"C://Users\Admin//vs code//newtable//assets//small_boss_bullet.png",
                scale=0.47
            )

        self.angle = angle

        self.speed = 6
        self.damage = 100 if is_big else 30

        if is_big:
            self.radius = 12
            self.color = arcade.color.FALU_RED
        else:
            self.radius = 6
            self.color = arcade.color.ONYX

    def update(self):
        self.x += math.cos(math.radians(self.angle)) * self.speed
        self.y += math.sin(math.radians(self.angle)) * self.speed

    def draw(self):
        self.sprite.center_x = self.x
        self.sprite.center_y = self.y
        self.sprite.angle = self.angle

        arcade.draw_sprite(self.sprite)

    def is_off_screen(self):
        return (
            self.x < -50 or self.x > SCREEN_WIDTH + 50 or
            self.y < -50 or self.y > SCREEN_HEIGHT + 50
        )


class Boss:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2 + random.uniform(-200, 200)
        self.y = 600

        self.sprite = arcade.Sprite(
            r"C://Users\Admin//vs code//newtable//assets\boss.png",
            scale=0.8
        )

        self.radius = 50

        self.health = 100
        self.max_health = 100

        self.speed = 1
        self.angle = -90

        self.normal_shoot_cooldown = 0
        self.big_shoot_cooldown = 0

        self.damage_flash_timer = 0
        self.flashing = False

        self.color = arcade.color.ORANGE

    def take_damage(self):
        self.health -= 1

        self.damage_flash_timer = 0.2
        self.flashing = True

        return self.health <= 0

    def update(self, player_x, player_y, delta_time):

        dx = player_x - self.x
        dy = player_y - self.y

        self.angle = math.degrees(math.atan2(dy, dx))

        self.x += math.cos(math.radians(self.angle)) * self.speed
        self.y += math.sin(math.radians(self.angle)) * self.speed

        self.normal_shoot_cooldown -= delta_time
        self.big_shoot_cooldown -= delta_time

        if self.flashing:
            self.damage_flash_timer -= delta_time

            if self.damage_flash_timer <= 0:
                self.flashing = False

    def shoot_normal(self):
        if self.normal_shoot_cooldown <= 0:

            bullet_x = self.x + math.cos(math.radians(self.angle)) * self.radius
            bullet_y = self.y + math.sin(math.radians(self.angle)) * self.radius

            self.normal_shoot_cooldown = 3

            return BossBullet(
                bullet_x,
                bullet_y,
                self.angle,
                False
            )

        return None

    def shoot_big(self):
        if self.big_shoot_cooldown <= 0:

            bullet_x = self.x + math.cos(math.radians(self.angle)) * self.radius
            bullet_y = self.y + math.sin(math.radians(self.angle)) * self.radius

            self.big_shoot_cooldown = 8

            return BossBullet(
                bullet_x,
                bullet_y,
                self.angle,
                True
            )

        return None

    def draw(self):

        self.sprite.center_x = self.x
        self.sprite.center_y = self.y

        self.sprite.angle = self.angle - 90

        arcade.draw_sprite(self.sprite)

        self.draw_health_bar()

    def draw_health_bar(self):

        bar_width = 200
        bar_height = 15

        health_percentage = self.health / self.max_health
        health_width = health_percentage * bar_width

        bar_x = self.x
        bar_y = self.y + self.radius + 40

        arcade.draw_lbwh_rectangle_filled(
            bar_x - bar_width / 2,
            bar_y - bar_height / 2,
            bar_width,
            bar_height,
            arcade.color.RED
        )

        if health_percentage > 0.7:
            health_color = arcade.color.GREEN
        elif health_percentage > 0.4:
            health_color = arcade.color.YELLOW
        else:
            health_color = arcade.color.RED

        arcade.draw_lbwh_rectangle_filled(
            bar_x - bar_width / 2,
            bar_y - bar_height / 2,
            health_width,
            bar_height,
            health_color
        )

        arcade.draw_lbwh_rectangle_outline(
            bar_x - bar_width / 2,
            bar_y - bar_height / 2,
            bar_width,
            bar_height,
            arcade.color.WHITE,
            2
        )

        arcade.draw_text(
            f"BOSS HP: {self.health}",
            bar_x - 60,
            bar_y + 20,
            arcade.color.WHITE,
            14
        )


class Bullet:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle

        self.sprite = arcade.Sprite(
            r"C://Users\Admin//vs code//newtable//assets//player_bullet.png",
            scale=0.40
        )

        self.speed = BULLET_SPEED
        self.radius = 5 * BULLET_SCALE

    def update(self):
        a = math.radians(self.angle)

        self.x += math.cos(a) * self.speed
        self.y += math.sin(a) * self.speed

    def draw(self):

        self.sprite.center_x = self.x
        self.sprite.center_y = self.y

        self.sprite.angle = self.angle

        arcade.draw_sprite(self.sprite)

    def is_off_screen(self):
        return (
            self.x < 0 or self.x > SCREEN_WIDTH or
            self.y < 0 or self.y > SCREEN_HEIGHT
        )


class GameWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        arcade.set_background_color((10, 10, 10))
        
        self.player_x = SCREEN_WIDTH // 2
        self.player_y = SCREEN_HEIGHT // 2
        self.player_angle = 0
        self.player_radius = 40
        self.player_sprite = arcade.Sprite(
                r"C://Users//Admin//vs code//newtable//assets//main_player.png",
                scale=0.35
                    )
             
        self.player_sprite.center_x = self.player_x
        self.player_sprite.center_y = self.player_y

        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player_sprite)

        self.bullets = []
        self.enemy_bullets = []
        self.enemies = []
        self.particles = []
        self.PowerUps = []

        self.boss = None
        self.boss_spawn_score = 10

        self.keys_pressed = set()

        self.shoot_cooldown = 0
        self.enemy_spawn_timer = ENEMY_SPAWN_RATE
        self.shield_timer = SHIELD_TIMER
        self.bomb_timer = BOMB_TIMER
        self.health_timer = HEALTH_TIMER
        self.PowerUp_spawn_timer = PowerUp_SPAWN_RATE
        self.current_spawn_rate = ENEMY_SPAWN_RATE
        self.enemy_bullet_damage = 10
        EnemyBullet.damage = self.enemy_bullet_damage

        self.score = 0
        self.health = 100
        self.game_over = False

        self.total_time = 0
        self.shield_active = False
        self.shield_timer = 0
        self.popup_text = ""
        self.popup_timer = 0
        self.enemy_damage = 10
        self.small_boss_bullet_damage = 30
        self.phealth = 50

        self.background = arcade.load_texture(
            r"C://Users//Admin//vs code//newtable//assets//game_background.jpg"
        )
                
    def on_draw(self):
        self.clear()

        arcade.draw_texture_rect(
            self.background,
            arcade.LBWH(
            0,
            0,
            SCREEN_WIDTH,
            SCREEN_HEIGHT
            )   
        )

        for particle in self.particles:
            particle.draw()

        for enemy in self.enemies:
            enemy.draw()

        if self.boss:
            self.boss.draw()

        for bullet in self.bullets:
            bullet.draw()

        for enemy_bullet in self.enemy_bullets:
            enemy_bullet.draw()

        for powerup in self.PowerUps:
            powerup.draw()

        self.player_sprite.center_x = self.player_x
        self.player_sprite.center_y = self.player_y

        self.player_sprite.angle = -self.player_angle + 360 + 90

        self.player_list.draw()

        if self.shield_active:

            angle = self.total_time * 200  # rotation speed

            arcade.draw_arc_outline(
                self.player_x,
                self.player_y,
                self.player_radius + 40,
                self.player_radius + 40,
                arcade.color.CYAN,
                angle,
                angle + 120,
                5
                )

            arcade.draw_arc_outline(
        self.player_x,
        self.player_y,
        self.player_radius + 40,
        self.player_radius + 40,
        arcade.color.AQUA,
        angle + 180,
        angle + 300,
        5
    )

        arcade.draw_text(
            f"Score: {self.score}",
            20,
            SCREEN_HEIGHT - 40,
            arcade.color.WHITE,
            20
        )

        arcade.draw_text(
            f"Health: {self.health}",
            20,
            SCREEN_HEIGHT - 70,
            arcade.color.WHITE,
            20
        )

        if self.game_over:

            arcade.draw_text(
        "GAME OVER...",
        SCREEN_WIDTH // 2 - 120,
        SCREEN_HEIGHT // 2,
        arcade.color.RED,
        50
    )

            arcade.draw_text(
        "Press R To Restart",
        SCREEN_WIDTH // 2 - 110,
        SCREEN_HEIGHT // 2 - 60,
        arcade.color.WHITE,
        24
    )
            
        if self.popup_timer > 0:

            arcade.draw_text(
        self.popup_text,
        SCREEN_WIDTH - 320,
        SCREEN_HEIGHT - 40,
        arcade.color.YELLOW,
        18,
        bold=True
    )

        if self.shield_active:

            arcade.draw_text(
        f"SHIELD : {int(self.shield_timer)} SECS REMAINING!",
        SCREEN_WIDTH - 420,
        SCREEN_HEIGHT - 70,
        arcade.color.CYAN,
        16,
        bold=True
    )

    def on_update(self, delta_time):

        if self.game_over:
            return

        self.total_time += delta_time
        self.shoot_cooldown -= delta_time
        self.enemy_spawn_timer -= delta_time

        if self.shield_active:
            self.shield_timer -= delta_time

        if self.shield_timer <= 0:
            self.shield_active = False
        
        for particle in self.particles[:]:
            if not particle.update():
                self.particles.remove(particle)

        if self.enemy_spawn_timer <= 0:
            self.enemies.append(Enemy())
            self.enemy_spawn_timer = ENEMY_SPAWN_RATE

        if self.score % 50  == 0 and self.boss is None and self.score != 0 :
            self.boss = Boss()

        a = math.radians(self.player_angle)

        if arcade.key.W in self.keys_pressed  :
            self.player_x += math.cos(a) * PLAYER_SPEED
            self.player_y += math.sin(a) * PLAYER_SPEED

        if arcade.key.S in self.keys_pressed:
            self.player_x -= math.cos(a) * PLAYER_SPEED
            self.player_y -= math.sin(a) * PLAYER_SPEED

        if arcade.key.A in self.keys_pressed:
            self.player_angle += PLAYER_TURN_SPEED

        if arcade.key.D in self.keys_pressed:
            self.player_angle -= PLAYER_TURN_SPEED

        if arcade.key.SPACE in self.keys_pressed:
            self.shoot()

        for bullet in self.bullets[:]:
            bullet.update()

            if bullet.is_off_screen():
                self.bullets.remove(bullet)

        for enemy_bullet in self.enemy_bullets[:]:
            enemy_bullet.update()

            if enemy_bullet.is_off_screen():
                self.enemy_bullets.remove(enemy_bullet)

            distance = math.sqrt(
                (enemy_bullet.x - self.player_x) ** 2 +
                (enemy_bullet.y - self.player_y) ** 2
            )

            if distance < enemy_bullet.radius + self.player_radius:

                if not self.shield_active:
                    self.health -= enemy_bullet.damage

                if enemy_bullet in self.enemy_bullets:
                    self.enemy_bullets.remove(enemy_bullet)

                if self.health <= 0:
                    self.game_over = True

        for enemy in self.enemies[:]:

            enemy.update(
                self.player_x,
                self.player_y,
                delta_time
            )

            enemy_bullet = enemy.shoot()

            if enemy_bullet is not None:
                self.enemy_bullets.append(enemy_bullet)

            if enemy_bullet:
                self.enemy_bullets.append(enemy_bullet)

            player_distance = math.sqrt(
                (self.player_x - enemy.x) ** 2 +
                (self.player_y - enemy.y) ** 2
                )

            if player_distance < self.player_radius + enemy.radius:

                if not self.shield_active:
                    self.health -= self.enemy_damage

                self.enemies.remove(enemy)

                if self.health <= 0:
                    self.game_over = True

                if self.health <= 0:
                    self.game_over = True

        if self.boss:

            self.boss.update(
                self.player_x,
                self.player_y,
                delta_time
            )

            normal_bullet = self.boss.shoot_normal()

            if normal_bullet:
                self.enemy_bullets.append(normal_bullet)

            big_bullet = self.boss.shoot_big()

            if big_bullet:
                self.enemy_bullets.append(big_bullet)

        for bullet in self.bullets[:]:

            for enemy in self.enemies[:]:

                distance = math.sqrt(
                    (bullet.x - enemy.x) ** 2 +
                    (bullet.y - enemy.y) ** 2
                )

                if distance < bullet.radius + enemy.radius:

                    enemy.health -= 1

                    if bullet in self.bullets:
                        self.bullets.remove(bullet)

                    for _ in range(random.choice(PARTICLE_COUNT)):
                            self.particles.append(
                                Particle(enemy.x, enemy.y)
                            )

                    if enemy.health <= 0:

                        for _ in range(random.choice(PARTICLE_COUNT)):
                            self.particles.append(
                                Particle(enemy.x, enemy.y)
                            )

                        if enemy in self.enemies:
                            self.enemies.remove(enemy)

                        self.score += 10

                    break

        if self.boss:

            for bullet in self.bullets[:]:

                distance = math.sqrt(
                    (bullet.x - self.boss.x) ** 2 +
                    (bullet.y - self.boss.y) ** 2
                )

                if distance < bullet.radius + self.boss.radius:

                    dead = self.boss.take_damage()

                    if bullet in self.bullets:
                        self.bullets.remove(bullet)

                    for _ in range(random.choice(PARTICLE_COUNT)):
                        self.particles.append(
                            Particle(bullet.x, bullet.y)
                        )

                    if dead:
                        self.score += 200
                        self.boss = None

                    break

        self.player_x = max(self.player_radius, min(SCREEN_WIDTH - self.player_radius, self.player_x))
        self.player_y = max(self.player_radius, min(SCREEN_HEIGHT - self.player_radius, self.player_y))

                # ---------------- PowerUp SPAWNING ---------------- #

        if self.popup_timer > 0:
            self.popup_timer -= delta_time
        self.PowerUp_spawn_timer -= delta_time

        if self.PowerUp_spawn_timer <= 0:

            power_type = random.choice(
                ["shield", "health", "bomb"]
            )

            spawn_x = random.randint(50, SCREEN_WIDTH - 50)

            self.PowerUps.append(
                PowerUp(
                    spawn_x,
                    SCREEN_HEIGHT,
                    power_type
                )
            )

            self.PowerUp_spawn_timer = PowerUp_SPAWN_RATE

        # ---------------- PowerUp UPDATE ---------------- #

        for powerup in self.PowerUps[:]:

            powerup.update()

            if powerup.is_off_screen():
                self.PowerUps.remove(powerup)
                continue

            distance = math.sqrt(
                (powerup.x - self.player_x) ** 2 +
                (powerup.y - self.player_y) ** 2
            )

            if distance < PowerUp_RADIUS + self.player_radius:

                if powerup.power_type == "health":

                    self.health += self.phealth

                    if self.health > 100:
                        self.health = 100

                    self.popup_text = "+50 HEALTH!"
                    self.popup_timer = 2
        

                elif powerup.power_type == "shield":

                    self.shield_active = True
                    self.shield_timer = random.randint(8,12)

                # BOMB PowerUp
                elif powerup.power_type == "bomb":

                    for enemy in self.enemies[:]:

                        for _ in range(random.choice(PARTICLE_COUNT)):
                            self.particles.append(
                                Particle(enemy.x, enemy.y)
                            )
                        
                        self.enemies.remove(enemy)
                        self.score += 10
                    self.popup_text = "BOMB USED!"
                    self.popup_timer = 2

                self.PowerUps.remove(powerup)                 

        if self.score % 70 == 0 and self.score != 0:
            self.shield_timer = random.randint(7,11)
            self.PowerUp_spawn_timer /= 1.2
            self.current_spawn_rate /= 1.2
            self.enemy_damage *= 1.2 
            EnemyBullet.damage *= 1.2
            self.phealth -= 3
            if self.phealth == 20:
                self.phealth = 20             
        
    def shoot(self):

        if self.shoot_cooldown <= 0:

            a = math.radians(self.player_angle)

            bullet_x = self.player_x + math.cos(a) * self.player_radius
            bullet_y = self.player_y + math.sin(a) * self.player_radius

            self.bullets.append(
                Bullet(
                    bullet_x,
                    bullet_y,
                    self.player_angle
                )
            )

            self.shoot_cooldown = PLAYER_SHOOT_COOLDOWN

    def on_key_press(self, key, modifiers):

        self.keys_pressed.add(key)

        if key == arcade.key.R and self.game_over:
            self.reset_game()

    def on_key_release(self, key, modifiers):
        self.keys_pressed.discard(key)

    def on_mouse_motion(self, x, y, dx, dy):

        dx = x - self.player_x
        dy = y - self.player_y

        self.player_angle = math.degrees(math.atan2(dy, dx))

    def on_mouse_press(self, x, y, button, modifiers):

        if button == arcade.MOUSE_BUTTON_LEFT:
            self.shoot()

        a = math.radians(self.player_angle)

        if button == arcade.MOUSE_BUTTON_MIDDLE:
            self.player_x += math.cos(a) * PLAYER_SPEED
            self.player_y += math.sin(a) * PLAYER_SPEED
            

    def reset_game(self):

        self.player_x = SCREEN_WIDTH // 2
        self.player_y = SCREEN_HEIGHT // 2
        self.player_angle = 0

        self.bullets.clear()
        self.enemy_bullets.clear()
        self.enemies.clear()
        self.particles.clear()

        self.boss = None

        self.score = 0
        self.health = 100

        self.game_over = False

        self.enemy_spawn_timer = ENEMY_SPAWN_RATE
        self.shoot_cooldown = 0

        self.PowerUps.clear()
        self.PowerUp_spawn_timer = PowerUp_SPAWN_RATE


def main():
    window = GameWindow()
    window.center_window()
    arcade.run()


if __name__ == "__main__":
    main() 