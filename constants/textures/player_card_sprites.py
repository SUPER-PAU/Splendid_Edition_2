import pygame


dead = pygame.image.load(r"assets\images\main hero\card_sprites\dead.png").convert_alpha()
picked = pygame.image.load(r"assets\images\main hero\card_sprites\pikced.png").convert_alpha()
clicked = pygame.image.load(r"assets\images\main hero\card_sprites\card_click.png").convert_alpha()
aksenov = pygame.image.load(r"assets\images\main hero\card_sprites\aks.png").convert_alpha()
pau = pygame.image.load(r"assets\images\main hero\card_sprites\pau.png").convert_alpha()
bt25 = pygame.image.load(r"assets\images\main hero\card_sprites\bt25.png").convert_alpha()
lisa = pygame.image.load(r"assets\images\main hero\card_sprites\lisa.png").convert_alpha()
vesisa = pygame.image.load(r"assets\images\main hero\card_sprites\vesisa.png").convert_alpha()
tagir = pygame.image.load(r"assets\images\main hero\card_sprites\tagir.png").convert_alpha()
aynur = pygame.image.load(r"assets\images\main hero\card_sprites\aynur.png").convert_alpha()
bulat = pygame.image.load(r"assets\images\main hero\card_sprites\bulat.png").convert_alpha()
egor = pygame.image.load(r"assets\images\main hero\card_sprites\egor.png").convert_alpha()
kingartema = pygame.image.load(r"assets\images\main hero\card_sprites\kingartema.png").convert_alpha()


card_by_name = {
    "lisa": lisa,
    "pau": pau,
    "vesisa": vesisa,
    "tagir": tagir,
    "aksenov": aksenov,
    "bt25": bt25,
    "aynur": aynur,
    "bulat": bulat,
    "egor": egor,
    "kingartema": kingartema
}

