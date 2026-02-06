# EduOdoo - Gestión de Academia de Cursos 📚

¡Hola! Este es **EduOdoo**, un módulo que desarrollé para Odoo 19 como parte de mi proyecto del DAM. La idea es simple: gestionar una academia de cursos de forma sencilla y eficiente.

## ¿Qué hace este módulo?

Básicamente te permite llevar el control de:

- **Cursos**: Crear cursos con diferentes niveles (A1 a C2), precios y asignar profesores
- **Sesiones**: Programar sesiones de cada curso con fecha, hora y control de asientos
- **Alumnos**: Registrar alumnos y ver en qué clases están matriculados
- **Profesores**: Gestionar el equipo docente
- **Matrículas**: Sistema de inscripción con flujo de estados (Borrador → Confirmada → Pagada)
- **Facturación**: Control básico de pagos

## Lo interesante (Semana 2-6 Febrero)

Esta semana me centré en la programación de Odoo, implementando:

### Campos Computados (@api.depends)

- **Porcentaje de ocupación**: La sesión calcula automáticamente cuántos asientos están ocupados
- **Barra de progreso**: Se ve visualmente el % de ocupación en la lista
- **Colores dinámicos**: Verde si hay sitio, rojo si está llena

### Validaciones (@api.constrains)

- **Límite de asientos**: No deja inscribir más alumnos de los que caben
- **Profesor ocupado**: Si un profe ya tiene sesión a esa hora, salta error

### Flujo de estados

Las matrículas pasan por: `Borrador → Confirmada → Pagada`

Con botones para ir avanzando y todo el control de fechas.

## Cómo probarlo

1. Clona el repo en la carpeta `addons` o `modules` de tu Odoo
2. Actualiza la lista de módulos
3. Instala "EduOdoo - Academia de Cursos"
4. Ve al menú EduOdoo y ¡a jugar!

```bash
python odoo-bin -d tu_base -u edu_odoo --addons-path=odoo/addons,addons,modules
```

## Estructura del módulo

```
edu_odoo/
├── models/
│   ├── alumno.py      # Modelo de alumnos
│   ├── clase.py       # Grupos y horarios
│   ├── curso.py       # Cursos disponibles
│   ├── facturacion.py # Pagos y facturas
│   ├── matricula.py   # Inscripciones con estados
│   ├── profesor.py    # Profesores
│   └── sesion.py      # Sesiones con ocupación
├── security/
│   └── ir.model.access.csv
├── views/
│   └── views.xml      # Todas las vistas
└── __manifest__.py
```

## Requisitos

- Odoo 19
- PostgreSQL
- Python 3.11+

## Autor

Adrián - Proyecto DAM @ ILERNA

---

*Si encuentras algún bug o tienes sugerencias, ¡dímelo! Esto es un proyecto de aprendizaje y cualquier feedback es bienvenido.* 🚀
