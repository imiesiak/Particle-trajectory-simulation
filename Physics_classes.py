import pygame
import math
k=500
class Particle(pygame.sprite.Sprite):
    def __init__(self,x,y,vel_x,vel_y,mass,charge):
        self.x=x
        self.y=y
        self.vel_x=vel_x
        self.vel_y=vel_y
        self.mass=mass
        self.charge=charge
        self.size=20 
    def move(self,field=None):
        distance=math.sqrt((self.x-field.x)**2 + (self.y-field.y)**2)
        force=-(k*self.charge*field.charge)/(distance)**2
        acceleration=force/self.mass
        angle=math.atan2(field.y-self.y,field.x-self.x)
        acc_x=acceleration*math.cos(angle)
        acc_y=acceleration*math.sin(angle)
        self.vel_x+=acc_x
        self.vel_y+=acc_y
        self.x+=self.vel_x
        self.y+=self.vel_y
    def move_uniform(self,field_direction, field_strenght,field_type):
        if field_type=="Electric":
                match field_direction:
                    case 'Left':
                        self.vel_x -= field_strenght*(self.charge/self.mass)
                    case 'Right':
                        self.vel_x += field_strenght*(self.charge/self.mass)
                    case 'Down':
                        self.vel_y += field_strenght * (self.charge / self.mass)
                    case 'Up':
                        self.vel_y -= field_strenght * (self.charge / self.mass)
        else:
            match field_direction:
                case "In":
                    self.vel_x+=(self.charge/self.mass)*self.vel_y*field_strenght
                    self.vel_y-=(self.charge/self.mass)*self.vel_x*field_strenght
                case 'Out':
                    self.vel_x-=(self.charge/self.mass)*self.vel_y*field_strenght
                    self.vel_y+=(self.charge/self.mass)*self.vel_x*field_strenght


                
        self.x+=self.vel_x
        self.y+=self.vel_y
        







class Negative_particle(Particle):
    def __init__(self, x, y, vel_x, vel_y, mass, charge):
        super().__init__(x, y, vel_x, vel_y, mass, charge)
        self.image=pygame.transform.scale(pygame.image.load('negative.png'),(self.size,self.size))
        self.rect=self.image.get_rect()
    
    def draw(self,surface):
        surface.blit(self.image,(self.x,self.y))
    
    def move(self,field=None):
        super().move(field)

    def move_uniform(self, field_direction, field_strenght, field_type):
        super().move_uniform(field_direction, field_strenght, field_type)
    
        
        

class Positive_particle(Particle):
    def __init__(self, x, y, vel_x, vel_y, mass, charge):
        super().__init__(x, y, vel_x, vel_y, mass, charge)
        self.image=pygame.transform.scale(pygame.image.load('positive.png'),(self.size,self.size))
    
    def draw(self,surface):
        surface.blit(self.image,(self.x,self.y))

    def move(self,field):
        super().move(field) 
    
    def move_uniform(self, field_direction, field_strenght, field_type):
        super().move_uniform(field_direction, field_strenght, field_type)

class Source:
    def __init__(self,x,y,charge):
        self.x=x
        self.y=y
        self.charge=charge
        self.size=60
        if charge<0:
            self.image=pygame.transform.scale(pygame.image.load('negative.png'),(self.size,self.size))
        else:
            self.image=pygame.transform.scale(pygame.image.load('positive.png'),(self.size,self.size))
    def draw(self,surface):
        surface.blit(self.image,(self.x,self.y))





def create_particle(Location, mouse,charge,mass):
    t_x,t_y=Location
    m_x,m_y=mouse
    vel_x=int((m_x-t_x)/25)
    vel_y=int((m_y-t_y)/25)
    if charge<0:
        obj=Negative_particle(t_x,t_y,vel_x,vel_y,mass,charge)
    else:
        obj=Positive_particle(t_x,t_y,vel_x,vel_y,mass,charge)
    return obj

def check_collision(p1, p2):
    dx = p1.x - p2.x
    dy = p1.y - p2.y
    distance = math.hypot(dx, dy)
    return distance < (p1.size // 2 + p2.size // 2)




def draw_electric_field(surface, direction, strength, color, start, spacing=40):
    width, height = surface.get_width(), surface.get_height()
    if direction == 'Right':
        for y in range(0, height, spacing):
            pygame.draw.line(surface, color, (start, y), (width, y), 1)
            pygame.draw.polygon(surface, color, [(width - 10, y - 5),
                                                 (width, y),
                                                 (width - 10, y + 5)])
    elif direction == 'Left':
        for y in range(0, height, spacing):
            pygame.draw.line(surface, color, (width, y), (start, y), 1)
            pygame.draw.polygon(surface, color, [(start + 10, y - 5),
                                                 (start, y),
                                                 (start + 10, y + 5)])
    elif direction == 'Down':
        for x in range(int(start)+5, width, spacing):
            pygame.draw.line(surface, color, (x, 0), (x, height), 1)
            pygame.draw.polygon(surface, color, [(x - 5, height - 10),
                                                 (x, height),
                                                 (x + 5, height - 10)])
    elif direction == 'Up':
        for x in range(int(start)+5, width, spacing):
            pygame.draw.line(surface, color, (x, 0), (x, height), 1)
            pygame.draw.polygon(surface, color, [(x - 5,  10),
                                                 (x, 0),
                                                 (x + 5,  10)])
            

def draw_magnetic_field(surface, direction, color,start, spacing=40, radius=8):
    width, height = surface.get_width(), surface.get_height()

    for x in range(int(start)+10, width, spacing):
        for y in range(spacing // 2, height, spacing):
            # Rysuj okrąg
            pygame.draw.circle(surface, color, (x, y), radius, 1)

            if direction == 'Out':  # z ekranu
                pygame.draw.circle(surface, color, (x, y), 2)  # kropka w środku
            elif direction == 'In':  # do ekranu
                pygame.draw.line(surface, color, (x - 3, y - 3), (x + 3, y + 3), 1)
                pygame.draw.line(surface, color, (x - 3, y + 3), (x + 3, y - 3), 1)