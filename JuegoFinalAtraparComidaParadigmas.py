import pygame, random, os # Importo los módulos.

# CLASES.
class Personaje(pygame.sprite.Sprite): #Clase que representa el personaje.
    def __init__(self, type): # Método para iniciar los atributos del personaje.
        super().__init__() # Llama al constructor de la clase padre (Sprite). 

        if type == 'niña':  # Caso de que el tipo de personaje sea niña.
            image = pygame.image.load('juegofinal/personajeniñaa.png').convert_alpha()

        image = pygame.transform.smoothscale(image, (96, 96)) # Agrego nuevas dimensiones para la imagen.

        self.image = image # Creo la imagen que aparecerá en la pantalla.
        self.rect = self.image.get_rect(midleft = (0, ventana_y // 2)) # Establezco la posicion en la ventana en la que se va a dibujar al personaje.
        self.velocidad = 10 # Establezco la velocidad en la que se va a mover el personaje.

    def movimiento(self): # Función para el movimiento del personaje.
        teclas = pygame.key.get_pressed()

        if (teclas[pygame.K_w] or teclas[pygame.K_UP]) and self.rect.top > 0: #Caso de que se presione la tecla w o fecla para arriba y la linea superior del rectangulo del personaje sea mayor que 0.
            self.rect.y -= self.velocidad
        elif (teclas[pygame.K_s] or teclas[pygame.K_DOWN]) and self.rect.bottom < ventana_y: #Caso de que se presione la tecla s o flecha para abajo y la linea inferior del rectangulo del personaje sea menor a la ventana del juego.
            self.rect.y += self.velocidad

    def update(self): # Función para actualizar e implementar el movimiento del personaje.
        self.movimiento()

class Comida(pygame.sprite.Sprite): #Clase que representa la comida.
    def __init__(self, type): # Metodo para iniciar los atributos de la comida.
        super().__init__() # Llama al constructor de la clase padre (Sprite).

        self.type = type

        if self.type == 'saludable': # Caso de que el tipo de comida sea saludable.
            comida_item = pygame.image.load('juegofinal/saludable/' + random.choice(saludable_comida))
        elif self.type == 'chatarra': # Caso de que el tipo de comida sea chatarra.
            comida_item = pygame.image.load('juegofinal/chatarra/' + random.choice(chatarra_comida))

        self.image = comida_item # Creo la imagen que aparecerá en la pantalla.
        # Establezco la posición en la ventana en la que se van a dibujar las comidas.
        self.rect = self.image.get_rect() 
        self.rect.x = random.randint(ventana_x, ventana_x + 200) #**
        self.rect.y = random.randint(0, ventana_y - 64) #**
        self.velocidad = random.randint(3, 13) #**

    def update(self): # Función para actualizar e implementar la velocidad.
        self.rect.x -= self.velocidad

    def destruir(self): # Función para destruir la comida si se sale del eje x.
        if self.rect.x <= 0:
            self.kill()

class Juego(): # Clase que representa el juego.
    def __init__(self): # Metodos para iniciar los atributos del juego.
        self.personaje = None
        # Inicializo los grupos.
        self.personaje_grupo = pygame.sprite.GroupSingle()

        self.comida_items_grupo = pygame.sprite.Group()

        # Declaro variables para la vida, la puntuación y el estado actual del juego.
        self.vida = 3
        self.puntuacion = 0

        self.estado = 'iniciar'

        # Sonidos.
        pygame.mixer.music.load('juegofinal/musicafondo.wav')
        pygame.mixer.music.set_volume(0.1)
        self.sonido_comida = pygame.mixer.Sound('juegofinal/efectosonidocomida.wav')

    def muestro_ventana_inicio(self): # Función para las variables que voy a mostrar en la ventana al iniciar.
        # Textos.
        titulo_texto = fuente_titulo.render('Atrapa la comida', True, negro)
        titulo_rect = titulo_texto.get_rect(center = (ventana_x // 2, ventana_y // 2 - 50))

        info_texto = fuente_contenido.render('Atrapa la comida sana y evita la comida chatarra', True, negro)
        info_rect = info_texto.get_rect(center = (ventana_x // 2, ventana_y // 2 + 20))

        iniciar_texto = fuente_contenido.render('Click aquí para iniciar el juego', True, negro)
        iniciar_rect = iniciar_texto.get_rect(center = (ventana_x // 2, ventana_y // 2 + 200))

        # Cargo la imagen del personaje.
        self.niña_img = pygame.image.load('juegofinal/derecha.png').convert_alpha()
        # Establezco la posición inicial del personaje.
        self.niña_rect = self.niña_img.get_rect(midleft = (300, ventana_y // 2 + 100))

        # Coloreo la ventana y cargo el fondo de la misma.
        ventana.fill(negro)
        ventana.blit(fondo, fondo_rect)

        # Muestro los textos en la ventana.
        ventana.blit(titulo_texto, titulo_rect)
        ventana.blit(info_texto, info_rect)
        ventana.blit(iniciar_texto, iniciar_rect)

        # Verifico si el usuario dió click en donde se le indicó que lo hiciera.
        if iniciar_rect.collidepoint(pygame.mouse.get_pos()): # Caso de que el usuario posiciono el puntero del mouse dentro de el rectangulo.
            pygame.draw.rect(ventana, amarillo, iniciar_rect, 2)
        else: # Caso de que el usuario no haya posicionado el puntero del mouse dentro de el rectangulo.
            pygame.draw.rect(ventana, blanco, iniciar_rect, 2)

    def añadir_comida(self, comida_item): # Función para añadir las comidas a un grupo de comidas.
        self.comida_items_grupo.add(comida_item)

    def update(self): # Función para las actualizaciones del estado del juego
        self.entrada_usuario() # Eventos donde se esperan las interacciones del usuario.

        # Estados del juego.
        if self.estado == 'iniciar': # Caso de que el estado sea iniciar.
            self.muestro_ventana_inicio() 
        elif self.estado == 'jugar': # Caso de que el estado sea jugando.
            self.jugando()
            self.colisiones()
            self.comida_perdida()
            self.update_estado()
        elif self.estado == 'fin': # Caso de que el estado sea fin del juego.
            self.muestro_ventana_final()
        
    # FUNCIONES PARA EL ESTADO DEL JUEGO.
    def muestro_ventana_final(self): # Función para mostrar en la ventana cuando el estado sea fin.
        ventana.fill(negro)
        ventana.blit(fondo, fondo_rect)

        # Textos.
        puntuacion_texto = fuente_contenido.render(' PUNTAJE: ' + str(self.puntuacion) + ' ', True, negro)
        puntuacion_rect = puntuacion_texto.get_rect(center = (ventana_x // 2, ventana_y // 2))

        fin_texto = fuente_contenido.render('FIN DEL JUEGO', True, negro)
        fin_rect = puntuacion_texto.get_rect(center = (ventana_x // 2, ventana_y // 2 + 40))

        # Muestro los textos en la ventana.
        ventana.blit(puntuacion_texto, puntuacion_rect)
        ventana.blit(fin_texto, fin_rect)

    def update_estado(self): # Función para cuando se esté jugando, actualizar la vida y el puntaje del personaje.
        # Textos.
        puntuacion_texto = fuente_contenido.render('PUNTUACIÓN: ' + str(self.puntuacion) + ' ', True, negro)
        puntuacion_rect = puntuacion_texto.get_rect(center = (ventana_x // 2, 20))

        vida_texto = fuente_contenido.render('VIDA(S): ' + str(self.vida) + ' ', True, negro)
        vida_rect = vida_texto.get_rect(center = (ventana_x // 2, ventana_y - 20))

        # Muestro los textoos en la ventana.
        ventana.blit(puntuacion_texto, puntuacion_rect)
        ventana.blit(vida_texto, vida_rect)

    def comida_perdida(self): # Función para descontar vida en caso de que se no se agarre una comida sana.
        for comida_item in self.comida_items_grupo: #**
            if comida_item.rect.right < 0 and comida_item.type == 'saludable': # Caso de que una comida sana salga de la ventana.
                self.vida -= 1
                comida_item.destruir()

                if self.vida <= 0: # Caso de que la vida llegue a 0.
                    self.estado = 'fin'

    def colisiones(self): # Función para verificar si hubo colisiones entre el personaje y los alimentos.
        choque_comida = pygame.sprite.spritecollideany(self.personaje, self.comida_items_grupo)

        if choque_comida: # Caso de que si haya colision.
            self.sonido_comida.play()
            if choque_comida.type == 'saludable': # Caso de que dicha colision haya sido con la comida saludable.
                self.puntuacion += 1
            else: # Caso de que dicha colision haya sido con la comida chatarra.
                if self.puntuacion >= 0.5:
                    self.puntuacion -= 0.5

            # Se eliminan los alimentos que chocan contra el personaje.
            choque_comida.remove(self.comida_items_grupo)

    def jugando(self): # Función para cuando se está jugando.
        ventana.fill(negro)
        ventana.blit(fondo, fondo_rect)

        self.personaje_grupo.draw(ventana) # Se dibujan los personajes y las actualizaciones.
        self.personaje_grupo.update()

        self.comida_items_grupo.draw(ventana) # Se dibujan las comidas y las actualizaciones.
        self.comida_items_grupo.update()

    def entrada_usuario(self): # Función para el inicio del juego.
        if self.estado == 'iniciar': # Caso de que el jugador inicie el juego.
            personaje_type = "niña"  

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # Caso de que el usuario haya clickeado en "Click aquí para iniciar el juego"
                if personaje_type: # Se agrega el personaje al grupo y el estado del juego pasa a ser "jugar" 
                    personaje = Personaje(personaje_type)
                    self.personaje_grupo.add(personaje)
                    self.personaje = personaje
                    self.estado = 'jugar' 
                    pygame.mixer.music.play(-1)
        if self.estado == 'fin': # Caso de que el jugador pierda el juego.
            pygame.mixer.music.stop()
            

pygame.init() # Inicialización de pygame.

# Medidas y nombre de la ventana.
ventana_x = 900
ventana_y = 596
ventana = pygame.display.set_mode((ventana_x, ventana_y))
pygame.display.set_caption('Atrapa la comida')

# Reloj.
FPS = 60 
reloj = pygame.time.Clock()

# Paleta de colores.
negro = (0, 0, 0)
blanco = (255, 255, 255)
amarillo = (255, 153, 0)

# Imagen de fondo.
fondo = pygame.image.load('juegofinal/fondocomidaa.jpg').convert_alpha()
fondo_rect = fondo.get_rect(topleft = (0, 0))

# Fuentes de texto.
fuente_titulo = pygame.font.SysFont('comicsans', 84)
fuente_contenido = pygame.font.SysFont('comicsans', 32)

# Variables con las imagenes de los alimentos.
saludable_comida = [f for f in os.listdir('juegofinal/saludable') if os.path.join('juegofinal/saludable', f)]
chatarra_comida = [f for f in os.listdir('juegofinal/chatarra') if os.path.join('juegofinal/chatarra', f)]

# Variable de tiempo.
comida_item_tiempo = pygame.USEREVENT + 1
pygame.time.set_timer(comida_item_tiempo, 1000) # Tiempo en el que van a aparecer las comidas.

# Inicialización del juego.
mi_juego = Juego() #Llamo a la clase Juego.

corriendo = True
while corriendo: # Bucle principal del juego.
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Caso de que se deje de jugar.
            corriendo = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: # Caso de que se presione la tecla escape.
            corriendo = False
        if mi_juego.estado == 'jugar': # Caso de que se esté jugando, aparecerán las comidas aleatoriamente.
            if event.type == comida_item_tiempo:
                mi_juego.añadir_comida(Comida(random.choice(['saludable','chatarra'])))

    mi_juego.update() # Actualizaciones del juego.

    pygame.display.update() # Actualización de la ventana.
    reloj.tick(FPS) # Implemento en el reloj los fps.

pygame.quit() # Cierro la ventana.