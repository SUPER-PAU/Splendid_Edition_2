from constants.textures.emoji import pau, lisa
from lib.display import display
import pygame
import random
from constants.textures.sprites import all_sprites, bullet_sprites, explosion, bullet, beam, rocket, energy, stone
from constants.audio.effects import explosion_sounds, gaubica_sounds, shield_sfx

screen_rect = (0, 0, display.screen_width, display.screen_height)


class Particle(pygame.sprite.Sprite):
    # сгенерируем частицы разного размера

    def __init__(self, pos, dx, dy, flip, particle):
        super().__init__(all_sprites)
        fire = [particle]
        for scale in (20 * display.scr_w, 24 * display.scr_w, 28 * display.scr_w):
            fire.append(pygame.transform.scale(fire[0], (scale, scale)))
        self.image = random.choice(fire)
        self.rect = self.image.get_rect()
        # у каждой частицы своя скорость — это вектор
        if flip:
            dx = dx + 11
        else:
            dx = -dx - 11
        self.velocity = [dx, dy]
        # и свои координаты
        self.rect.x, self.rect.y = pos
        # гравитация будет одинаковой (значение константы)
        self.gravity = 1.4

    def update(self):
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0] * display.scr_w
        self.rect.y += self.velocity[1] * display.scr_h
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect(screen_rect):
            self.kill()


def create_particles(position, flip, particle):
    # количество создаваемых частиц
    particle_count = 13
    # возможные скорости
    numbers = range(-15, 16)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers), flip, particle)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, rect, sprite_sheet, data, target, damage):
        super().__init__(bullet_sprites)
        self.rect = rect.copy()
        self.size, self.image_scale, self.offset, self.animation_steps = data[0], data[1], data[2], data[3]
        self.animation_list = self.load_images(sprite_sheet, self.animation_steps)
        self.action = 0  # 0 - idle
        self.frame_index = 0
        self.flip = data[4]
        self.hit = False
        self.target = target
        self.damage = damage
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.speed = 45

    def update_action(self, new_action):
        # check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # update anim sattings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def load_images(self, sprite_sheet, animation_steps):
        # extract images from sprite_sheets
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(
                    pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list

    def update(self):
        if not self.hit:
            self.update_action(0)
        else:
            self.update_action(1)
        animation_cooldown = 100
        # update image
        self.image = self.animation_list[self.action][self.frame_index]

        # check if enough time has passed sinse the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        if self.rect.left > display.screen_width or (
                self.action == 1 and self.frame_index >= len(self.animation_list[self.action])) or self.rect.right < 0:
            self.kill()
        self.move()
        self.draw()
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0
        # pygame.draw.rect(display.screen, (255, 0, 0), self.rect)

    def move(self):
        dx = 0
        if not self.hit:
            if self.flip:
                dx = -self.speed
            else:
                dx = self.speed
        self.rect.x += dx * display.scr_w
        if not self.speed <= 20:
            self.speed -= 0.5
        self.attack()

    def attack(self):
        if self.rect.colliderect(self.target.rect) and not self.hit:
            self.hit = True
            self.target.take_damage(self.damage)

    def draw(self):
        # pygame.draw.rect(display.screen, (255, 0, 0), self.rect)
        img = pygame.transform.flip(self.image, self.flip, False)
        display.screen.blit(img,
                            (self.rect.x - self.offset[0] * self.image_scale,
                             self.rect.y - self.offset[1] * self.image_scale))


class Dash(pygame.sprite.Sprite):
    def __init__(self, rect, flip, target, player, damage, sprite_group):
        super().__init__(sprite_group)
        self.rect = rect.copy()
        self.action = 0  # 0 - idle
        self.frame_index = 0
        self.flip = flip
        self.hit = False
        self.target = target
        self.damage = damage
        self.player = player
        self.update_time = pygame.time.get_ticks()

    def update(self):
        self.move(self.player)
        if not self.player.attacking:
            self.kill()

    def move(self, player):
        self.rect.x += player.dash_x * display.scr_w
        self.rect.y = self.rect.y
        if self.rect.colliderect(self.target.rect) and not self.hit:
            self.hit = True
            self.target.take_damage(self.damage)


class Explosion(pygame.sprite.Sprite):
    def __init__(self, rect, sprite_sheet, data, target, damage):
        super().__init__(bullet_sprites)
        self.rect = rect.copy()
        self.size, self.image_scale, self.offset, self.animation_steps = data[0], data[1], data[2], data[3]
        self.animation_list = self.load_images(sprite_sheet, self.animation_steps)
        self.action = 0  # 0 - idle
        self.frame_index = 0
        self.flip = data[4]
        self.hit = False
        self.target = target
        self.damage = damage
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.speed = 45
        # play sound

    def update_action(self, new_action):
        # check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # update anim sattings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def load_images(self, sprite_sheet, animation_steps):
        # extract images from sprite_sheets
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(
                    pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list

    def update(self):
        self.update_action(0)
        animation_cooldown = 100
        # update image
        self.image = self.animation_list[self.action][self.frame_index]

        # check if enough time has passed sinse the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        self.attack()
        self.draw()
        if self.frame_index >= len(self.animation_list[self.action]):
            self.kill()
        # pygame.draw.rect(display.screen, (255, 0, 0), self.rect)

    def attack(self):
        if self.rect.colliderect(self.target.rect) and not self.hit:
            self.hit = True
            self.target.take_damage(self.damage, True)

    def draw(self):
        # pygame.draw.rect(display.screen, (255, 0, 0), self.rect)
        img = pygame.transform.flip(self.image, self.flip, False)
        display.screen.blit(img,
                            (self.rect.x - self.offset[0] * self.image_scale,
                             self.rect.y - self.offset[1] * self.image_scale))


def create_explosion(rect, data, target, damage):
    Explosion(rect, explosion, data, target, damage)


class Rocket(Explosion):
    def __init__(self, rect, sprite_sheet, data, target, damage):
        super().__init__(rect, sprite_sheet, data, target, damage)
        self.rect = rect.copy()
        self.size, self.image_scale, self.offset, self.animation_steps = data[0], data[1], data[2], data[3]
        self.animation_list = self.load_images(sprite_sheet, self.animation_steps)
        self.action = 0  # 0 - idle
        self.frame_index = 0
        self.flip = data[4]
        self.hit = False
        self.target = target
        self.damage = damage
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.speed = 30 * display.scr_w
        self.vel_y = -50 * display.scr_h
        # play shoot sound
        pygame.mixer.Sound.play(random.choice(gaubica_sounds))

    def update(self):
        if self.vel_y < 0:
            self.update_action(0)
        else:
            self.update_action(1)
        animation_cooldown = 50
        # update image
        self.image = self.animation_list[self.action][self.frame_index]

        # check if enough time has passed sinse the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        self.move()
        self.draw()
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0
        # pygame.draw.rect(display.screen, (255, 0, 0), self.rect)

    def move(self):
        GRAVITY = 2 * display.scr_h
        dx = 0
        dy = 0
        if not self.hit:
            if self.flip:
                dx = -self.speed
            else:
                dx = self.speed
        if self.speed > 2 * display.scr_w:
            self.speed -= 0.5 * display.scr_w
        # apply gravity
        self.vel_y += GRAVITY
        dy += self.vel_y

        # ensure it stays on screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > display.screen_width:
            dx = display.screen_width - self.rect.right
        if self.rect.bottom + dy * display.scr_h > display.screen_height - 110 * display.scr_h:
            self.create_expl()
            self.kill()

        # update position
        self.rect.x += dx
        self.rect.y += dy

    def create_expl(self):
        # play prilet sound
        pygame.mixer.Sound.play(random.choice(explosion_sounds))
        explosion_rect = pygame.Rect(self.rect.centerx - (200 * display.scr_w),
                                     display.screen_height - 710 * display.scr_h,
                                     400 * display.scr_w, 600 * display.scr_h)
        offset = 34
        if self.flip:
            offset = 40
        explosion_data = [127, 7.7 * display.scr_w, (offset, 10), [5], self.flip]
        create_explosion(explosion_rect, explosion_data, self.target, self.damage)


class Stone(Explosion):
    def __init__(self, rect, sprite_sheet, data, target, damage):
        super().__init__(rect, sprite_sheet, data, target, damage)
        self.rect = rect.copy()
        self.speed = 25 * display.scr_w
        self.vel_y = -47 * display.scr_h

    def update(self):
        if not self.hit:
            self.update_action(0)
        else:
            self.update_action(1)
        animation_cooldown = 100
        # update image
        self.image = self.animation_list[self.action][self.frame_index]

        # check if enough time has passed sinse the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        if self.rect.left > display.screen_width or (
                self.action == 1 and self.frame_index >= len(self.animation_list[self.action])) or self.rect.right < 0:
            self.kill()
        self.move()
        self.draw()
        self.attack()
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def move(self):
        GRAVITY = 2 * display.scr_h
        dx = 0
        dy = 0
        if self.flip:
            dx = -self.speed
        else:
            dx = self.speed
        if self.speed > 2 * display.scr_w:
            self.speed -= 0.5 * display.scr_w
        # apply gravity
        self.vel_y += GRAVITY
        dy += self.vel_y

        # ensure it stays on screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > display.screen_width:
            dx = display.screen_width - self.rect.right
        if self.rect.bottom + dy * display.scr_h > display.screen_height - 110 * display.scr_h:
            self.hit = True
        if not self.hit:
            # update position
            self.rect.x += dx
            self.rect.y += dy


class ScyRocket(Rocket):
    def __init__(self, rect, sprite_sheet, data, target, damage):
        super().__init__(rect, sprite_sheet, data, target, damage)
        self.speed = 0


class Beam(Bullet):
    def attack(self):
        if self.rect.colliderect(self.target.rect) and not self.hit:
            self.hit = True
            self.target.take_damage(self.damage)
            self.target.stun()


class CreateBombing:
    def __init__(self):
        self.attack_cooldown = 150
        self.data = [200, 0.6 * display.scr_w, (10, 10), [2, 2], False]

    def enable(self, target):
        if self.attack_cooldown <= 0:
            a = random.randint(int(50 * display.scr_w), int(1800 * display.scr_w))
            bullet_rect = pygame.Rect(a, -400, 100 * display.scr_w, 100 * display.scr_h)
            ScyRocket(bullet_rect, rocket, self.data, target, 10)
            self.attack_cooldown = 300
        else:
            self.attack_cooldown -= 1


class Energy(Stone):
    def __init__(self, rect, sprite_sheet, data, target, damage):
        super().__init__(rect, sprite_sheet, data, target, damage)
        self.speed = 25
        self.vel_y = -30 * display.scr_h

    def create_expl(self):
        # play prilet sound
        pygame.mixer.Sound.play(random.choice(explosion_sounds))
        explosion_rect = pygame.Rect(self.rect.centerx - (200 * display.scr_w),
                                     display.screen_height - 710 * display.scr_h,
                                     400 * display.scr_w, 600 * display.scr_h)
        offset = 34
        if self.flip:
            offset = 40
        explosion_data = [127, 7.7 * display.scr_w, (offset, 10), [5], self.flip]
        create_explosion(explosion_rect, explosion_data, self.target, self.damage)

    def attack(self):
        if self.rect.colliderect(self.target.rect) and not self.hit:
            self.create_expl()
            self.hit = True


class DamageNumber(pygame.sprite.Sprite):
    def __init__(self, rect, flip, damage):
        super().__init__(bullet_sprites)
        self.damage, self.flip = f"-{str(damage)}", flip
        self.rect = rect.copy()
        self.vel_y = -0.1 * display.scr_h
        self.color = (255, 255, 255)
        self.font = pygame.font.SysFont('Times New Roman', int(60 * display.scr_w))
        if damage >= 20:
            self.font = pygame.font.SysFont('Times New Roman', int(75 * display.scr_w))
            self.color = (255, 255, 0)
        if damage >= 30:
            self.font = pygame.font.SysFont('Times New Roman', int(90 * display.scr_w))
            self.color = (255, 0, 0)

    def update(self):
        if self.rect.top > 330 * display.scr_h:
            self.kill()
        self.move()
        self.draw()

    def draw(self):
        black_img = self.font.render(self.damage, True, (0, 0, 0))
        display.screen.blit(black_img, (self.rect.x + 2 * display.scr_w, self.rect.y + 2 * display.scr_h))
        img = self.font.render(self.damage, True, self.color)
        display.screen.blit(img, (self.rect.x, self.rect.y))

    def move(self):
        GRAVITY = 0.05 * display.scr_h
        dy = 0
        # apply gravity
        self.vel_y += GRAVITY
        dy += self.vel_y
        # update position
        self.rect.y += dy


def create_damage_number(coords, flip, damage):
    rect = pygame.Rect(coords[0], coords[1],
                       int(90 * display.scr_w * (damage // 10)), int(90 * display.scr_w * (damage // 10)))
    DamageNumber(rect, flip, damage)


def create_stone(rect, data, target, damage):
    Stone(rect, stone, data, target, damage)


def create_rocket(rect, data, target, damage):
    Rocket(rect, rocket, data, target, damage)


def create_energy(rect, data, target, damage):
    Energy(rect, energy, data, target, damage)


def create_bullet(rect, data, target, damage):
    Bullet(rect, bullet, data, target, damage)


def create_dash(rect, flip, target, player, damage):
    Dash(rect, flip, target, player, damage, bullet_sprites)


def create_beam(rect, data, target, damage):
    Beam(rect, beam, data, target, damage)


create_bombing = CreateBombing()
