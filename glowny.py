import pygame
import math
import Physics_classes as pc
import Input_field as ifc
pygame.init()  #Initializes pygame module

#Constants
WIDTH, HEIGHT = 1000, 650 #Wymiary nominalne olienka
win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)  # Main window
pygame.display.set_caption("Particle trajectory")
FPS = 60
#Temporary physics
particle_radius = 10 # To ma być stałe

# Images
negative = pygame.transform.scale(pygame.image.load('negative.png'), (particle_radius * 2, particle_radius * 2))  #To stałe
positive = pygame.transform.scale(pygame.image.load('positive.png'), (particle_radius * 2, particle_radius * 2)) # Stałe







def main():
    running = True
    clock = pygame.time.Clock()
    objects = []
    temp_obj_pos = None
    interface_width = 0.3 * win.get_width()
    sources = []
    source_positioning = False
    charge = -20
    mass = 100
    source_charge = 20

    # Pola fizyczne
    uniform_electric_field_on = False
    uniform_magnetic_field_on = False
    e_field_strength = 0.5
    m_field_strength = 0.5
    e_field_direction='Left'
    m_field_direction='In'

    #Pola wyboru
    font = pygame.font.SysFont(None, 24)
    dropdown_e_direction = ifc.Dropdown(20, 490, 120, 24, font,
                                    main_color=pygame.Color('white'),
                                    option_color=pygame.Color('lightgray'),
                                    options=["Left", "Right", "Up", "Down"])
    dropdown_m_direction = ifc.Dropdown(20, 230, 120, 24, font,
                                    main_color=pygame.Color('white'),
                                    option_color=pygame.Color('lightgray'),
                                    options=["In","Out"])
    # Checkbox pola
    checkbox_electric = ifc.Checkbox(20, 390, "Pole jednorodne elektryczne", uniform_electric_field_on) #chyba git
    checkbox_magnetic = ifc.Checkbox(20, 263, "Pole jednorodne magnetyczne", uniform_magnetic_field_on) #chyba git
    checkbox_source = ifc.Checkbox(20, 130, "Pole centralne elektryczne", source_positioning)   #chyba git

    # Input pola
    input_mass = ifc.TextInput(20, 40, 120, 24, str(mass))
    input_charge = ifc.TextInput(20, 90, 120, 24, str(charge))
    input_source_charge = ifc.TextInput(20, 180, 120, 24, str(source_charge))
    input_e_strength = ifc.TextInput(20, 440, 120, 24, str(e_field_strength))
    input_m_strength = ifc.TextInput(20, 310, 120, 24, str(m_field_strength))




    while running:
        win.fill('black')
        clock.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                dropdown_clicked = (
                    dropdown_e_direction.was_clicked(event.pos) or
                    dropdown_m_direction.was_clicked(event.pos)
                )
            else:
                dropdown_clicked = False

            #Dropdown obsługa
            dropdown_e_direction.handle_event(event)
            dropdown_m_direction.handle_event(event)
            # Checkbox obługa

            if not dropdown_clicked:
                checkbox_electric.handle_event(event)
                checkbox_magnetic.handle_event(event)
                checkbox_source.handle_event(event)

            # Pola wejściowe
            input_e_strength.handle_event(event)
            input_m_strength.handle_event(event)
            input_mass.handle_event(event)
            input_charge.handle_event(event)
            input_source_charge.handle_event(event)


            if source_positioning:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x_t, y_t = mouse_pos
                    if x_t>interface_width:
                        source = pc.Source(x_t, y_t, source_charge)
                        sources.append(source)
                        source_positioning = False
                        checkbox_source.checked=not checkbox_source.checked
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if sources:
                        temp = sources[0]
                        if event.button == 3 and temp.x < x < temp.x + temp.size and temp.y < y < temp.y + temp.size:
                            sources.pop()
                        elif event.button == 1:
                            if temp_obj_pos and temp_obj_pos[0] > interface_width:
                                obj = pc.create_particle(temp_obj_pos, mouse_pos, charge, mass)
                                objects.append(obj)
                                temp_obj_pos = None
                            else:
                                temp_obj_pos = mouse_pos
                    else:
                        if temp_obj_pos and temp_obj_pos[0] > interface_width:
                            obj = pc.create_particle(temp_obj_pos, mouse_pos, charge, mass)
                            objects.append(obj)
                            temp_obj_pos = None
                        else:
                            temp_obj_pos = mouse_pos

        uniform_electric_field_on = checkbox_electric.checked
        uniform_magnetic_field_on = checkbox_magnetic.checked
        source_positioning = checkbox_source.checked

        try:
            e_field_strength = float(input_e_strength.text)
            e_field_direction = dropdown_e_direction.get_selected()
            mass = float(input_mass.text)
            m_field_strength = float(input_m_strength.text)
            m_field_direction=dropdown_m_direction.get_selected()
            charge = float(input_charge.text)
            source_charge=float(input_source_charge.text)
        except ValueError:
            pass

        # Interfejs
        pygame.draw.rect(win, 'white', (0, 0, interface_width, win.get_height()))

        if uniform_electric_field_on:
            pc.draw_electric_field(win, e_field_direction, e_field_strength, color='red', start=interface_width)
        if uniform_magnetic_field_on:
           pc.draw_magnetic_field(win, direction=m_field_direction, color=(0, 0, 255), start=interface_width)

        if temp_obj_pos:
            if temp_obj_pos[0] > interface_width:
                x, y = temp_obj_pos
                pygame.draw.line(win, 'red', (x + particle_radius, y + particle_radius), mouse_pos, 2)
                if charge < 0:
                    win.blit(negative, temp_obj_pos)
                else:
                    win.blit(positive, temp_obj_pos)

        if len(sources) != 0:
            sources[0].draw(win)

        for obj in objects[:]:
            off_screen = obj.x < interface_width or obj.x > win.get_width() or obj.y < 0 or obj.y > win.get_height()
            if off_screen:
                objects.remove(obj)
                continue

            if len(sources) != 0:
                distance = math.sqrt((obj.x - sources[0].x - sources[0].size / 2) ** 2 +
                                     (obj.y - sources[0].y - sources[0].size / 2) ** 2)
                obj.move(sources[0])
                if distance < sources[0].size / 2:
                    objects.remove(obj)
                    continue

            if uniform_electric_field_on:
                obj.move_uniform(e_field_direction, e_field_strength, field_type="Electric")
            elif uniform_magnetic_field_on:
                obj.move_uniform(m_field_direction, m_field_strength, field_type="Magnetic")
            else:
                obj.x += obj.vel_x
                obj.y += obj.vel_y

            obj.draw(win)

        for i, p1 in enumerate(objects):
            for p2 in objects[i + 1:]:
                if pc.check_collision(p1, p2):
                    objects.remove(p1)
                    objects.remove(p2)
                    break
                        



        font = pygame.font.SysFont(None, 24)

       #Etikiety

        mass_label = font.render("Masa cząstki", True, pygame.Color('black'))
        charge_label = font.render("Ładunek cząstki", True, pygame.Color('black'))
        e_label = font.render("Siła pola elektrycznego", True, pygame.Color('black'))
        m_label = font.render("Moc siły pola magnetycznego", True, pygame.Color('black'))
        dir_label = font.render("Kierunek pola elektrycznego", True, pygame.Color('black'))
        source_charge_label = font.render("Źródło ładunku centralnego ", True, pygame.Color('black'))
        m_direction_label = font.render("Kierunek pola magnetycznego", True, pygame.Color('black'))





        font = pygame.font.SysFont(None, 24)

        win.blit(mass_label, (20, 20)) #Masa cząstki
        win.blit(charge_label, (20,70)) #Ładunek cząstki
        win.blit(m_label, (20, 290))   #Moc siły pola magnetycznego
        win.blit(e_label, (20, 420)) #Siła pola elektrycznego
        win.blit(dir_label, (20, 470))  #kierunek pola elektrycznego
        win.blit(source_charge_label, (20, 160)) #Źródło ładunku centralnego
        win.blit(m_direction_label, (20, 210))  #Kierunek pola magnetycznego


        # Rysowanie elementów interfejsu

        checkbox_electric.draw(win)
        checkbox_magnetic.draw(win)
        checkbox_source.draw(win)
        input_e_strength.draw(win)
        input_m_strength.draw(win)
        input_mass.draw(win)
        input_charge.draw(win)
        input_source_charge.draw(win)
        dropdown_e_direction.draw(win)
        dropdown_m_direction.draw(win)
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
