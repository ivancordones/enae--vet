---
title: Reglas de Negocio y Lógica de Agenda
source: Reglas de Negocio y Lógica de Agenda (PDF)
---

## 1. Definición de Capacidad Operativa ("La Cuota")

El sistema gestiona la agenda con un **modelo de inventario de minutos**, no por franjas horarias fijas.

- **Días operativos**: Lunes a jueves.  
  - Viernes, sábado y domingo están bloqueados por defecto para cirugía, salvo indicación contraria.
- **Ventana quirúrgica**: 09:00 a 13:00.
- **Capacidad diaria máxima**: 240 minutos disponibles por día.
- **Lógica de ocupación**:
  - Cada cita resta minutos de esta capacidad total según la **tabla de servicios** (sección 2).

El sistema debe respetar estos límites al confirmar cualquier cita.

## 2. Tabla Maestra de Servicios y Tiempos

El Agente de IA clasifica la petición del cliente y asigna una duración (coste en tiempo) según especie y tipo de servicio.  
Estos minutos se descuentan de la cuota diaria de 240 minutos.

### 2.1. Especie: GATO

- **Límite**: Sin límite de cantidad de gatos; solo aplica el límite de tiempo total.
- **Servicios y tiempos**:
  - Esterilización gato macho: **12 minutos**
  - Esterilización gata hembra: **15 minutos**
- Puede marcarse internamente una alerta de "Gato callejero" cuando proceda, **sin modificar el tiempo asignado**.

### 2.2. Especie: PERRO

- **Límite**: Sujeto a **restricción de cantidad diaria** (ver sección 3).
- El tiempo se determina por sexo y peso:
  - Perro macho (cualquier peso): **30 minutos**
  - Perra 0–10 kg: **45 minutos**
  - Perra 10–20 kg: **50 minutos**
  - Perra 20–30 kg: **60 minutos**
  - Perra 30–40 kg: **60 minutos**
  - Perra >40 kg: **70 minutos**

## 3. Algoritmo de Restricción y Bloqueo ("El Tetris")

Para confirmar una fecha, el sistema debe validar **ambas** condiciones siguientes:

### Regla 1: Validación de tiempo (suma ≤ 240)

\[
\text{Minutos ya ocupados} + \text{Minutos de la nueva cita} \le 240
\]

Si la suma supera los 240 minutos, la fecha se marca como **NO DISPONIBLE**.

### Regla 2: Límite de perros (máximo 2 por día)

Si la nueva cita es de especie PERRO:

\[
\text{Número de perros del día} + 1 \le 2
\]

- Si ya hay **2 perros** programados en un día, el sistema **bloquea** ese día para nuevas citas de perro, aunque queden minutos libres.
- Esta regla **no aplica a gatos**:
  - Un día con 2 perros puede seguir aceptando gatos hasta completar los 240 minutos.

## 4. Ventanas de Entrega por Especie (Obligatorias)

Las horas de entrega dependen de la especie y son **estrictas**.  
El sistema solo ofrecerá y confirmará citas cuya **hora de entrega** caiga dentro de estas ventanas.

### 4.1. Gatos

- **Ventana de entrega**: 08:00–09:00 (estricto)
- **Días aplicables**: Lunes a viernes.
- Reglas:
  - Ningún gato puede ser entregado fuera de 08:00–09:00.
  - En días operativos (lunes–jueves) se usa 08:00–09:00.
  - El viernes (si se habilita para gatos) se mantiene la misma ventana 08:00–09:00.

### 4.2. Perros

- **Ventana de entrega**: 09:00–10:30 (estricto)
- **Días aplicables**: Días operativos (lunes a jueves).
- Reglas:
  - Ningún perro puede ser entregado fuera de 09:00–10:30.

### 4.3. Resumen de ventanas

- **Gatos**: entrega 08:00–09:00, lunes–viernes.  
- **Perros**: entrega 09:00–10:30, lunes–jueves (días operativos).

## 5. Protocolo de Comunicación y Logística

El sistema debe gestionar las expectativas del cliente distinguiendo claramente entre:

- **Reserva**: Día de la cirugía.
- **Entrega**: Ventana horaria en la que el cliente debe traer al animal.

### 5.1. Ocultar horarios quirúrgicos

- El cliente **no** elige una hora concreta (p. ej. 10:30).  
- El cliente solo elige el **DÍA** de la cita.  
- Los horarios quirúrgicos internos se mantienen ocultos para simplificar la experiencia y mantener flexibilidad interna.

### 5.2. Mensaje de entrega por especie

Al confirmar la cita, el sistema informa automáticamente al cliente:

- **Gatos**:  
  > "El gato debe ser entregado estrictamente entre las 08:00 y las 09:00 de la mañana."

- **Perros**:  
  > "El perro debe ser entregado estrictamente entre las 09:00 y las 10:30 de la mañana para su preparación."

### 5.3. Protocolo de ayuno

- Las instrucciones de ayuno (desde medianoche de la noche anterior) se **adjuntan al mensaje final de confirmación**.
- El sistema debe incluir este texto de forma consistente en todas las confirmaciones de cirugía.

