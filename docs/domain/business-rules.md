# Reglas de negocio operativas — esterilización y agenda (Tetris)

Políticas explícitas del caso clínica / chatbot de reservas, alineadas con el Event Storming y el límite de **240 minutos** de quirófano por día (ver también reglas de agenda del repositorio).

Ticket: [SCRUM-14](https://ivancordonesnunez.atlassian.net/browse/SCRUM-14) (VET-14).

## 1. Alcance

Estas reglas describen el **comportamiento esperado del sistema de reserva** (mock o real), no sustituyen protocolos clínicos aprobados por un veterinario responsable.

## 2. Identificación y derivación

| ID | Regla |
| :--- | :--- |
| BR-01 | Si el tutor indica **más de una mascota** en el mismo flujo de reserva, **derivar a llamada telefónica** (o canal humano). |
| BR-02 | Para una sola mascota, recoger como mínimo: **especie**, **sexo**, **peso** (perros; gatos según política de la clínica). |

## 3. Especie y celo

| ID | Regla |
| :--- | :--- |
| BR-10 | **Gato**: recoger información de celo/estado reproductivo según guión; calcular tiempo de bloque de quirófano según tabla de duraciones. |
| BR-11 | **Perro en celo**: **no** reservar; indicar espera (p. ej. **2 meses**) y fin del flujo automático. |
| BR-12 | **Perro sin celo**: continuar al cálculo de duración. |

## 4. Duraciones de bloque (quirófano) — referencia del flujo

Valores usados en el modelo Event Storming (ajustables por ticket futuro):

| Contexto | Duración de bloque |
| :--- | :--- |
| Gato macho | 12 min |
| Gata hembra | 15 min |
| Perro macho | 30 min |
| Perra hembra | 45–70 min según **peso** (desglose fino en implementación / datos) |

## 5. Agenda tipo “Tetris”

| ID | Regla |
| :--- | :--- |
| BR-20 | **Límite diario de quirófano:** la suma de minutos reservados en un día **no supera 240 minutos** (4 h). |
| BR-21 | **Límite de perros por día:** si el candidato es **perro**, el total de perros ese día **no supera 2** (regla del diagrama; revisar con negocio real). |
| BR-22 | Si no hay hueco, **probar el día siguiente** (búsqueda iterativa). |

> **Nota:** El máximo de **240 minutos** por cita individual en otros contextos del repo (p. ej. citas genéricas) es una restricción distinta: aquí 240 min es **capacidad diaria agregada** de quirófano en el modelo pedagógico.

## 6. Confirmación y entrega

| ID | Regla |
| :--- | :--- |
| BR-30 | Tras elegir fecha: preguntar **extras** (p. ej. microchip, rabia) y registrar decisión. |
| BR-31 | **Ventana de entrega** sugerida: gato **08:00–09:00**; perro **09:00–10:30** (valores del diagrama; parametrizables). |
| BR-32 | Tras confirmar cita: enviar **instrucciones de ayuno** y **formulario de consentimiento** (canal acordado: email, WhatsApp, etc.). |

## 7. Enlaces

- [Glosario y reglas preparatorias](glossary-and-preparation.md)
- [Event Storming (Mermaid)](event-storming-sterilization-booking.md)
- Lógica de agenda relacionada en el repo: `.cursor/docs/reglas-negocio-logica-agenda.md` (si existe en tu clon).
