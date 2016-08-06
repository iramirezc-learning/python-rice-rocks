# Author: Isaac Ramírez, iramirezc@live.com.mx
# Last date modified: 5/11/2015
# Project: Mini-project #8. "RiceRocks (Asteroids)".
# Course: An Introduction to Interactive Programming in
#         Python (Part 2) @coursera.org

import simplegui
import math
import random

# Globals for user interface
WIDTH = 800
HEIGHT = 600
max_score = 0
last_score = 0
score = 0
lives = 3
time = 0
pos = WIDTH
started = False
MAX_ROCKS = 12
SPEED = 0.1

# ImageInfo class
class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_url = {
    0: "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris3_blue.png",
    1: "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris1_brown.png",
    2: "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png",
    3: "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris4_brown.png",
    4: "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris_blend.png"
}
debris_images = {
    0: simplegui.load_image(debris_url[0]),
    1: simplegui.load_image(debris_url[1]),
    2: simplegui.load_image(debris_url[2]),
    3: simplegui.load_image(debris_url[3]),
    4: simplegui.load_image(debris_url[4]),
}
debris_image = debris_images[0]

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_url = {
    0: "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.png",
    1: "https://www.dropbox.com/s/up6by1vkwqrabb2/earth1.jpg?dl=1",
    2: "https://www.dropbox.com/s/a3zlmutc84geva5/earth3.jpg?dl=1",
    3: "https://www.dropbox.com/s/nuobotz4d4brys1/earth4.jpg?dl=1"
}
nebula_images = {
    0: simplegui.load_image(nebula_url[0]),
    1: simplegui.load_image(nebula_url[1]),
    2: simplegui.load_image(nebula_url[2]),
    3: simplegui.load_image(nebula_url[3])
}
nebula_image = nebula_images[3]

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot1.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_url = {
    0: "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png",
    1: "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_brown.png",
    2: "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blend.png"
}
asteroid_image = {
    0: simplegui.load_image(asteroid_url[0]),
    1: simplegui.load_image(asteroid_url[1]),
    2: simplegui.load_image(asteroid_url[2])
}

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_url = {
    0: "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_orange.png",
    1: "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_blue.png",
    2: "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_blue2.png",
    3: "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png"
}
explosion_image = {
    0: simplegui.load_image(explosion_url[0]),
    1: simplegui.load_image(explosion_url[1]),
    2: simplegui.load_image(explosion_url[2]),
    3: simplegui.load_image(explosion_url[3])
}

# sound assets purchased from sounddogs.com, please do not redistribute
# .ogg versions of sounds are also available, just replace .mp3 by .ogg
#soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
#missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
#explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# Recorded by Kibblesbob downloaded from http://soundbible.com/1804-M4A1-Single.html Licensed as: Attribution 3.0
# More info => https://creativecommons.org/licenses/by/3.0/
missile_sound = simplegui.load_sound("https://www.dropbox.com/s/fp8nuhuvznth71e/M4A1_Single-Kibblesbob-8540445.mp3?dl=1")
missile_sound.set_volume(.2)

# Recorded by Mike Koenig downloaded from http://soundbible.com/7-Anti-Aircraft-Gun.html Licensed as: Attribution 3.0
# More info => https://creativecommons.org/licenses/by/3.0/
explosion_sound = simplegui.load_sound("https://www.dropbox.com/s/5xnmi6t1pbqpfo3/Anti%20Aircraft.mp3?dl=1")

# Hyperbola by Tejaswi downloaded from http://sampleswap.org/artist/TranceAddict Licensed as: by-sa 
# More info => http://creativecommons.org/licenses/by-sa/3.0/
soundtrack = simplegui.load_sound("https://www.dropbox.com/s/tnfsqtpsv15i3pu/Tejaswi_Hyperbola-160.mp3?dl=1")
soundtrack.set_volume(.6)
soundtrack.rewind()
soundtrack.play()

# Helper functions to handle transformations
# Angles
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

# Distance
def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)

# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
    
    def get_pos(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
        
    def draw(self,canvas):
        center = self.image_center
        if self.thrust:
            center = [self.image_center[0] + self.image_size[0], self.image_center[1]]
        canvas.draw_image(self.image, center, self.image_size, self.pos, self.image_size, self.angle)    

    def update(self):
        # Update angle
        self.angle += self.angle_vel
        
        # Update position
        for i in range(2):
            self.pos[i] += self.vel[i]
        
        # Friction
        for i in range(2):
            self.vel[i] *= (1 - SPEED / 10)

        # Accelerate if thrust
        if self.thrust:
            acc = angle_to_vector(self.angle)
            for i in range(2):
                self.vel[i] += acc[i] * SPEED
        
        # Wrap
        self.pos[0] %= WIDTH
        self.pos[1] %= HEIGHT

    def set_thrust(self, on = False):
        self.thrust = on
        if on:
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()
       
    def set_angle_vel(self, angle_vel):
        self.angle_vel = angle_vel
        
    def shoot(self):
        global missile_group
        forward = angle_to_vector(self.angle)
        missile_pos = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
        missile_vel = [self.vel[0] + 6 * forward[0], self.vel[1] + 6 * forward[1]]
        new_missile = Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound)
        missile_group.add(new_missile)
       
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
    
    def get_pos(self):
        return self.pos
    
    def get_vel(self):
        return self.vel
    
    def get_angle(self):
        return self.angle
    
    def get_radius(self):
        return self.radius
   
    def draw(self, canvas):
        if self.animated:
            index = (self.age % self.lifespan) // 1
            center = [self.image_center[0] +  index * self.image_size[0], self.image_center[1]]
            canvas.draw_image(self.image, center, self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        # Update angle
        self.angle += self.angle_vel
        
        # Update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        
        self.age += 1
        
        if self.age >= self.lifespan:
            return True
        
        return False
    
    # Check if this object collides whit another.
    def collide(self, other_object):
        distance = dist(self.get_pos(), other_object.get_pos())
        if distance <= (self.get_radius() + other_object.get_radius()):
            return True
        return False      

# Canvas
def draw(canvas):
    global time, pos, started, lives, score
    
    # Animate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # Draw UI
    canvas.draw_text("Lives: " + str(lives), [30, 45],  18, "White", "monospace")
    canvas.draw_text("Score: " + str(score), [660, 45], 18, "White", "monospace")

    # Draw and update ship and sprites
    my_ship.draw(canvas)
    my_ship.update()
    
    process_sprite_group(canvas, rock_group)
    process_sprite_group(canvas, missile_group)
    process_sprite_group(canvas, explosion_group)
    
    # If the ship collides then looses a life
    if group_collide(rock_group, my_ship):
        lives -= 1
        # If no more lives then game over.
        if lives == 0:
            reset()
    
    # Number of missiles destroying rocks
    score += group_group_collide(rock_group, missile_group)

    # Draw splash screen if not started
    if not started:
        pos -= 1
        canvas.draw_image(splash_image, splash_info.get_center(), splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], splash_info.get_size())
        canvas.draw_text(message, (pos, HEIGHT - 20), 12, "Lime", "monospace")
        if pos < -(WIDTH + len(message) * 2):
            pos = WIDTH
        canvas.draw_text("Last Score: " + str(last_score), [605, 75],  18, "White", "monospace")
        canvas.draw_text("Max Score: "  + str(max_score),  [615, 110], 18, "White", "monospace")

# Helper function to draw collection of sprites on the canvas
def process_sprite_group(canvas, group):
    removed_items = set([])
    for sprite in group:
        sprite.draw(canvas)
        if sprite.update():
            removed_items.add(sprite)
    group.difference_update(removed_items)

# Checks if the a single sprite collides with the sprites from a group
# if so, then removes the sprite from the group.
def group_collide(group, other_object):
    group_copy = set(group)
    for sprite in group_copy:
        if sprite.collide(other_object):
            # Generate a explosion
            new_explosion = Sprite(sprite.get_pos(), sprite.get_vel(), sprite.get_angle(), 0, explosion_image[random.randrange(4)], explosion_info, explosion_sound)
            explosion_group.add(new_explosion)
            # Remove Sprite
            group_copy.discard(sprite)
            group.intersection_update(group_copy)
            return True
    return False

# Checks if the sprites from each group collide, if so, it removes them,
# then returns the number of collisions.
def group_group_collide(groupA, groupB):
    total_collisions = 0
    copyA = set(groupA)
    for spriteA in copyA:
        if group_collide(groupB, spriteA):
            copyA.discard(spriteA)
            total_collisions += 1
    groupA.intersection_update(copyA)
    return total_collisions

# Resets the game
def reset():
    global started, lives, score, last_score, max_score, rock_group, missile_group, nebula_image, debris_image
    started = False
    last_score = score
    if last_score > max_score:
        max_score = last_score
    score = 0
    lives = 3
    missile_group = set([])
    rock_group = set(())
    #soundtrack.pause()
    nebula_image = nebula_images[random.randrange(4)]
    debris_image = debris_images[random.randrange(5)]


# Timer handler that spawns a rock
def rock_spawner():
    global rock_group
    if started:
        if len(rock_group) < MAX_ROCKS:
            cvel =  ((score + 2) * 0.5) / 15.0
            rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
            #rock_vel = [random.random() * .6 - .3, random.random() * .6 - .3]
            rock_vel = [random.randint(-2, 2) * cvel, random.randint(-2, 2) * cvel]
            rock_avel = random.random() *.3 - .1
            
            new_rock = Sprite(rock_pos, rock_vel, 0, rock_avel, asteroid_image[random.randrange(3)], asteroid_info)
            distance_from_ship = dist(new_rock.get_pos(), my_ship.get_pos())
            if distance_from_ship > (new_rock.get_radius() + my_ship.get_radius() * 2):
                rock_group.add(new_rock)

# Key handlers to control ship   
def keydown(key):
    if key == simplegui.KEY_MAP['right']:
        my_ship.set_angle_vel(SPEED)
    elif key == simplegui.KEY_MAP['left']:
        my_ship.set_angle_vel(-SPEED)
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(True)
    elif key == simplegui.KEY_MAP['space']:
        my_ship.shoot()
        
def keyup(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.set_angle_vel(0)
    elif key == simplegui.KEY_MAP['right']:
        my_ship.set_angle_vel(0)
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust()
        
# Mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth  = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True

def mute():
    soundtrack.pause()

def play():
    soundtrack.play()
    
# Initialize stuff
frame = simplegui.create_frame("IsaacRiceRocks", WIDTH, HEIGHT)

# Initialize ship
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)

# Group of rocks
rock_group = set([])

# Group of missiles
missile_group = set([])

# Group of explosions
explosion_group = set([])

# Register handlers
frame.set_keyup_handler(keyup)
frame.set_keydown_handler(keydown)
frame.set_mouseclick_handler(click)
frame.set_draw_handler(draw)
frame.add_button("Mute Sound", mute,100)
frame.add_button("Play Music", play,100)

timer = simplegui.create_timer(1000.0, rock_spawner)

# Get things rolling
timer.start()
frame.start()

message = "Mini-project #8 - RiceRocks (Asteroids). Developed by Isaac Ramirez as final project for the course: An Introduction to Interactive Programming in Python @ coursera.org. November 2015."