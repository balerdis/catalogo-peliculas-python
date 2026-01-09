# Arquitectura de la aplicación

## Visión general

La aplicación implementa una arquitectura en capas inspirada en **Clean Architecture** y **Domain-Driven Design (DDD)**, adaptada al uso de **FastAPI** y **SQLAlchemy**.

El flujo completo de una request sigue el siguiente esquema:

```
Requests (FastAPI Endpoints)
   ↓↑
Pydantic (Validación y serialización)
   ↓↑
Servicios (Lógica de negocio)
   ↓↑
Unit of Work (Control de transacciones)
   ↓↑
Repositories (Acceso a datos)
   ↓↑
SQLAlchemy ORM
   ↓↑
Base de Datos
```

---

## Capas y responsabilidades

### 1. Endpoints (FastAPI)

Responsabilidades:

* Exponer la API HTTP.
* Orquestar dependencias (services).
* Traducir excepciones a respuestas HTTP.

No contienen:

* Lógica de negocio.
* Acceso directo a base de datos.

---

### 2. Pydantic (Schemas / DTOs)

Responsabilidades:

* Validar inputs.
* Serializar outputs.
* Definir contratos de entrada y salida.

Actúan como frontera entre el mundo HTTP y la lógica de negocio.

---

### 3. Servicios (Business Logic)

Responsabilidades:

* Implementar reglas de negocio.
* Coordinar múltiples repositorios.
* Decidir *qué* se hace, no *cómo* se persiste.

Los servicios:

* Abren una Unit of Work.
* Operan sobre entidades del dominio.
* No conocen detalles de SQLAlchemy.

---

### 4. Unit of Work

Responsabilidades:

* Mantener una única sesión de base de datos por request.
* Controlar el ciclo de vida de la transacción.
* Ejecutar `commit` o `rollback` de forma consistente.

Características clave:

* `commit()` ejecuta un `flush` implícito.
* `rollback()` revierte todos los cambios de la sesión.

---

### 5. Repositories

Responsabilidades:

* Encapsular el acceso a datos.
* Traducir operaciones de dominio a consultas ORM.
* Aislar SQLAlchemy del resto de la aplicación.

Decisión de diseño importante:

No existe un método `update()` explícito.

Motivo:

* Las entidades obtenidas mediante `SELECT` quedan automáticamente **attached** a la `Session` de SQLAlchemy.
* SQLAlchemy mantiene un **identity map** y trackea los cambios sobre las entidades attached.
* Al ejecutar el `commit()` de la Unit of Work, SQLAlchemy realiza el `flush` automáticamente.

---

### 6. SQLAlchemy ORM

Responsabilidades:

* Mapear entidades a tablas.
* Gestionar el estado de las entidades (attached / detached).
* Sincronizar cambios mediante `flush` y `commit`.

---

## Flujo de una operación de actualización

Ejemplo conceptual:

1. El endpoint recibe un request HTTP.
2. Pydantic valida el input.
3. El servicio abre una Unit of Work.
4. El repositorio obtiene la entidad (`SELECT`).
5. La entidad queda attached a la sesión.
6. El servicio modifica atributos del objeto.
7. SQLAlchemy marca la entidad como dirty.
8. El `commit()` de la UoW ejecuta el `flush`.
9. Se persisten los cambios en la base de datos.

---

## Beneficios de esta arquitectura

* Separación clara de responsabilidades.
* Transacciones consistentes.
* Código predecible y fácil de testear.
* Menor acoplamiento entre capas.
* Uso correcto del modelo de sesión de SQLAlchemy.

---

## Decisiones explícitas

* No usar `session.commit()` fuera de la Unit of Work.
* No usar `update()` explícito en repositorios.
* Usar soft delete como estrategia de borrado.

---

## Consideraciones futuras

* Introducir repositorios de solo lectura.
* Soportar múltiples Unit of Work (ej. CQRS).
* Mejorar el versionado de esquemas.
