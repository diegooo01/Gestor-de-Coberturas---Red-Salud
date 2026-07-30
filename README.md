# Gestor de Coberturas

Aplicación para consultar pólizas de salud y registrar el consumo de sus coberturas. Un operador inicia sesión, busca una póliza por su número y puede ver al asegurado, el plan asociado y las coberturas disponibles con su saldo de usos, además de registrar consumos respetando las reglas del negocio.

El proyecto es un monorepo: el backend (API REST en Django) y el frontend (Angular) viven en la misma raíz, en las carpetas `backend/` y `frontend/`.

## Stack

**Backend**
- Python 3.12
- Django 6 + Django REST Framework
- MySQL 8 (driver PyMySQL)
- Autenticación JWT con `djangorestframework-simplejwt`
- Documentación de la API con Swagger (`drf-spectacular`)

**Frontend**
- Angular 22 (componentes standalone)
- TypeScript
- Node 22

**Infraestructura**
- Docker / Docker Compose

## Cómo levantarlo

### Con Docker (recomendado)

Es la forma más simple; solo necesitas Docker instalado. Desde la raíz del proyecto:

```bash
docker compose up --build
```

Esto levanta tres contenedores: la base de datos MySQL, el backend y el frontend. El backend, al arrancar, corre las migraciones y carga los datos de prueba solo, así que no hace falta nada más.

Cuando termine de compilar (la primera vez tarda un poco):

- Frontend: http://localhost:4200
- API: http://localhost:8000/api
- Swagger: http://localhost:8000/api/docs/

### Manual (sin Docker)

Requiere Python 3.12+, Node 22+ y una instancia de MySQL corriendo.

**Backend**

```bash
cd backend
python -m venv venv
# Windows: venv\Scripts\activate   |   Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # ajusta las credenciales de la BD si hace falta
python manage.py migrate
python manage.py seed
python manage.py runserver
```

**Frontend** (en otra terminal)

```bash
cd frontend
npm install
npm start
```

## Usuario y datos de prueba

El comando `seed` deja la base lista para probar de una. Además de los datos de negocio, crea un usuario para iniciar sesión:

- **Usuario:** `admin`
- **Contraseña:** `admin123`

El seed es reproducible: se puede correr las veces que sea y siempre deja el mismo estado (limpia todo y vuelve a cargar), por lo que no genera duplicados. Entre los datos que carga hay pólizas pensadas para probar distintos escenarios:

| Póliza | Situación |
|--------|-----------|
| `POL-2025-0001` | Vigente, Plan Salud Total (la principal para probar) |
| `POL-2025-0002` | Vigente, Plan Premium (más coberturas) |
| `POL-2025-0003` | Vigente, Plan Básico |
| `POL-2024-0009` | Vencida (la fecha de fin ya pasó) |
| `POL-2025-0004` | Suspendida |

Las dos últimas sirven para verificar que el registro de consumo se bloquea cuando la póliza no está vigente o no está activa.

## API

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/api/token/` | Login. Devuelve el token de acceso y el de refresco |
| `GET` | `/api/polizas/{numero}/` | Consulta una póliza con su asegurado, plan, estado y vigencia |
| `GET` | `/api/polizas/{numero}/coberturas/` | Lista las coberturas del plan con límite, consumos y saldo |
| `POST` | `/api/polizas/{numero}/consumos/` | Registra un consumo validando las reglas de negocio |

Los endpoints de negocio requieren token. La documentación completa está en Swagger (`/api/docs/`), donde se puede probar cada uno usando el botón *Authorize* con el token obtenido en `/api/token/`.

## Decisiones técnicas

El modelo tiene seis entidades: `Asegurado`, `Plan`, `Cobertura`, `PlanCobertura` (la tabla intermedia), `Poliza` y `Consumo`. Anoto acá las decisiones que me parecieron menos evidentes.

**El límite de usos vive en la relación plan–cobertura, no en la cobertura.** Es la decisión central del modelo. Una misma cobertura puede tener un límite distinto según el plan: "Consulta médica" permite 10 usos en el Plan Total, 4 en el Básico y 20 en el Premium. Si el límite estuviera en la cobertura, quedaría amarrado de forma global y no se podría diferenciar por plan. Por eso el `limite_usos` está en `PlanCobertura`, que une un plan con una cobertura.

**La vigencia se calcula, no se guarda.** No es un campo de la tabla sino una propiedad (`esta_vigente`) que combina dos condiciones: que el estado sea ACTIVA y que la fecha de hoy caiga dentro del rango inicio–fin. La puse en el modelo y no en la vista porque es una regla del negocio que se reutiliza tanto al consultar la póliza como al registrar un consumo.

**La póliza maneja tres estados: ACTIVA, SUSPENDIDA e INACTIVA.** Para la vigencia solo importa si está ACTIVA, pero separé los otros dos porque tienen significados distintos: SUSPENDIDA es una pausa recuperable (por ejemplo, por falta de pago) e INACTIVA es una baja definitiva. Modelarlos aparte refleja mejor el dominio, aunque hoy ambos impidan consumir por igual.

**Las validaciones del consumo están en la vista.** Las cuatro reglas del registro (que la póliza exista, esté vigente, que la cobertura pertenezca al plan y que no se supere el límite) se resuelven en la vista antes de crear el consumo. Para el tamaño de esta prueba me pareció suficiente; en un proyecto más grande las movería a una capa de servicios para dejar la vista más delgada.

**El acceso es por token JWT.** Reutilicé el modelo de usuario que ya trae Django en vez de crear uno propio, porque quien inicia sesión es el operador del sistema, no el asegurado (el asegurado es un dato que se consulta, no alguien que entra a la app). En el frontend el token se guarda en `localStorage` y un interceptor lo adjunta automáticamente en cada petición, y un guard protege la ruta de consulta para que no se pueda entrar sin sesión.

**El frontend está organizado por tipo de archivo** (servicios, componentes, guards, interceptors) porque el proyecto es chico. En algo más grande convendría organizarlo por features.

## Supuestos

- Los términos "póliza" y "certificado" se tratan como equivalentes, tal como indica el enunciado.
- Cada registro de consumo cuenta como un uso; el saldo disponible es el límite menos la cantidad de consumos registrados para esa póliza y cobertura.
- El diseño visual se mantuvo mínimo a propósito, ya que la prueba indica que no se evalúa. El foco está en la funcionalidad y la organización del código.
- Los operadores del sistema se crean por administración (el seed o `createsuperuser`); no hay auto-registro porque no corresponde al caso de negocio.