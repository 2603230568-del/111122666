# Pong Retro Arcade - Proyecto Integrador

**Estudiante:** Ivan Gil  
**Materia:** Logíca de programación 
**Nivel:** 1er Cuatrimestre  

## Objetivo General
Desarrollar un prototipo funcional del juego Pong en 2D con Python y Pygame aplicando POO, manejo de eventos en tiempo real, colisiones y sincronizacion a 60 FPS.

## Investigacion sobre Pygame

### 1. ¿Que es Pygame y para que se utiliza?
Pygame es un conjunto de modulos libres para Python orientados al desarrollo de videojuegos 2D. Funciona como un envoltorio (wrapper) de la biblioteca SDL (Simple DirectMedia Layer) escrita en C, facilitando el acceso al hardware grafico, teclado, raton y audio. Se utiliza en el ambito educativo para ensenar arquitectura de software y logica de juegos sin la complejidad del bajo nivel de C.

### 2. ¿Como se relaciona Pygame con los temas vistos en clase?
- **Ciclos (Loops):** Opera bajo el patron Game Loop (un bucle while infinito) que ejecuta secuencialmente: eventos, logica/fisicas, dibujado y actualizacion de pantalla.
- **Manejo de Eventos:** Emplea una cola de eventos (pygame.event.get()) para capturar teclas, clics o cierre de ventana y evaluarlos mediante condicionales.
- **Estructuras de Datos:** Utiliza tuplas para coordenadas y colores RGB, y listas o grupos dinamicos (pygame.sprite.Group) para iterar entidades.
- **Funciones y Modularidad:** Desacopla la logica de inicializacion, calculo de rebotes y renderizado en funciones reutilizables.
- **Programacion Orientada a Objetos (POO):** Mediante pygame.sprite.Sprite, las entidades heredan propiedades visuales (image) y geometricas (rect).

### 3. ¿Que significa que Pygame permite "tomar mucho o poco" de la libreria?
Pygame no impone una estructura rigida. Un programador puede "tomar poco" usandola unicamente para abrir una ventana y dibujar pixeles (escribiendo su propio motor de fisicas y colisiones desde cero), o "tomar mucho" aprovechando sus sistemas auxiliares de sprites, audio multicanal, fuentes tipograficas y colisiones matriciales.
