from lib.display import display
import pygame
import random
from constants.textures.sprites import all_sprites, bullet_sprites, damage_num_group, \
    explosion, bullet, beam, rocket, energy, stone, knifes
from constants.audio.effects import explosion_sounds, gaubica_sounds

screen_rect = (0, 0, display.screen_width, display.screen_height)


def load_images(sprite_sheet, animation_steps, size, scale):
    # extract images from sprite_sheets
    animation_list = []
    for y, animation in enumerate(animation_steps):
        temp_img_list = []
        for x in range(animation):
            temp_img = sprite_sheet.subsurface(x * size, y * size, size, size)
            temp_img_list.append(
                pygame.transform.scale(temp_img, (size * scale, size * scale)))
        animation_list.append(temp_img_list)
    return animation_list


rock_animation = load_images(stone, [2, 2], 200, 0.6)
knife_animation = load_images(knifes, [2, 2], 200, 0.6)
bullet_animation = load_images(bullet, [2, 2], 20, 4.55)
beam_animation = load_images(beam, [2, 2], 20, 4.55)
explosion_animation = load_images(explosion, [5], 127, 7.7)
sprite_by_name = {
    "explosion": explosion_animation,
    "bullet": bullet_animation,
    "rocket": rocket,
    "stone": rock_animation,
    "enegry": energy,
    "beam": beam_animation,
    "knife": knife_animation
}


class Particle(pygame.sprite.Sprite):
    # сгенерируем частицы разного размера

    def __init__(self, pos, dx, dy, flip, particle):
        super().__init__(all_sprites)
        fire = [particle]
        for scale in (18, 22, 25):
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
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
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
    def __init__(self, rect, data, target, damage):
        super().__init__(bullet_sprites)
        self.rect = rect.copy()
        self.size, self.image_scale, self.offset, self.animation_steps = data[0], data[1], data[2], data[3]
        self.action = 0  # 0 - idle
        self.frame_index = 0
        self.flip = data[4]
        self.hit = False
        self.sec_hit = False
        self.target = target
        self.damage = damage
        self.name = "bullet"
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

    def update(self, enemy, n=1):
        self.target = enemy
        if not self.hit:
            self.update_action(0)
        else:
            self.update_action(1)
        if not self.sec_hit:
            self.move()
        self.draw()
        if not self.hit:
            self.attack(n)
        animation_cooldown = 100
        # update image
        # check if enough time has passed sinse the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        if self.rect.left > display.screen_width or (
                self.action == 1 and self.frame_index >= 2) or self.rect.right < 0:
            self.kill()

        if self.frame_index >= 2:
            self.frame_index = 0
        # pygame.draw.rect(display.screen, (255, 0, 0), self.rect)

    def move(self):
        dx = 0
        if not self.hit:
            if self.flip:
                dx = -self.speed
            else:
                dx = self.speed
        self.rect.x += dx
        if not self.speed <= 20:
            self.speed -= 0.5

    def attack(self, n):
        if self.sec_hit and (self.target.hit or self.target.blocking):
            self.hit = True
        else:
            if n == 1 and self.sec_hit:
                pass
            else:
                if self.rect.colliderect(self.target.rect) and (not self.sec_hit or n == 2):
                    self.sec_hit = True
                    self.target.take_damage(self.damage, True, n)

    def draw(self):
        image = sprite_by_name[self.name][self.action][self.frame_index]
        # pygame.draw.rect(display.screen, (255, 0, 0), self.rect)
        img = pygame.transform.flip(image, self.flip, False)
        display.screen.blit(img,
                            (self.rect.x - self.offset[0] * self.image_scale,
                             self.rect.y - self.offset[1] * self.image_scale))


class Knife(Bullet):
    def __init__(self, rect, data, target, damage):
        super().__init__(rect, data, target, damage)
        self.name = "knife"


class Explosion(pygame.sprite.Sprite):
    def __init__(self, rect, data, target, damage):
        super().__init__(bullet_sprites)
        self.rect = rect.copy()
        self.size, self.image_scale, self.offset, self.animation_steps = data[0], data[1], data[2], data[3]
        self.name = "explosion"
        self.action = 0  # 0 - idle
        self.frame_index = 0
        self.flip = data[4]
        self.hit = False
        self.sec_hit = False
        self.target = target
        self.damage = damage
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

    def update(self, enemy, n):
        self.target = enemy
        self.update_action(0)
        animation_cooldown = 100
        # update image

        # check if enough time has passed sinse the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        if not self.hit:
            self.attack(n)
        if self.frame_index >= len(sprite_by_name[self.name][self.action]):
            self.frame_index = 0
            self.kill()
        self.draw()
        # pygame.draw.rect(display.screen, (255, 0, 0), self.rect)

    def attack(self, n):
        if self.sec_hit and (self.target.hit or self.target.blocking):
            self.hit = True
        else:
            if n == 1 and self.sec_hit:
                pass
            else:
                if self.rect.colliderect(self.target.rect) and (not self.sec_hit or n == 2):
                    self.sec_hit = True
                    self.target.take_damage(self.damage, True, n)

    def draw(self):
        image = sprite_by_name[self.name][self.action][self.frame_index]
        # pygame.draw.rect(display.screen, (255, 0, 0), self.rect)
        img = pygame.transform.flip(image, self.flip, False)
        display.screen.blit(img,
                            (self.rect.x - self.offset[0] * self.image_scale,
                             self.rect.y - self.offset[1] * self.image_scale))


def create_explosion(rect, data, target, damage):
    Explosion(rect, data, target, damage)


class Rocket(Explosion):
    def __init__(self, rect, data, target, damage):
        super().__init__(rect, data, target, damage)
        self.rect = rect.copy()
        self.size, self.image_scale, self.offset, self.animation_steps = data[0], data[1], data[2], data[3]
        self.action = 0  # 0 - idle
        self.frame_index = 0
        self.flip = data[4]
        self.hit = False
        self.target = target
        self.damage = damage
        self.update_time = pygame.time.get_ticks()
        self.speed = 30
        self.vel_y = -50
        self.name = "rocket"
        # play shoot sound
        pygame.mixer.Sound.play(random.choice(gaubica_sounds))

    def update(self, enemy, n):
        self.target = enemy
        if self.vel_y < 0:
            self.update_action(0)
        else:
            self.update_action(1)
        animation_cooldown = 50
        self.move()
        self.draw()
        # update image
        # check if enough time has passed sinse the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()

        if self.frame_index >= 2:
            self.frame_index = 0
        # pygame.draw.rect(display.screen, (255, 0, 0), self.rect)

    def move(self):
        GRAVITY = 2
        dx = 0
        dy = 0
        if not self.hit:
            if self.flip:
                dx = -self.speed
            else:
                dx = self.speed
        if self.speed > 2:
            self.speed -= 0.5
        # apply gravity
        self.vel_y += GRAVITY
        dy += self.vel_y

        # ensure it stays on screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > display.screen_width:
            dx = display.screen_width - self.rect.right
        if self.rect.bottom + dy > display.screen_height - 110:
            self.create_expl()
            self.kill()

        # update position
        self.rect.x += dx
        self.rect.y += dy

    def create_expl(self):
        # play prilet sound
        pygame.mixer.Sound.play(random.choice(explosion_sounds))
        explosion_rect = pygame.Rect(self.rect.centerx - 200, display.screen_height - 710, 400, 600)
        offset = 34
        if self.flip:
            offset = 40
        explosion_data = [127, 7.7, (offset, 10), [5], self.flip]
        create_explosion(explosion_rect, explosion_data, self.target, self.damage)


class Stone(Explosion):
    def __init__(self, rect, data, target, damage):
        super().__init__(rect, data, target, damage)
        self.rect = rect.copy()
        self.name = "stone"
        self.speed = 25
        self.vel_y = -47

    def update(self, enemy, n):
        self.target = enemy
        if not self.hit:
            self.update_action(0)
        else:
            self.update_action(1)
        animation_cooldown = 100
        # update image
        if not self.sec_hit:
            self.move()
        self.draw()
        if not self.hit:
            self.attack(n)
        # check if enough time has passed sinse the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        if self.rect.left > display.screen_width or (
                self.action == 1 and self.frame_index >= 2) or self.rect.right < 0:
            self.kill()

        if self.frame_index >= 2:
            self.frame_index = 0

    def move(self):
        GRAVITY = 2
        dy = 0
        if self.flip:
            dx = -self.speed
        else:
            dx = self.speed
        if self.speed > 2:
            self.speed -= 0.5
        # apply gravity
        self.vel_y += GRAVITY
        dy += self.vel_y

        # ensure it stays on screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > display.screen_width:
            dx = display.screen_width - self.rect.right
        if self.rect.bottom + dy > display.screen_height - 110:
            self.hit = True
        if not self.hit:
            # update position
            self.rect.x += dx
            self.rect.y += dy


class ScyRocket(Rocket):
    def __init__(self, rect, data, target, damage):
        super().__init__(rect, data, target, damage)
        self.speed = 0


class Beam(Bullet):
    def attack(self, n):
        if self.sec_hit and (self.target.hit or self.target.blocking):
            self.hit = True
        else:
            if n == 1 and self.sec_hit:
                pass
            else:
                if self.rect.colliderect(self.target.rect) and (not self.sec_hit or n == 2):
                    self.sec_hit = True
                    self.target.take_damage(self.damage, True, n)
                    self.target.stun()


class CreateBombing:
    def __init__(self):
        self.attack_cooldown = 150
        self.data = [200, 0.6, (10, 10), [2, 2], False]

    def enable(self, target):
        if self.attack_cooldown <= 0:
            a = random.randint(50, 1800)
            bullet_rect = pygame.Rect(a, -400, 100, 100)
            ScyRocket(bullet_rect, self.data, target, 10)
            self.attack_cooldown = 300
        else:
            self.attack_cooldown -= 1


class Energy(Stone):
    def __init__(self, rect, data, target, damage):
        super().__init__(rect, data, target, damage)
        self.speed = 25
        self.name = "energy"
        self.vel_y = -30

    def create_expl(self):
        # play prilet sound
        pygame.mixer.Sound.play(random.choice(explosion_sounds))
        explosion_rect = pygame.Rect(self.rect.centerx - 200, display.screen_height - 710, 400, 600)
        offset = 34
        if self.flip:
            offset = 40
        explosion_data = [127, 7.7, (offset, 10), [5], self.flip]
        create_explosion(explosion_rect, explosion_data, self.target, self.damage)

    def attack(self, n):
        if self.sec_hit and (self.target.hit or self.target.blocking):
            self.hit = True
        else:
            if n == 1 and self.sec_hit:
                pass
            else:
                if self.rect.colliderect(self.target.rect) and not self.sec_hit:
                    self.sec_hit = True
                    self.target.take_damage(self.damage, True, n)
                    self.create_expl()


class DamageNumber(pygame.sprite.Sprite):
    def __init__(self, rect, flip, damage):
        super().__init__(damage_num_group)
        self.damage, self.flip = f"-{str(damage)}", flip
        self.rect = rect.copy()
        self.vel_y = -0.1
        self.color = (255, 255, 255)
        self.size = 60
        if damage >= 20:
            self.size = 75
            self.color = (255, 255, 0)
        if damage >= 30:
            self.size = 90
            self.color = (255, 0, 0)

    def update(self):
        if self.rect.top > 330:
            self.kill()
        self.move()
        self.draw()

    def draw(self):
        font = pygame.font.SysFont('Times New Roman', self.size)
        black_img = font.render(self.damage, True, (0, 0, 0))
        display.screen.blit(black_img, (self.rect.x + 2, self.rect.y + 2))
        img = font.render(self.damage, True, self.color)
        display.screen.blit(img, (self.rect.x, self.rect.y))

    def move(self):
        GRAVITY = 0.05
        dy = 0
        # apply gravity
        self.vel_y += GRAVITY
        dy += self.vel_y
        # update position
        self.rect.y += dy


def create_damage_number(coords, flip, damage):
    rect = pygame.Rect(coords[0], coords[1],
                       int(90 * (damage // 10)), int(90 * (damage // 10)))
    DamageNumber(rect, flip, damage)


def create_stone(rect, data, target, damage):
    Stone(rect, data, target, damage)


def create_rocket(rect, data, target, damage):
    Rocket(rect, rocket, target, damage)


def create_energy(rect, data, target, damage):
    Energy(rect, energy, target, damage)


def create_bullet(rect, data, target, damage):
    Bullet(rect, data, target, damage)


def create_knife(rect, data, target, damage):
    Knife(rect, data, target, damage)


def create_beam(rect, data, target, damage):
    Beam(rect, data, target, damage)


create_bombing = CreateBombing()
