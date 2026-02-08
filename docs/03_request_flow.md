# Request Flow Diagram

This document explains how an HTTP request flows through the Coffee Shop Django application, from the user’s browser to the database and back.  
The goal is to clearly show responsibilities of each layer and keep the architecture scalable, testable, and easy to reason about.

---

## High-Level Request Flow (Django Web App)

```mermaid
flowchart TD
    A[User / Browser] -->|HTTP Request| B[URL Router urls.py]
    B --> C[View Function / Class-Based View]
    C -->|Business Logic| D[Service Layer]
    D -->|ORM Queries| E[(Database)]
    E --> D
    D --> C
    C -->|Context Data| F[Template Engine]
    F -->|HTML Response| A
```

