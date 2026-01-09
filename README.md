# Proyecto API – README

## Descripción general

Este proyecto implementa una API REST construida con **FastAPI**, utilizando **SQLAlchemy** como ORM y siguiendo una arquitectura en capas con el patrón **Unit of Work (UoW)** para el manejo transaccional.

El objetivo principal de la arquitectura es:

* Separar claramente responsabilidades.
* Mantener la lógica de negocio independiente de la infraestructura.
* Garantizar consistencia transaccional.
* Facilitar el mantenimiento, testeo y evolución del sistema.

---

## Stack tecnológico

* **Python 3.x**
* **FastAPI** – Framework web
* **Pydantic** – Validación de datos (input / output)
* **SQLAlchemy ORM** – Persistencia
* **MySQL / PostgreSQL** (agnóstico a motor)

---

## Arquitectura

La arquitectura del sistema está documentada en detalle en el archivo **ARCHITECTURE.md**.

En términos generales, la aplicación sigue un modelo de capas bien definido:

```
Requests (FastAPI Endpoints)
   ↓↑
Pydantic (Schemas / DTOs)
   ↓↑
Servicios (Lógica de negocio)
   ↓↑
Unit of Work (Control transaccional)
   ↓↑
Repositories
   ↓↑
SQLAlchemy ORM
   ↓↑
Base de Datos
```

---

## Principios clave

* **Una request = una Unit of Work**
* **Una sesión de base de datos por UoW**
* **No hay lógica de negocio en los endpoints**
* **No hay SQL ni ORM en los servicios**
* **Los repositorios encapsulan el acceso a datos**

---

## Estructura del proyecto (simplificada)

```
app/
├── api/
│   └── v1/
│       ├── endpoints/
│       └── schemas/
├── core/
│   ├── services/
│   ├── unit_of_work/
│   └── database/
│       ├── models/
│       └── repositories/
└── scripts/
```

---

## Notas finales

Este README describe el *qué* del proyecto. Para entender el *cómo* y el *por qué* de las decisiones arquitectónicas, consultar **ARCHITECTURE.md**.
