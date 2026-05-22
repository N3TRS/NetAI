# 🤖 NetAI — Microservicio de Análisis de Código con IA

<div align="center">

### 🛠️ Stack Tecnológico

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.135.3-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-LLaMA_3.3_70B-F55036?style=for-the-badge&logo=groq&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1.2.15-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)

### ☁️ Infraestructura & Calidad

![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-CI/CD-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)
![SonarQube](https://img.shields.io/badge/SonarQube-Quality-4E9BCD?style=for-the-badge&logo=sonarqube&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-Metrics-E6522C?style=for-the-badge&logo=prometheus&logoColor=white)
![Azure](https://img.shields.io/badge/Azure-App_Service-0078D4?style=for-the-badge&logo=microsoftazure&logoColor=white)

### 🏗️ Arquitectura

![Layered](https://img.shields.io/badge/Architecture-Layered_Modular-blueviolet?style=for-the-badge)
![MCP](https://img.shields.io/badge/MCP-Model_Context_Protocol-6DB33F?style=for-the-badge)
![REST API](https://img.shields.io/badge/REST-API-009688?style=for-the-badge)

</div>

---

## 📑 Tabla de Contenidos

1. [👤 Integrantes](#1--integrantes)
2. [🎯 Objetivo del Microservicio](#2--objetivo-del-microservicio)
3. [⚡ Funcionalidades Principales](#3--funcionalidades-principales)
4. [📋 Estrategia de Versionamiento y Branches](#4--estrategia-de-versionamiento-y-branches)
5. [⚙️ Tecnologías Utilizadas](#5-️-tecnologías-utilizadas)
6. [🧩 Funcionalidad y Endpoints](#6--funcionalidad-y-endpoints)
7. [🏛️ Arquitectura, Patrones y Módulos](#7-️-arquitectura-patrones-y-módulos)
8. [⚠️ Manejo de Errores](#8-️-manejo-de-errores)
9. [🧪 Evidencia de Pruebas y Cobertura](#9--evidencia-de-pruebas-y-cobertura)
10. [🗂️ Organización del Código](#10-️-organización-del-código)
11. [🔗 Conexiones con Servicios Externos](#11--conexiones-con-servicios-externos)
12. [🚀 Ejecución del Proyecto](#12--ejecución-del-proyecto)
13. [⚙️ Pipelines CI/CD](#13-️-pipelines-cicd)
14. [☁️ Despliegue en Azure](#14-️-despliegue-en-azure)
15. [🤝 Integrantes y Contribuciones](#15--integrantes-y-contribuciones)

---

## 1. 👤 Integrantes

- Tulio Riaño Sánchez
- Julian Camilo Lopez Barrero
- Juan Sebastián Puentes Julio
- David Alejandro Patacon Henao

---

## 2. 🎯 Objetivo del Microservicio

**NetAI** es un microservicio de análisis inteligente de código fuente. Recibe fragmentos de código (TypeScript, Python o Java) junto con una pregunta del desarrollador y retorna un análisis conversacional generado por un modelo LLM (LLaMA 3.3 70B vía Groq). Además, expone un endpoint de generación colaborativa de diagramas usando el protocolo MCP con Excalidraw como tablero interactivo.

El microservicio implementa controles de seguridad activos contra inyección de prompts, protección ante filtración del system prompt, y métricas operacionales en formato Prometheus para observabilidad en producción.

---

## 3. ⚡ Funcionalidades Principales

| Funcionalidad | Descripción |
|---|---|
| **Análisis de Código con IA** | Envía código fuente y una pregunta; recibe análisis conversacional del modelo LLaMA 3.3 70B. Soporta TypeScript, Python y Java. |
| **Generación de Diagramas** | Genera diagramas colaborativos en Excalidraw mediante instrucciones en lenguaje natural y herramientas MCP. |
| **Detección de Inyección de Prompts** | Middleware que bloquea solicitudes con patrones de prompt injection antes de llegar al LLM. |
| **Protección del System Prompt** | Valida que la respuesta del modelo no contenga fragmentos del system prompt (detección de leakage). |
| **Métricas Prometheus** | Expone conteo de peticiones y latencia por ruta en formato compatible con Prometheus/Grafana. |
| **Health Check** | Endpoint de salud para integraciones con load balancers y pipelines de despliegue. |

---

## 4. 📋 Estrategia de Versionamiento y Branches

### Estrategia de Ramas (Git Flow)

#### `main`
- Rama **estable** lista para producción. Dispara el pipeline CI/CD automáticamente.
- Rama **protegida**: PR obligatorio, CI en verde antes de mergear.

#### `develop`
- Integración continua. Recibe merges desde `feature/*`.

#### `feature/*`
- Desarrollo de una funcionalidad específica. **Base:** `develop`. **Cierre:** PR hacia `develop`.

### 4.1 Convenciones para commits

```
feat: agregar detección de inyección de prompts
fix: corregir timeout en llamadas al MCP server
docs: actualizar README con endpoints de métricas
test: agregar pruebas de seguridad en injection_guard
refactor: extraer lógica de safety check a función dedicada
```

---

## 5. ⚙️ Tecnologías Utilizadas

| **Tecnología** | **Uso en el proyecto** |
|---|---|
| **Python 3.12** | Lenguaje base con soporte completo de async/await. |
| **FastAPI 0.135.3** | Framework principal para los endpoints REST asíncronos. |
| **Uvicorn 0.44.0** | Servidor ASGI de alto rendimiento con soporte uvloop. |
| **Starlette 1.0.0** | Base de FastAPI; middleware CORS y routing. |
| **Groq 0.37.1** | Cliente oficial para la API de Groq (inferencia LLM). |
| **LangChain 1.2.15** | Orquestación de cadenas LLM y gestión de mensajes. |
| **LangChain-Groq 1.1.2** | Integración LangChain ↔ Groq (`ChatGroq`). |
| **LangChain-MCP-Adapters 0.2.2** | Adaptadores MCP para herramientas de dibujo colaborativo. |
| **MCP 1.27.1** | Model Context Protocol para conectar el agente con Excalidraw. |
| **Pydantic 2.13.1** | Validación de requests con modelos tipados. |
| **Pydantic-Settings 2.13.1** | Gestión de variables de entorno. |
| **prometheus-client 0.21.1** | Exportación de métricas HTTP en formato Prometheus. |
| **python-dotenv 1.2.2** | Carga de variables de entorno desde `.env`. |
| **pytest** | Framework de pruebas unitarias e integración. |
| **pytest-cov** | Reporte de cobertura de código. |
| **SonarCloud** | Análisis estático de calidad y seguridad. |
| **GitHub Actions** | Pipeline CI/CD automatizado. |
| **Azure App Service** | Plataforma de despliegue en producción. |

---

## 6. 🧩 Funcionalidad y Endpoints

---

### 1️⃣ Analizar Código — `POST /analyze`

#### 📦 Request

| Campo | Tipo | Restricción | Descripción |
|---|---|:---:|---|
| prompt | string | Obligatorio, no vacío | Pregunta o instrucción sobre el código (máx. 2000 chars) |
| code | string | Obligatorio, no vacío | Fragmento de código a analizar (máx. 32000 chars) |

#### 📤 Response (200 OK)

```json
{
  "status": "success",
  "analysis": "El código implementa un patrón singleton mediante el decorador @cache ..."
}
```

| HTTP | Escenario | Mensaje |
|:---:|:---|:---|
| 422 | Código vacío | `"No se proporcionó código para analizar..."` |
| 422 | Prompt vacío | `"La solicitud está vacía..."` |
| 400 | Inyección detectada | `"Solicitud no válida."` |
| 503 | Error de Groq API | `"AI Service unavailable temporary"` |
| 500 | Error inesperado | `"Error processing analysis"` |

**Lenguajes soportados:** TypeScript, Python, Java.

---

### 2️⃣ Generar Diagrama — `POST /draw`

#### 📦 Request

| Campo | Tipo | Restricción | Descripción |
|---|---|:---:|---|
| prompt | string | Obligatorio, no vacío | Descripción del diagrama a generar |
| sessionId | string | Obligatorio, no vacío | ID de sesión del tablero Excalidraw |

#### 📤 Response (200 OK)

```json
{
  "status": "success",
  "response": "Diagrama generado con los componentes solicitados."
}
```

| HTTP | Escenario | Mensaje |
|:---:|:---|:---|
| 422 | Campos vacíos | `"Field cannot be empty"` |
| 500 | Error de procesamiento | `"Error processing drawing request"` |

**Herramientas MCP disponibles:** `draw_shape`, `draw_text`, `draw_arrow`, `add_elements`, `get_board_state`, `clear_board`.

---

### 3️⃣ Health Check — `GET /health`

**Response (200 OK):**

```json
{ "status": "healthy" }
```

---

### 4️⃣ Métricas — `GET /metrics`

Retorna métricas en formato texto compatible con Prometheus.

**Métricas expuestas:**

| Métrica | Tipo | Labels | Descripción |
|---|---|---|---|
| `http_requests_total` | Counter | method, status, route | Total de peticiones HTTP por ruta y código de respuesta |
| `http_request_duration_seconds` | Histogram | method, route | Latencia de peticiones (buckets: 0.1s, 0.5s, 1s, 2s, 5s, 10s) |

---

## 7. 🏛️ Arquitectura, Patrones y Módulos

### Estilo Arquitectónico: Arquitectura Modular por Capas

El dominio de análisis permanece aislado de los controllers HTTP. Las dependencias fluyen de afuera hacia adentro: Middleware → Controllers → Analysis Services → Modelos externos (Groq, MCP).

```
┌─────────────────────────────────────────────────┐
│                   MIDDLEWARE                     │
│  InjectionGuard │ MetricsMiddleware │ CORS       │
└───────────────────────┬─────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────┐
│                  CONTROLLERS                     │
│  AssistantController │ DrawController │ Metrics  │
└───────────────────────┬─────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────┐
│               ANALYSIS SERVICES                  │
│       chatAnalysis (LangChain + Groq)            │
│       drawAnalysis (LangChain + MCP Tools)       │
└───────────────────────┬─────────────────────────┘
                        │
         ┌──────────────┴──────────────┐
         ▼                             ▼
  ┌─────────────┐             ┌───────────────┐
  │  Groq API   │             │  MCP Server   │
  │ LLaMA 3.3   │             │  (Excalidraw) │
  └─────────────┘             └───────────────┘
```

### Patrones de Diseño Aplicados

| Patrón | Dónde se aplica | Propósito |
|---|---|---|
| **Guard / Chain of Responsibility** | `injection_guard.py`, `metrics_middleware.py` | Intercepta y valida cada request antes de llegar al controller. La inyección detectada corta la cadena con HTTP 400. |
| **Adapter** | `board_client.py`, `LangChain-MCP-Adapters` | Traduce las herramientas MCP a funciones invocables por el agente LangChain. |
| **Singleton (cacheado)** | `chatAnalysis._get_model()` | El cliente `ChatGroq` se instancia una sola vez con `@cache` de functools, evitando reconexiones innecesarias. |
| **Strategy** | `chatAnalysis.chatAnalysis()` | Selecciona el nivel de verbosidad de la respuesta (breve vs. completo) según el tamaño del código. |
| **DTO (Data Transfer Object)** | `AnalyzeRequest`, `DrawRequest` | Separa la representación de la API de la lógica interna. Validado con Pydantic antes de llegar al servicio. |
| **Middleware Pipeline** | `main.py` | CORS → MetricsMiddleware → Router. Cada capa tiene responsabilidad única. |
| **Dependency Injection** | FastAPI `APIRouter` + `@router.post` | Inyección de dependencias gestionada por el framework para routers y handlers. |

---

## 8. ⚠️ Manejo de Errores

Los controllers capturan excepciones específicas y retornan respuestas HTTP uniformes mediante `HTTPException` de FastAPI.

### Formato estándar de error

```json
{
  "detail": "Descripción del error"
}
```

### Excepciones manejadas

| ⚠️ Excepción / Escenario | 🔢 HTTP | 💬 Descripción |
|:---|:---:|:---|
| Código o prompt vacío | 422 | Validación de campos obligatorios antes de invocar el LLM |
| Inyección de prompt detectada | 400 | `detect_injection()` retorna `True` para el prompt o el código |
| `groq.APIError` | 503 | Error de disponibilidad del servicio Groq |
| System prompt leakage | — | La respuesta se reemplaza por mensaje genérico; no expone detalles al cliente |
| `ValidationError` de Pydantic | 422 | Campos faltantes o tipos incorrectos en el request body |
| `Exception` genérica | 500 | Error inesperado; se registra en logs con `exc_info=True` |

### Patrones de Inyección Bloqueados

```
ignore instructions  │  you are now        │  repeat your prompt
act as               │  forget instructions │  new persona
jailbreak            │  DAN mode
```

### Beneficios del Manejo de Errores

| 🎯 Beneficio | 📋 Descripción |
|:---|:---|
| **Seguridad** | No expone stack traces ni detalles internos al cliente |
| **Trazabilidad** | Cada error se loguea con `request_id` único (UUID truncado a 8 chars) y duración en ms |
| **Uniformidad** | Todas las respuestas de error usan el esquema `{"detail": "..."}` de FastAPI |

---

## 9. 🧪 Evidencia de Pruebas y Cobertura

### Tipos de pruebas implementadas

| 🧪 Tipo | 📋 Descripción | 🛠️ Herramientas |
|:---|:---|:---|
| **Pruebas Unitarias** | Validan lógica de análisis, guard de inyección y detección de leakage con mocks | pytest + unittest.mock |
| **Pruebas de Endpoints** | Verifican comportamiento HTTP de `/analyze`, `/draw`, `/health` | pytest + FastAPI TestClient |
| **Pruebas de Seguridad** | 16 casos cubriendo cada patrón de inyección y detección de lenguaje | pytest |
| **Cobertura de Código** | Mide el porcentaje cubierto por las pruebas | pytest-cov (XML para SonarCloud) |

### Suites de prueba — 50 casos totales

```
tests/
├── test_analyze.py              (9 casos)
│   ├── Éxito con código válido
│   ├── Código vacío → 422
│   ├── Código solo espacios → 422
│   ├── Prompt vacío → 422
│   ├── Prompt solo espacios → 422
│   ├── Groq APIError → 503
│   ├── Excepción inesperada → 500
│   └── Campos faltantes → 422
│
├── test_chat_analysis.py        (9 casos)
│   ├── Validación de respuesta segura (sin leakage)
│   ├── Detección de fragmentos del system prompt
│   ├── Respuesta segura pasa sin modificación
│   ├── Invocación del modelo con código corto (hint breve)
│   └── Invocación del modelo con código largo (hint completo)
│
├── test_draw.py                 (15 casos)
│   ├── Éxito del endpoint /draw
│   ├── Prompt vacío → 422
│   ├── Prompt solo espacios → 422
│   ├── sessionId vacío → 422
│   ├── sessionId solo espacios → 422
│   ├── Campos faltantes → 422
│   ├── Error en drawAnalysis → 500
│   ├── Unit tests de drawAnalysis (output del agente)
│   ├── Respuestas de fallback
│   └── Context manager board_session
│
├── test_health.py               (1 caso)
│   └── GET /health → {"status": "healthy"}
│
└── test_injection_guard.py      (16 casos)
    ├── Detección de 8 patrones de inyección
    ├── Case-insensitive matching
    ├── Detección de lenguaje Python
    ├── Detección de lenguaje TypeScript
    ├── Detección de lenguaje Java
    └── Manejo de texto vacío / solo espacios
```

### Cómo ejecutar las pruebas

```bash
# Ejecutar todas las pruebas
pytest tests/

# Con reporte de cobertura en terminal
pytest tests/ --cov=app --cov-report=term-missing

# Generar reporte XML (usado por SonarCloud)
pytest tests/ --cov=app --cov-report=xml:coverage.xml --cov-report=term-missing

# Suite específica
pytest tests/test_injection_guard.py -v
```

---

## 10. 🗂️ Organización del Código

```
NetAI/
│
├── .github/
│   └── workflows/
│       └── deploy.yml                    # Pipeline CI/CD (tests + Sonar + Azure deploy)
│
├── app/
│   ├── main.py                           # 🔵 Entry point: FastAPI app, middleware, routers
│   ├── __init__.py
│   │
│   ├── controllers/                      # 🟠 CAPA DE ENTRADA (HTTP Adapters)
│   │   ├── __init__.py
│   │   ├── assistant_controller.py       # POST /analyze, GET /health
│   │   ├── draw_controller.py            # POST /draw
│   │   └── metrics_controller.py         # GET /metrics
│   │
│   ├── analysis/                         # 🟢 CAPA DE NEGOCIO (LLM Services)
│   │   ├── __init__.py
│   │   ├── chatAnalysis.py               # LLM análisis de código (LangChain + Groq)
│   │   ├── drawAnalysis.py               # Generación de diagramas con agente MCP
│   │   └── metrics_service.py            # Counters y histogramas Prometheus
│   │
│   ├── middleware/                       # 🔴 CROSS-CUTTING CONCERNS
│   │   ├── __init__.py
│   │   ├── injection_guard.py            # Detección de prompt injection y lenguaje
│   │   └── metrics_middleware.py         # Tracking HTTP requests/latencia
│   │
│   ├── models/                           # 🟡 DATA TRANSFER OBJECTS
│   │   ├── __init__.py
│   │   └── analyze_request.py            # Pydantic: AnalyzeRequest
│   │
│   └── mcp/                              # 🟣 MCP CLIENT (Excalidraw)
│       ├── __init__.py
│       └── board_client.py               # Context manager para sesiones MCP
│
├── tests/
│   ├── __init__.py
│   ├── test_analyze.py
│   ├── test_chat_analysis.py
│   ├── test_draw.py
│   ├── test_health.py
│   └── test_injection_guard.py
│
├── requirements.txt                      # Dependencias pip
├── sonar-project.properties              # Config SonarCloud
├── .env.example                          # Variables de entorno requeridas
└── README.md
```

---

## 11. 🔗 Conexiones con Servicios Externos

| Servicio | Tipo | Variable de Entorno | Descripción |
|---|---|---|---|
| **Groq API** | HTTP REST (LLM) | `GROQ_API_KEY` | Inferencia LLaMA 3.3 70B. Timeout 30s, máx. 2 reintentos. Sin esta clave el endpoint `/analyze` retorna 503. |
| **MCP Server (Excalidraw)** | HTTP + MCP Protocol | `MCP_SERVER_URL` | Servidor MCP que gestiona el estado del tablero Excalidraw. Default: `http://localhost:3003/mcp`. Requerido para `/draw`. |
| **SonarCloud** | CI (análisis estático) | `SONAR_TOKEN` (secret) | Análisis de calidad y cobertura en cada push a `main`. Organización: `n3trs`, proyecto: `N3TRS_NetAI`. |
| **Azure App Service** | PaaS (deploy) | `AZURE_WEBAPP_PUBLISH_PROFILE` (secret) | Destino de despliegue automático tras CI verde. App name: `omnicode-api-python`. |

---

## 12. 🚀 Ejecución del Proyecto

### 📋 Prerrequisitos

- **Python 3.12+** y **pip**
- Clave de API de Groq: [console.groq.com](https://console.groq.com)

### 🛠️ Local con Python

```bash
# 1. Clonar el repositorio
git clone <repo-url>
cd NetAI

# 2. Crear entorno virtual e instalar dependencias
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 3. Configurar variables de entorno
cp .env.example .env
# Editar .env y agregar GROQ_API_KEY=<tu-clave>

# 4. Ejecutar el servidor
uvicorn app.main:app --reload --port 8080
```

📍 **URL Local:** `http://localhost:8080`
📚 **Swagger UI:** `http://localhost:8080/docs`
📊 **ReDoc:** `http://localhost:8080/redoc`

### ⚙️ Variables de Entorno

| Variable | Requerida | Valor por defecto | Descripción |
|:---|:---:|:---|:---|
| `GROQ_API_KEY` | ✅ Sí | — | Clave de autenticación Groq API |
| `MCP_SERVER_URL` | ❌ No | `http://localhost:3003/mcp` | URL del servidor MCP para el endpoint `/draw` |

---

## 13. ⚙️ Pipelines CI/CD

### Pipeline — `deploy.yml`

Se ejecuta en cada **push a `main`**:

```yaml
name: Deploy to Azure App Service

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov
      - name: Run tests and generate coverage
        run: pytest tests/ --cov=app --cov-report=xml:coverage.xml --cov-report=term-missing
      - name: SonarQube Scan
        uses: SonarSource/sonarqube-scan-action@v6
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
      - name: Deploy to Azure App Service
        uses: azure/webapps-deploy@v2
        with:
          app-name: 'omnicode-api-python'
          publish-profile: ${{ secrets.AZURE_WEBAPP_PUBLISH_PROFILE }}
          package: .
```

**Flujo completo:**

```
Push a main
    │
    ├─ Checkout + Setup Python 3.12
    ├─ pip install -r requirements.txt + pytest
    ├─ pytest (50 tests) + cobertura XML
    ├─ SonarCloud scan (calidad + coverage)
    │
    └─ Deploy Azure App Service → 🟢 omnicode-api-python
```

### Secrets de GitHub requeridos

| Secret | Descripción |
|---|---|
| `SONAR_TOKEN` | Token de SonarCloud (org: n3trs) |
| `AZURE_WEBAPP_PUBLISH_PROFILE` | Perfil de publicación de Azure App Service |

---

## 14. ☁️ Despliegue en Azure

El microservicio está desplegado en **Azure App Service**.

| Recurso | Valor |
|---|---|
| **App Service Name** | `omnicode-api-python` |
| **Runtime** | Python 3.12, Linux |
| **Trigger** | Push automático desde `main` vía GitHub Actions |

### Variables de entorno en Azure App Service

| Nombre | Descripción |
|---|---|
| `GROQ_API_KEY` | Clave de autenticación Groq (requerida) |
| `MCP_SERVER_URL` | URL del servidor MCP para el endpoint `/draw` |

---

## 15. 🤝 Integrantes y Contribuciones

<div align="center">

![Course](https://img.shields.io/badge/Course-ARSW-orange?style=for-the-badge)
![Year](https://img.shields.io/badge/Year-2026--1-blue?style=for-the-badge)

| 👤 Integrante | 🎓 Rol |
|:---|:---|
| Tulio Riaño Sánchez | Desarrollo y arquitectura |
| Julian Camilo Lopez Barrero | Desarrollo y arquitectura |
| Juan Sebastián Puentes Julio | Desarrollo y arquitectura |
| David Alejandro Patacon Henao | Desarrollo y arquitectura |

> 💡 **NetAI** analiza código fuente con inteligencia artificial, ayudando a desarrolladores a detectar errores, malas prácticas y oportunidades de mejora en TypeScript, Python y Java — de forma segura y conversacional.

**🎓 Escuela Colombiana de Ingeniería Julio Garavito**

</div>
