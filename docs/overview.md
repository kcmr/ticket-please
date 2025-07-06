# Especificaciones del Proyecto: Asistente CLI para Tareas (Jira/GitHub)

## 1. Overview del Proyecto

**Nombre provisional:** TicketPlease (tk)


**Elevator Pitch:** TicketPlease es una herramienta de línea de comandos (CLI) desarrollada en Python que utiliza IA para ayudar a desarrolladores e ingenieros a generar descripciones de tareas estandarizadas y de alta calidad para plataformas como Jira y GitHub. A través de un flujo interactivo, la herramienta recopila los requisitos clave y produce un texto formateado listo para ser copiado y pegado, acelerando el proceso de creación de tickets y mejorando la claridad de las tareas.

**Problema que resuelve:** La creación manual de tareas es repetitiva y propensa a inconsistencias. A menudo se omiten detalles importantes como los Criterios de Aceptación (AC) o la Definición de Hecho (DoD), lo que genera ambigüedad. Esta herramienta automatiza y estandariza este proceso.

**Público objetivo:** Desarrolladores de software, Product Managers, QA Engineers, y cualquier persona que cree tareas en Jira o GitHub.

## 2. Objetivos Principales

- **Acelerar la creación de tareas:** Reducir significativamente el tiempo dedicado a escribir descripciones de tickets.
- **Estandarizar el formato:** Asegurar que todas las tareas sigan una estructura consistente, incluyendo AC y DoD.
- **Mejorar la calidad:** Utilizar la IA para generar textos claros, bien redactados y completos a partir de entradas concisas del usuario.
- **Flexibilidad:** Permitir al usuario elegir su proveedor de LLM preferido (OpenAI, Anthropic, Google, OpenRouter) y personalizar las plantillas.
- **Facilidad de uso:** Ofrecer una experiencia de usuario fluida e intuitiva directamente desde la terminal.

## 3. Características Clave (Features)

- **Flujo Interactivo Guiado:** La CLI hace preguntas paso a paso para recopilar toda la información necesaria.
- **Generación de Contenido por IA:** Utiliza un LLM para procesar las respuestas del usuario y generar una descripción completa y bien formateada.
- **Soporte Multiplataforma:** Genera la salida en Markdown para GitHub o en el formato de marcado de texto de Jira.
- **Configuración Inicial Guiada (Onboarding):** En el primer uso, la herramienta guía al usuario para configurar su API Key y el modelo de IA a utilizar.
- **Persistencia y Memoria:** Guarda las preferencias del usuario (idioma, paths a archivos, plataforma) para pre-rellenarlas en futuros usos.
- **Refinamiento Iterativo:** Permite al usuario solicitar modificaciones sobre el texto generado antes de aceptarlo.
- **Soporte Multilingüe:** Acepta la entrada en el idioma del usuario y genera la salida en el idioma configurado.
- **Integración con el Portapapeles:** Copia automáticamente el texto final al portapapeles para un uso inmediato.

## 4. Especificaciones Técnicas

### 4.1. Stack Tecnológico

- **Lenguaje:** Python 3.10+
- **Librerías CLI:**
  - **Typer:** Para crear una interfaz de línea de comandos robusta y fácil de usar.
  - **rich:** Para mejorar la visualización en la terminal (colores, tablas, spinners).
  - **questionary o InquirerPy:** Para las preguntas interactivas (listas de selección, autocompletado).
- **Integración con IA:** litellm: Para abstraer las llamadas a las diferentes APIs de LLMs (OpenAI, Anthropic, Gemini, OpenRouter) con una única interfaz.
- **Utilidades:**
  - **pyperclip:** Para la gestión del portapapeles multiplataforma.
**PyYAML o toml:** Para la gestión del archivo de configuración.

### 4.2. Gestión de Configuración

**Ubicación:** El archivo de configuración se guardará en el directorio home del usuario (p. ej., ~/.config/ticketplease/config.toml).

Estructura del archivo config.toml:

```toml
# ~/.config/ticketplease/config.toml

[api_keys]
# Las claves se guardarán aquí de forma segura.
# Se recomienda usar 'keyring' para un almacenamiento más seguro en el futuro.
provider = "openai" # openai, anthropic, gemini, openrouter
api_key = "sk-..."

[llm]
model = "gpt-4o-mini" # Modelo específico, p.ej. "claude-3-haiku-20240307", "gemini-1.5-pro-latest"

[preferences]
default_output_language = "es" # 'es' o 'en'
default_platform = "github"  # 'github' o 'jira'
default_ac_path = "/Users/user/templates/default_ac.md"
default_dod_path = "/Users/user/templates/default_dod.md"
```

### 4.3. Formato de Salida

La herramienta deberá formatear la salida según la plataforma seleccionada.

GitHub (Markdown):

```markdown
### Descripción

Aquí va la descripción general de la tarea.

### Criterios de Aceptación
- [ ] El usuario puede hacer X.
- [ ] El sistema responde con Y.
- [ ] Se registra el evento Z en el log.

### Definition of Done
- [ ] Código revisado por pares (PR aprobado).
- [ ] Pruebas unitarias cubren el 100% del nuevo código.
- [ ] La documentación ha sido actualizada.
```

Jira (Markup):

```markdown
h3. Descripción

Aquí va la descripción general de la tarea.

h3. Criterios de Aceptación
* El usuario puede hacer X.
* El sistema responde con Y.
* Se registra el evento Z en el log.

h3. Definition of Done
* Código revisado por pares (PR aprobado).
* Pruebas unitarias cubren el 100% del nuevo código.
* La documentación ha sido actualizada.
```

## 5. Flujo de Usuario

### 5.1. Primer Uso (Onboarding)

- El usuario ejecuta `tk config`.
- La herramienta detecta que no existe ~/.config/ticketplease/config.toml.
- Inicia el asistente de configuración:
  - Pregunta 1: "Elige tu proveedor de IA: [OpenAI, Anthropic, Gemini, OpenRouter]".
  - Pregunta 2: "Por favor, introduce tu API Key".
  - Pregunta 3: "Elige un modelo de la lista: [gpt-4o-mini, claude-3-sonnet..., etc.]" (La lista se obtiene vía litellm).
  - Guarda la configuración en el archivo config.toml.
  - El usuario puede ejecutar `tk please` para crear tareas.

### 5.2. Uso Regular

- El usuario ejecuta `tk please` en su terminal.
- La herramienta carga las preferencias desde config.toml.
- Pregunta 1: ¿Qué hay que hacer? (Describe la tarea brevemente)
- Pregunta 2: Plataforma de destino: [GitHub | Jira] (pre-seleccionada según la preferencia).
- Pregunta 3: Criterios de Aceptación (escribe una lista, o introduce un path a un archivo .md/.txt): (muestra el path por defecto si existe).
- Pregunta 4: Definition of Done (escribe una lista, o introduce un path a un archivo): (muestra el path por defecto si existe).
- Pregunta 5: Idioma de salida: [Español | Inglés] (pre-seleccionada según la preferencia).
- La herramienta muestra un spinner de carga (Generando descripción con IA...).
- Se envía una petición al LLM configurado (vía litellm) con un prompt estructurado.
- Se muestra la descripción generada con formato rich.
- Pregunta final: ¿Qué quieres hacer? [Aceptar y copiar | Refinar | Cancelar]
  - Aceptar y copiar: El texto se copia al portapapeles. La herramienta muestra "¡Texto copiado al portapapeles!" y finaliza.
  - Refinar: Pregunta al usuario ¿Qué te gustaría cambiar o añadir?. Envía una nueva petición al LLM con la descripción original y la solicitud de refinamiento. Vuelve al paso 10.
  - Cancelar: La herramienta finaliza sin realizar ninguna acción.

## 6. Estructura de Comandos CLI (Propuesta)

```bash
# Inicia el flujo interactivo principal para crear una nueva tarea
\$ tk please

# Muestra la ayuda (comportamiento por defecto sin argumentos)
\$ tk

# Muestra la versión de la herramienta
\$ tk --version
\$ tk -v

# Permite gestionar la configuración
\$ tk config
# Opciones interactivas para:
# - Ver la configuración actual
# - Cambiar la API Key o el proveedor
# - Cambiar el modelo de LLM
# - Actualizar las preferencias (idioma, paths por defecto)

```

## 7. Consideraciones Adicionales y Futuras Mejoras

- Integración Directa con APIs: Conectar directamente con las APIs de Jira y GitHub para crear el ticket/issue desde la CLI.
- Plantillas personalizadas: Permitir a los usuarios crear y guardar sus propias plantillas de prompt.
- Soporte para Bugs y otros tipos de Issues: Añadir flujos específicos para reportar bugs (p. ej., "Pasos para reproducir", "Comportamiento esperado vs. actual").
- Empaquetado y Distribución: Publicar el paquete en PyPI (pip install taskgenius) y considerar la distribución a través de Homebrew o Scoop.
