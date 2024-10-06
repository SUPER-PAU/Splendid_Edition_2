import pygame
# группа со спрайтами
all_sprites = pygame.sprite.Group()
bullet_sprites = pygame.sprite.Group()

attack_group = pygame.sprite.Group()
enemy_attack_group = pygame.sprite.Group()

damage_num_group = pygame.sprite.Group()

# Спрайты персов
aksenov = r"assets\images\main hero\Sprites\aksenov.png"
lisa = r"assets\images\main hero\Sprites\lisa.png"
lisa_boss = r"assets\images\main hero\Sprites\lisa_boss.png"
soldier = r"assets\images\main hero\Sprites\soldier.png"
yacugi = r"assets\images\main hero\Sprites\yakugi.png"
soldier_japan = r"assets\images\main hero\Sprites\japanese_soldier.png"
police = r"assets\images\main hero\Sprites\police.png"
negrominator = r"assets\images\main hero\Sprites\negrominator.png"
artestro = r"assets\images\main hero\Sprites\artestro.png"
general = r"assets\images\main hero\Sprites\generall.png"
super_pau = r"assets\images\main hero\Sprites\SUPERPAUK.png"
super_pau_boss = r"assets\images\main hero\Sprites\Superpau.png"
SUPER_PAU = r"assets\images\main hero\Sprites\SUPER_PAU.png"
bt25t = r"assets\images\main hero\Sprites\bt.png"
moiseev = r"assets\images\main hero\Sprites\moiseev.png"
tagir = r"assets\images\main hero\Sprites\tagir.png"
egor = r"assets\images\main hero\Sprites\egor.png"
kingartema = r"assets\images\main hero\Sprites\kingartema.png"
vesisa = r"assets\images\main hero\Sprites\vesisa.png"
bulat = r"assets\images\main hero\Sprites\bulat.png"
robot_woman = r"assets\images\main hero\Sprites\robot_womon.png"
moiseev_security = r"assets\images\main hero\Sprites\soldier_mais.png"
walker = r"assets\images\main hero\Sprites\strider.png"
trio = r"assets\images\main hero\Sprites\trio.png"
supertank = r"assets\images\main hero\Sprites\supertank.png"
albinos = r"assets\images\main hero\Sprites\albinos.png"
moiseev_bot = r"assets\images\main hero\Sprites\moiseev_bot.png"
moiseev_robot = r"assets\images\main hero\Sprites\mois_robot.png"

super_pau_2 = r"assets\images\main hero\Sprites_2\SUPER_PAU.png"
lisa_2 = r"assets\images\main hero\Sprites_2\lisa.png"
vesisa_2 = r"assets\images\main hero\Sprites_2\vesisa.png"
tagir_2 = r"assets\images\main hero\Sprites_2\tagir.png"
artestro_2 = r"assets\images\main hero\Sprites_2\artestro.png"
aksenov_2 = r"assets\images\main hero\Sprites_2\aksenov.png"
bulat_2 = r"assets\images\main hero\Sprites_2\bulat.png"
robot_woman_2 = r"assets\images\main hero\Sprites_2\robot_woman.png"
bt25t_2 = r"assets\images\main hero\Sprites_2\bt25t.png"
egor_2 = r"assets\images\main hero\Sprites_2\egor.png"
kingartema_2 = r"assets\images\main hero\Sprites_2\dumpling.png"

# партиклы
blood = pygame.image.load(r"assets\images\main hero\particles\blood.png").convert_alpha()
electricity = pygame.image.load(r"assets\images\main hero\particles\electrisity.png").convert_alpha()
bt_parts = pygame.image.load(r"assets\images\main hero\particles\bt_parts.png").convert_alpha()
dumplings = pygame.image.load(r"assets\images\main hero\particles\dumpling.png").convert_alpha()
dust = pygame.image.load(r"assets\images\main hero\particles\dust.png").convert_alpha()
shield_parts = pygame.image.load(r"assets\images\main hero\particles\shield_parts.png").convert_alpha()
bag = pygame.image.load(r"assets\images\main hero\particles\bag.png").convert_alpha()
on_fire = pygame.image.load(r"assets\images\main hero\particles\fire.png").convert_alpha()

blood_splash = pygame.image.load(r"assets\images\main hero\particles\blood_splash.png").convert_alpha()
electricity_splash = pygame.image.load(r"assets\images\main hero\particles\electricity_splash.png").convert_alpha()
dust_splash = pygame.image.load(r"assets\images\main hero\particles\dust_splash.png").convert_alpha()
bt_splash = pygame.image.load(r"assets\images\main hero\particles\bt_splash.png").convert_alpha()
shield_splash = pygame.image.load(r"assets\images\main hero\particles\shield_splash.png").convert_alpha()

energy = pygame.image.load(r"assets\images\main hero\particles\energy.png").convert_alpha()
explosion = pygame.image.load(r"assets\images\main hero\particles\explosion.png").convert_alpha()
bullet = pygame.image.load(r"assets\images\main hero\particles\bullet.png").convert_alpha()
beam = pygame.image.load(r"assets\images\main hero\particles\beam.png").convert_alpha()
rocket = pygame.image.load(r"assets\images\main hero\particles\rocket.png").convert_alpha()
stone = pygame.image.load(r"assets\images\main hero\particles\stone.png").convert_alpha()
knifes = pygame.image.load(r"assets\images\main hero\particles\knifes.png").convert_alpha()
knife = pygame.image.load(r"assets\images\main hero\particles\knife.png").convert_alpha()
green_energy = pygame.image.load(r"assets\images\main hero\particles\green_energy.png").convert_alpha()
grenade = pygame.image.load(r"assets\images\main hero\particles\grenade.png").convert_alpha()
