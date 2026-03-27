# Glosario y reglas preparatorias — clínica veterinaria (esterilización)

Documento de dominio para el caso **clínica veterinaria / chatbot de reserva de esterilización**.  
Relacionado con el ticket [SCRUM-14](https://ivancordonesnunez.atlassian.net/browse/SCRUM-14) (VET-14).

## Objetivo

Unificar términos, actores y condiciones previas que el sistema (o el asistente) debe conocer antes de proponer citas o dar información operativa.

## Actores

| Término | Descripción |
| :--- | :--- |
| **Tutor** | Persona que gestiona la mascota y solicita la cita. |
| **Mascota** | Perro o gato sometido a esterilización en este caso de uso. |
| **Clínica / recepción** | Personal que confirma datos, documentación y ventanas de entrega. |
| **Quirófano / agenda** | Recurso limitado en tiempo total diario y reglas de encaje (“Tetris”). |

## Glosario

| Término | Significado |
| :--- | :--- |
| **Esterilización** | Procedimiento quirúrgico programado (castración / OVH según sexo y especie). |
| **Celo (heat)** | Estado fisiológico; puede **contraindicar** o posponer la cirugía según política. |
| **Ayuno (fasting)** | Restricción de alimentación previa al procedimiento; se comunica tras confirmar cita. |
| **Ventana de entrega** | Franja horaria asignada para ingreso del paciente el día de la cirugía. |
| **Session / intent** | En el flujo conversacional: identificación del usuario y de la intención (reservar, informar, etc.). |
| **Tetris (agenda)** | Lógica de encaje de huecos respetando duración por tipo de paciente y **límite diario de minutos de quirófano** (ver [business-rules.md](business-rules.md)). |
| **Microchip / rabia** | Extras opcionales que se registran tras elegir fecha y antes de la confirmación final. |

## Reglas preparatorias (alto nivel)

1. **Identificación**: confirmar quién habla y qué quiere hacer (p. ej. nueva reserva vs consulta genérica).
2. **Mascotas múltiples**: si el tutor tiene **más de una mascota** en el mismo flujo, derivar a **llamada telefónica** o canal humano (evitar errores de datos).
3. **Datos mínimos de la mascota**: especie, sexo, peso (perros); información de celo cuando aplique.
4. **Seguridad clínica**: no sustituir juicio veterinario; las políticas de celo/peso son **reglas de negocio operativas** documentadas aparte.
5. **Consentimiento e instrucciones**: tras reservar, enviar ayuno y formulario de consentimiento según flujo acordado con la clínica.

## Enlaces

- [Event Storming — reserva de esterilización](event-storming-sterilization-booking.md)
- [Reglas de negocio operativas](business-rules.md)
