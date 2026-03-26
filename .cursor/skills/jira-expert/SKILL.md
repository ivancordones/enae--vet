---
name: jira-expert
description: Provides Jira usage and SCRUM best practices for writing, enriching, and managing issues, boards, and workflows. Use when the user mentions Jira tickets, SCRUM boards, acceptance criteria, or wants to improve how work is modeled and tracked in Jira.
---

# Jira Expert & SCRUM Best Practices

## When to Use This Skill

Use this skill whenever:
- The user asks how to **crear, enriquecer o mantener tickets** en Jira.
- The user wants to **modelar trabajo** (epics, stories, tasks, subtasks, bugs) o definir **arquitectura de boards**.
- The user needs help con **Acceptance Criteria, DoR, DoD, workflows y transiciones de estado**.
- The user habla de **SCRUM board, sprints, grooming/refinement, planning, review o retro**.
- The task implica **listar, actualizar o comentar issues** usando el MCP de Atlassian desde Cursor.

## Roles y Responsabilidades en Jira

- **Product Owner / Product Manager**:
  - Mantener el **product backlog** priorizado.
  - Asegurar que cada ticket tenga **contexto, objetivo y AC claros**.
  - Alinear tickets con **objetivos de negocio** y roadmap.
- **Equipo de Desarrollo**:
  - Detallar tareas técnicas, estimar, levantar dudas.
  - Actualizar estados y registrar trabajo realizado.
- **Scrum Master**:
  - Garantizar que el flujo en Jira refleje la realidad del equipo.
  - Facilitar ceremonias y eliminar bloqueos.

## Modelado de Trabajo en Jira

### Tipos de Issue Recomendados

- **Epic**: iniciativa grande (varios sprints) que agrupa múltiples tickets.
- **Story** (o **Feature**): valor funcional para el usuario/cliente.
- **Task**: trabajo técnico o de soporte que no es una story (infra, refactor, docs).
- **Sub-task**: parte de una story o task que ayuda a dividir trabajo.
- **Bug**: defecto identificado en producción o entornos previos.

### Buenas Prácticas de Redacción de Tickets

Para cada ticket:
- **Summary (título)**:
  - Claro y accionable. Ejemplos:
    - `Implementar endpoint de login`  
    - `Enriquecer ticket SCRUM-5 con arquitectura y workflow`
- **Description**: usar una estructura consistente, por ejemplo:
  - **Contexto / Problema**
  - **Objetivo**
  - **Alcance (In / Out of scope)**
  - **Solución propuesta / Notas de diseño** (si aplica)
  - **Riesgos / Dependencias**
  - **DOCs / Links relacionados** (Confluence, ADRs, repos, otros tickets)
- **Acceptance Criteria (AC)**:
  - Formato de checklist (`- [ ] ...`).
  - Cada AC debe ser **observable y verificable**.
  - Evitar “genérico” (p. ej. “que sea rápido”) sin métrica o condición concreta.

## SCRUM Board y Flujo de Trabajo

### Columnas / Estados Recomendados

- **Backlog** (opcional en tablero): ideas no refinadas.
- **To Do**: items refinados y listos (cumplen DoR).
- **In Progress**: items en desarrollo.
- **In Review** (o Code Review): PR abiertos, revisión activa.
- **QA / Testing** (si el flujo lo requiere).
- **Done**: criterios de DoD cumplidos; listo en producción o listo para release definido por el equipo.

### Definition of Ready (DoR)

Un ticket está listo para pasar a **To Do** y ser tomado cuando:
- Tiene **contexto y objetivo** claros.
- Incluye **Acceptance Criteria** concretos.
- Las **dependencias** están identificadas (otros tickets, decisiones, diseños).
- Se entiende lo suficiente para poder **estimar** (story points u otra unidad).

### Definition of Done (DoD)

Adaptar a cada equipo, pero típicamente incluye:
- Código **mergeado en la rama principal** (por ejemplo, `main` o `develop`).
- Tests relevantes **añadidos y pasando** (unitarios, integración, e2e según aplique).
- **Validación funcional** hecha (QA/PO cuando corresponde).
- **Documentación actualizada** (README, DOCs, Confluence, esquemas).
- Estado en Jira actualizado a **Done** solo cuando todo lo anterior se cumple.

## Uso Diario de Jira (Buenas Prácticas)

- **Actualizar estados a tiempo real**:
  - Cambiar a **In Progress** al iniciar trabajo.
  - Mover a **In Review** cuando hay PR.
  - Mover a **Done** solo cuando se cumple DoD.
- **Evitar tickets “zombie”**:
  - Revisar en grooming los tickets viejos sin movimiento.
  - Cerrar o reagrupar si ya no aportan valor.
- **Relaciones entre tickets**:
  - Usar enlaces: “is blocked by / blocks”, “relates to”, “duplicates”.
  - Enlazar bugs a las stories/epics relacionadas.
- **Comentarios de calidad**:
  - Explicar decisiones y acuerdos clave.
  - Registrar resultados de investigación (spikes) con conclusiones y siguientes pasos.

## Trabajar con Sprints

- **Sprint Planning**:
  - Seleccionar tickets que cumplen DoR.
  - Alinear con capacidad del equipo y objetivos del sprint.
  - Dividir stories grandes en tasks/subtasks si es necesario.
- **Daily**:
  - Revisar el tablero; cada miembro habla de:
    - Qué hizo ayer (en relación a tickets).
    - Qué hará hoy.
    - Bloqueos.
- **Review & Retro**:
  - En Review: mostrar trabajo completado en Jira (filtro por sprint y estado Done).
  - En Retro: usar métricas (burndown, lead time, throughput) y feedback cualitativo para ajustar procesos y configuración del tablero.

## Acceptance Criteria: Plantillas Útiles

### Plantilla General

Usar cuando se definen AC para cualquier ticket:

```markdown
### Acceptance Criteria

- [ ] El comportamiento está claramente descrito para casos principales.
- [ ] Se han cubierto los casos de error / edge cases relevantes.
- [ ] Existen pruebas (manuales o automatizadas) que permiten verificar cada AC.
- [ ] La documentación y enlaces en el ticket están actualizados.
```

### Plantilla para Tickets de Documentación (como SCRUM-5)

```markdown
### Acceptance Criteria (Doc tickets)

- [ ] El ticket incluye secciones de contexto, arquitectura y alcance.
- [ ] Están documentadas las tecnologías involucradas y su propósito.
- [ ] Hay un índice/glosario de documentos relacionados (en Jira o en el repo).
- [ ] El flujo de trabajo (estados Jira y proceso SCRUM) está descrito.
- [ ] Se explicita el out-of-scope para evitar malentendidos.
```

## Uso del MCP de Atlassian desde Cursor

Cuando estés en Cursor y necesites **leer o editar issues de Jira**:

- **Lectura de tickets**:
  - Usa la herramienta `getJiraIssue` del MCP Atlassian con:
    - `cloudId`: el de tu instancia (por ejemplo, el obtenido por `getAccessibleAtlassianResources`).
    - `issueIdOrKey`: por ejemplo, `SCRUM-5`.
- **Búsqueda de issues**:
  - Usa `searchJiraIssuesUsingJql` con:
    - `cloudId`.
    - `jql`: e.g., `project = SCRUM ORDER BY updated DESC`.
- **Edición de tickets**:
  - Usa `editJiraIssue` para actualizar `description`, `summary` u otros campos.
  - Mantén una estructura consistente (secciones + AC) al editar descripciones.

## Cómo Aplicar Esta Skill en la Práctica

Cuando uses esta skill:
- **Primero**, lee bien el ticket y su contexto (incluyendo links y comentarios).
- **Después**, aplica las secciones de este documento:
  - Mejora título, descripción y AC siguiendo las plantillas.
  - Verifica que el tipo de issue y sus enlaces son adecuados.
  - Asegura que el estado y la pertenencia a sprint/epic tienen sentido.
- **Finalmente**, resume para el usuario:
  - Qué cambios se han sugerido o aplicado.
  - Cómo eso mejora la claridad, el seguimiento y el alineamiento con SCRUM.

