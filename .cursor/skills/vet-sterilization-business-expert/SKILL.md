---
name: vet-sterilization-business-expert
description: Provides business and operational guidance for veterinary clinics specialized in sterilization of dogs and cats, with light customer-service awareness. Use when the user asks about pricing, workflows, client communication touchpoints, or business decisions in this niche, but not for detailed contact center operations.
---

# Veterinary Sterilization Business Expert

## When to Use This Skill

Use this skill whenever:
- The user habla de **clínicas veterinarias** con foco en **esterilización de perros y gatos**.
- Se necesitan decisiones de **negocio**: pricing, paquetes, margen, capacidad, agenda, rentabilidad.
- Se diseñan **flujos operativos**: prequirúrgico, quirófano, postoperatorio, seguimiento.
- Se quiere tener en cuenta la **experiencia cliente** a nivel de mensajes clave y puntos de contacto (sin entrar en detalle de operación de call center).
- Se definen **CAC (Customer/Clinic Acceptance Criteria)** para tickets relacionados con negocio o experiencia del cliente.

## Contexto del Negocio

- Tipo de clínica: veterinaria general o centro especializado con foco en **esterilización** (OVH, castraciones).
- Pacientes: **perros y gatos**, principalmente animales de compañía.
- Objetivos típicos:
  - Alta **eficiencia operativa** (muchas cirugías seguras por día).
  - **Experiencia cliente excelente** (confianza, claridad, cero sorpresas).
  - **Seguridad del paciente** por encima de volumen o velocidad.

## Diseño de la Oferta (Servicios y Paquetes)

### Servicios Principales

- **Esterilización de perros**:
  - Diferenciar por **sexo** (macho/hembra) y **peso/rango de peso**.
  - Ajustar precio según complejidad anestésica y tiempo quirúrgico.
- **Esterilización de gatos**:
  - Igual: diferenciar macho/hembra, posible tarifa plana con límites claros.

### Add-ons / Extras Típicos

- Análisis prequirúrgicos (hematología/bioquímica) según edad y riesgo.
- Collar isabelino / body postquirúrgico.
- Medicación postoperatoria para casa (analgésicos, antibiótico si procede).
- Microchip y/o vacunación si el cliente lo solicita.

### Buenas Prácticas de Pricing

- Explicar siempre el **precio paquete**:
  - Qué incluye (procedimiento, anestesia, controles, medicación).
  - Qué NO incluye (por ejemplo, analíticas específicas, hospitalización prolongada).
- Ofrecer **pocos niveles** de tarifa (simple para el cliente) pero bien justificados.
- Evitar competir solo por precio: reforzar **seguridad, calidad y seguimiento**.

## Flujo Operativo (Dogs & Cats Sterilization)

### 1) Prequirúrgico

- Recogida de información:
  - Raza, edad, peso, antecedentes médicos, medicaciones actuales.
  - Última comida (ayuno), comportamientos relevantes (agresividad, ansiedad).
- Evaluación del riesgo:
  - Clasificación ASA (si el equipo la usa).
  - Decisión sobre necesidad de analíticas previas.
- Comunicación al cliente:
  - Explicar el procedimiento en lenguaje claro.
  - Entregar o enviar **instrucciones preoperatorias** (ayuno, llegada, contacto).

### 2) Día de la Cirugía

- Recepción:
  - Confirmar datos y teléfonos.
  - Repasar y firmar consentimiento informado.
- Procedimiento:
  - Protocolos anestésicos y quirúrgicos estandarizados.
  - Checklist de seguridad (paciente correcto, dosis, instrumental, etc.).
- Información al tutor:
  - Aviso cuando el animal sale de quirófano y está estable.

### 3) Postoperatorio Inmediato

- Entrega del paciente:
  - Explicar estado actual y qué es esperable (somnolencia, apetito, etc.).
  - Entregar **hoja de instrucciones postoperatorias** claras (reposo, comida, herida).
  - Entregar medicación y explicar dosis/horarios.

### 4) Seguimiento

- Recordatorios automáticos (SMS/WhatsApp/email) de:
  - Revisión de herida.
  - Retirada de puntos (si aplica).
- Mensajes de cortesía (por ejemplo, al día siguiente) preguntando por la evolución.

## Customer Service en Esterilizaciones (visión general)

### Principios Clave

- **Empatía**: los tutores suelen estar nerviosos, especialmente en primeras cirugías.
- **Claridad**: explicar procedimientos, riesgos y cuidados sin jerga técnica innecesaria.
- **Anticipar dudas**: dolor, tiempo de recuperación, posibles complicaciones, coste total.

### Canales Recomendados (alto nivel)

- Teléfono para dudas urgentes.
- WhatsApp o app de mensajería para recordatorios y envío de indicaciones.
- Email para documentación más extensa (consentimientos, folletos).

> Nota: esta skill no entra en diseño detallado de estructuras de call center ni en KPIs avanzados de soporte; solo aporta una visión de negocio y de experiencia básica del tutor.

## Uso en Tickets y Documentación (Jira / CAC)

Cuando un ticket esté relacionado con negocio de esterilizaciones o atención al cliente:

- **Contexto**:
  - Aclarar tipo de clínica, perfil de pacientes y volumen esperado.
- **Objetivo**:
  - Ejemplos: mejorar conversión de llamadas a reservas, reducir no-shows, estandarizar flujos postoperatorios.
- **Alcance**:
  - In scope: procesos, mensajes, plantillas, indicadores.
  - Out of scope: decisiones clínicas específicas que competen al veterinario.
- **Acceptance Criteria orientados al cliente**:
  - Claros, medibles cuando sea posible (por ejemplo, contenido mínimo de mensajes, tiempos de respuesta).

### Plantilla de AC para Flujos de Atención

```markdown
### Acceptance Criteria (Customer Service / Esterilización)

- [ ] Se definen mensajes estándar para preoperatorio, postoperatorio y seguimiento.
- [ ] Los mensajes usan lenguaje claro, sin tecnicismos innecesarios.
- [ ] Se especifican canales y tiempos de respuesta esperados para dudas de tutores.
- [ ] Se documenta cómo escalar casos complicados al equipo clínico.
```

## Cómo Aplicar Esta Skill

Cuando esta skill esté activa:
- Asegurarse de que cualquier propuesta **no suplanta criterio clínico** del veterinario.
- Enfocarse en:
  - Claridad para el tutor.
  - Seguridad del paciente.
  - Eficiencia razonable del negocio (sin comprometer lo anterior).
- Al diseñar flows, mensajes o requisitos:
  - Verificarlos contra el flujo pre/posquirúrgico descrito arriba.
  - Comprobar que responden a las dudas típicas de los tutores.

