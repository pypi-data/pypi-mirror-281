# Hack4u Academy Library
 Una biblioteca Python pra consultar cursos de la academia Hack4u
 
 ## Cursos dispobibles:

- Introduccion a Linux [15 horas]
- Personalización de Linux[3 horas]
- Introduccion al Hacking[53 horas]

## Instalación

Instala el paquete usando `pip3`:

### Listar todos los cursos

```python
from hack4u import list_courses
for course in list_courses():
    print(course)
```

#### Obtener un curso por nombre

```python
from hack4u import search_by_name
course = search_by_name("Introduccion al Hacking"):
print(course)
```

#### calcular duracion total de los cursos

```python
from hack4u.utils import total_duration
print(f"Duracion total: {total_duration()} horas")
```