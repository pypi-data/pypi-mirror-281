import pygame

class GameObject:
    def __init__(self, start_pos=(0, 0), size=(50, 50), speed=0, color=(255, 255, 255), image_path=None):
        self.position = list(start_pos)
        self.size = size
        self.speed = speed
        self.color = color
        self.image = None

        if image_path:
            self.load_image(image_path)

    def load_image(self, image_path):
        try:
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.image, self.size)
        except pygame.error as e:
            print(f"Unable to load image at {image_path}: {e}")
            self.image = None

    def render(self, screen):
        if self.image:
            screen.blit(self.image, self.position)
        else:
            pygame.draw.rect(screen, self.color, (*self.position, *self.size))

    def update(self):
        # Implement any logic to update the object's state here
        pass

    def keep_within_bounds(self, screen_width, screen_height):
        self.position[0] = max(0, min(self.position[0], screen_width - self.size[0]))
        self.position[1] = max(0, min(self.position[1], screen_height - self.size[1]))
