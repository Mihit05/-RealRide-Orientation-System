import pygame

class BikeVisualizer:
    def __init__(self, width=800, height=600):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Roll + Pitch Visualization")
        self.clock = pygame.time.Clock()

        self.width = width
        self.height = height

        self.bike_width = 200
        self.bike_height = 20

        self.font = pygame.font.SysFont(None, 30)

        # Create bike surface once
        self.bike_surface = pygame.Surface((self.bike_width, self.bike_height), pygame.SRCALPHA)
        self.bike_surface.fill((0, 255, 0))

    # =====================
    # DRAW BIKE
    # =====================
    def draw_bike(self, roll, pitch, control, speed):
        self.screen.fill((30, 30, 30))

        # Clamp values
        roll = max(min(roll, 90), -90)
        pitch = max(min(pitch, 45), -45)

        # Roll → rotation
        rotated = pygame.transform.rotate(self.bike_surface, -roll)

        # Pitch → vertical shift
        y_offset = int(pitch * 3)

        rect_pos = rotated.get_rect(center=(self.width // 2,
                                            self.height // 2 + y_offset))

        self.screen.blit(rotated, rect_pos)

        # Draw ground reference
        pygame.draw.line(self.screen, (100, 100, 100),
                         (0, self.height // 2),
                         (self.width, self.height // 2), 2)

        # Draw control arrow (based on roll OR pitch)
        self.draw_arrow(control)

        # Display values
        text = self.font.render(
            f"Roll: {roll:.2f}  Pitch: {pitch:.2f}",
            True, (255,255,255)
        )
        self.screen.blit(text, (20, 20))
        speed_text = self.font.render(f"Speed: {speed:.2f} km/h", True, (255,255,255))
        self.screen.blit(speed_text, (20, 60))

    # =====================
    # DRAW ARROW (horizontal for roll control)
    # =====================
    def draw_arrow(self, control):
        center_x = self.width // 2
        center_y = self.height // 2

        length = 80
        max_control = 50

        control = max(min(control, max_control), -max_control)

        # For roll → horizontal arrow
        direction = -control / max_control

        end_x = center_x + int(direction * length)
        end_y = center_y

        color = (255, 0, 0)

        pygame.draw.line(self.screen, color,
                         (center_x, center_y),
                         (end_x, end_y), 5)

        pygame.draw.circle(self.screen, color, (end_x, end_y), 6)

    # =====================
    # UPDATE LOOP
    # =====================
    def update(self, roll, pitch, control, speed):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        self.draw_bike(roll, pitch, control, speed)
        pygame.display.flip()
        self.clock.tick(60)

        return True

    def close(self):
        pygame.quit()