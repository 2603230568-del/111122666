
import math  # Permite calcular las ondas que forman los sonidos.
import random  # Permite elegir al azar la dirección inicial de la pelota.
import sys  # Permite terminar el programa al cerrar el juego.
from array import array  # Guarda las muestras de sonido en un formato compacto.

import pygame  # Importa la biblioteca que se usa para crear el juego.


ANCHO = 800  # Define el ancho de la ventana en píxeles.
ALTO = 500  # Define el alto de la ventana en píxeles.
FPS = 60  # Limita el juego a 60 cuadros por segundo.
META = 5  # Establece cuántos puntos se necesitan para ganar.

FONDO = (22, 27, 38)  # Guarda el color oscuro del fondo en formato RGB.
BLANCO = (240, 240, 240)  # Guarda el color claro para pelota y textos.
AZUL = (75, 160, 255)  # Guarda el color de la paleta del primer jugador.
NARANJA = (255, 170, 80)  # Guarda el color de la paleta del segundo jugador.


def crear_sonido(frecuencia, duracion=0.12):
    """Crea un sonido corto sin necesitar un archivo externo."""
    frecuencia_audio = 22050  # Establece cuántas muestras de audio se crean por segundo.
    cantidad_muestras = int(frecuencia_audio * duracion)  # Calcula cuántas muestras dura el sonido.
    muestras = array("h")  # Crea una lista de números enteros para guardar el audio.

    for numero in range(cantidad_muestras):
        tiempo = numero / frecuencia_audio  # Convierte el número de muestra en tiempo.
        volumen = 10000 * (1 - numero / cantidad_muestras)  # Hace que el sonido baje de volumen poco a poco.
        muestra = int(volumen * math.sin(2 * math.pi * frecuencia * tiempo))  # Calcula una parte de la onda de sonido.
        muestras.append(muestra)  # Agrega esa parte del sonido a la lista.

    return pygame.mixer.Sound(buffer=muestras.tobytes())  # Convierte las muestras en un sonido de Pygame.


class Paleta(pygame.sprite.Sprite):
    """Representa una de las paletas que controlan los jugadores."""

    def __init__(self, x, color):
        super().__init__()  # Inicializa las características básicas del sprite.
        self.image = pygame.Surface((14, 90))  # Crea la imagen rectangular de la paleta.
        self.image.fill(color)  # Pinta la paleta con el color recibido.
        self.rect = self.image.get_rect(center=(x, ALTO // 2))  # Coloca la paleta en su posición inicial.
        self.velocidad = 6  # Define cuántos píxeles se mueve la paleta.

    def mover(self, arriba, abajo):
        teclas = pygame.key.get_pressed()  # Consulta cuáles teclas están presionadas.

        if teclas[arriba]:
            self.rect.y -= self.velocidad  # Si se presiona arriba, mueve la paleta hacia arriba.
        if teclas[abajo]:
            self.rect.y += self.velocidad  # Si se presiona abajo, mueve la paleta hacia abajo.

        # Evita que la paleta salga de la ventana.
        self.rect.top = max(0, self.rect.top)  # Evita que la parte superior pase del borde superior.
        self.rect.bottom = min(ALTO, self.rect.bottom)  # Evita que la parte inferior pase del borde inferior.


class Pelota(pygame.sprite.Sprite):
    """Representa la pelota y su movimiento."""

    def __init__(self):
        super().__init__()  # Inicializa las características básicas del sprite.
        self.image = pygame.Surface((18, 18))  # Crea una imagen cuadrada para la pelota.
        self.image.fill(BLANCO)  # Pinta la pelota de color blanco.
        self.rect = self.image.get_rect(center=(ANCHO // 2, ALTO // 2))  # Sitúa la pelota en el centro.
        self.velocidad_x = 0  # Inicia la pelota sin movimiento horizontal.
        self.velocidad_y = 0  # Inicia la pelota sin movimiento vertical.

    def sacar(self):
        # La pelota empieza a moverse en una dirección al azar.
        direccion = random.choice((-1, 1))  # Elige si la pelota sale hacia la izquierda o la derecha.
        self.velocidad_x = 5 * direccion  # Establece la velocidad horizontal con la dirección elegida.
        self.velocidad_y = 3  # Establece la velocidad vertical inicial.

    def reiniciar(self):
        self.rect.center = (ANCHO // 2, ALTO // 2)  # Regresa la pelota al centro de la ventana.
        self.velocidad_x = 0  # Detiene el movimiento horizontal.
        self.velocidad_y = 0  # Detiene el movimiento vertical.

    def mover(self):
        self.rect.x += self.velocidad_x  # Actualiza la posición horizontal de la pelota.
        self.rect.y += self.velocidad_y  # Actualiza la posición vertical de la pelota.


def centrar_texto(pantalla, fuente, mensaje, color, y):
    imagen = fuente.render(mensaje, True, color)  # Convierte el mensaje en una imagen que Pygame puede dibujar.
    posicion = imagen.get_rect(center=(ANCHO // 2, y))  # Calcula la posición para centrar el texto.
    pantalla.blit(imagen, posicion)  # Dibuja el texto en la ventana.


def main():
    pygame.init()  # Prepara los módulos de Pygame para usarlos.
    pantalla = pygame.display.set_mode((ANCHO, ALTO))  # Crea la ventana del juego.
    pygame.display.set_caption("Pong - Proyecto final de Pygame")  # Define el título de la ventana.

    sonido_golpe = None  # Reserva una variable para el sonido de los choques.
    sonido_punto = None  # Reserva una variable para el sonido al anotar puntos.
    if pygame.mixer.get_init() is None:
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=1)  # Intenta preparar el audio del juego.
        except pygame.error as error:
            # Muestra el problema, pero permite que el juego continúe sin sonido.
            print(f"No se pudo iniciar el sonido; el juego seguirá sin audio: {error}")

    if pygame.mixer.get_init() is not None:
        sonido_golpe = crear_sonido(600)  # Crea el sonido que se escucha al chocar.
        sonido_punto = crear_sonido(300, 0.2)  # Crea el sonido que se escucha al anotar.

    reloj = pygame.time.Clock()  # Crea un reloj para controlar la velocidad del juego.
    fuente_marcador = pygame.font.SysFont("Arial", 48)  # Define la fuente grande para el marcador.
    fuente_mensaje = pygame.font.SysFont("Arial", 25)  # Define la fuente para los mensajes principales.
    fuente_pequena = pygame.font.SysFont("Arial", 18)  # Define la fuente para las instrucciones.

    paleta_izquierda = Paleta(35, AZUL)  # Crea la paleta azul del jugador izquierdo.
    paleta_derecha = Paleta(ANCHO - 35, NARANJA)  # Crea la paleta naranja del jugador derecho.
    pelota = Pelota()  # Crea la pelota del juego.
    sprites = pygame.sprite.Group(paleta_izquierda, paleta_derecha, pelota)  # Agrupa los objetos que se dibujan.

    puntos_izquierda = 0  # Guarda los puntos del jugador azul.
    puntos_derecha = 0  # Guarda los puntos del jugador naranja.
    ganador = ""  # Guarda el mensaje del ganador cuando alguien llega a la meta.
    ejecutando = True  # Mantiene activo el bucle principal del juego.

    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False  # Detiene el juego cuando se cierra la ventana.

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    ejecutando = False  # Cierra el juego cuando se presiona Esc.
                elif evento.key == pygame.K_SPACE and not ganador:
                    if pelota.velocidad_x == 0:
                        pelota.sacar()  # Inicia la pelota si está detenida y aún no hay ganador.
                elif evento.key == pygame.K_r:
                    puntos_izquierda = 0  # Borra los puntos del jugador azul.
                    puntos_derecha = 0  # Borra los puntos del jugador naranja.
                    ganador = ""  # Quita el mensaje de ganador.
                    pelota.reiniciar()  # Coloca la pelota en el centro y la detiene.

        paleta_izquierda.mover(pygame.K_w, pygame.K_s)  # Mueve al jugador azul con las teclas W y S.
        paleta_derecha.mover(pygame.K_UP, pygame.K_DOWN)  # Mueve al jugador naranja con las flechas.

        if pelota.velocidad_x != 0 and not ganador:
            pelota.mover()  # Actualiza la posición mientras la pelota está en movimiento.

            # La pelota rebota en los bordes de arriba y abajo.
            if pelota.rect.top <= 0 or pelota.rect.bottom >= ALTO:
                pelota.velocidad_y *= -1  # Invierte el movimiento vertical para rebotar.
                if sonido_golpe:
                    sonido_golpe.play()  # Reproduce el sonido si el audio está disponible.

            # La pelota rebota en las paletas y cambia un poco de ángulo.
            if pygame.sprite.collide_rect(pelota, paleta_izquierda):
                if pelota.velocidad_x < 0:
                    pelota.velocidad_x = min(abs(pelota.velocidad_x) + 0.4, 9)  # La manda hacia la derecha y aumenta su rapidez.
                    diferencia = pelota.rect.centery - paleta_izquierda.rect.centery  # Mide dónde chocó respecto al centro de la paleta.
                    pelota.velocidad_y = diferencia / 12  # Cambia el ángulo según el lugar del choque.
                    if sonido_golpe:
                        sonido_golpe.play()  # Reproduce el sonido del choque.

            if pygame.sprite.collide_rect(pelota, paleta_derecha):
                if pelota.velocidad_x > 0:
                    pelota.velocidad_x = -min(abs(pelota.velocidad_x) + 0.4, 9)  # La manda hacia la izquierda y aumenta su rapidez.
                    diferencia = pelota.rect.centery - paleta_derecha.rect.centery  # Mide dónde chocó respecto al centro de la paleta.
                    pelota.velocidad_y = diferencia / 12  # Cambia el ángulo según el lugar del choque.
                    if sonido_golpe:
                        sonido_golpe.play()  # Reproduce el sonido del choque.

            # Si sale por un lado, el otro jugador gana un punto.
            if pelota.rect.right < 0:
                puntos_derecha += 1  # Suma un punto al jugador naranja.
                pelota.reiniciar()  # Coloca la pelota al centro para el siguiente saque.
                if sonido_punto:
                    sonido_punto.play()  # Reproduce el sonido del punto.
            elif pelota.rect.left > ANCHO:
                puntos_izquierda += 1  # Suma un punto al jugador azul.
                pelota.reiniciar()  # Coloca la pelota al centro para el siguiente saque.
                if sonido_punto:
                    sonido_punto.play()  # Reproduce el sonido del punto.

            if puntos_izquierda == META:
                ganador = "¡Gana el jugador azul!"  # Declara ganador al jugador azul al llegar a la meta.
            elif puntos_derecha == META:
                ganador = "¡Gana el jugador naranja!"  # Declara ganador al jugador naranja al llegar a la meta.

        pantalla.fill(FONDO)  # Limpia la ventana y dibuja el fondo.
        # Dibuja la línea que divide el campo en dos mitades.
        pygame.draw.line(pantalla, (100, 105, 115), (ANCHO // 2, 0), (ANCHO // 2, ALTO), 2)
        sprites.draw(pantalla)  # Dibuja las paletas y la pelota en sus posiciones actuales.

        # Crea la imagen del marcador con los puntos de los dos jugadores.
        marcador = fuente_marcador.render(
            f"{puntos_izquierda}     {puntos_derecha}", True, BLANCO
        )
        pantalla.blit(marcador, marcador.get_rect(center=(ANCHO // 2, 45)))  # Dibuja el marcador en la parte superior.

        if ganador:
            centrar_texto(pantalla, fuente_mensaje, ganador, BLANCO, ALTO // 2 - 15)  # Muestra quién ganó.
            # Indica que R permite comenzar otra partida.
            centrar_texto(pantalla, fuente_pequena, "Presiona R para jugar de nuevo", BLANCO, ALTO // 2 + 20)
        elif pelota.velocidad_x == 0:
            # Indica que la barra espaciadora inicia el saque.
            centrar_texto(pantalla, fuente_mensaje, "Presiona ESPACIO para sacar", BLANCO, ALTO // 2 + 65)

        # Crea las instrucciones de los controles que aparecen al pie de la ventana.
        instrucciones = fuente_pequena.render(
            "Azul: W/S     Naranja: Flechas     R: reiniciar     ESC: salir",
            True,
            BLANCO,
        )
        # Dibuja las instrucciones centradas en la parte inferior.
        pantalla.blit(instrucciones, instrucciones.get_rect(center=(ANCHO // 2, ALTO - 22)))

        pygame.display.flip()  # Actualiza la ventana para mostrar lo dibujado en este cuadro.
        reloj.tick(FPS)  # Espera lo necesario para mantener la velocidad definida.

    pygame.quit()  # Cierra correctamente los módulos de Pygame.
    sys.exit()  # Finaliza el programa.


if __name__ == "__main__":
    main()  # Ejecuta el juego si este archivo se abre directamente.