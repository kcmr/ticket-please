# Especificaciones Técnicas

Este documento define las directrices técnicas, los estándares de codificación y el flujo de trabajo de desarrollo para el proyecto Ticket Please. El objetivo es garantizar un código consistente, legible, mantenible y de alta calidad. El nombre del paquete en PyPI será ticketplease y el comando de la CLI será tkp.

## Gestión de Dependencias

- Se utilizará Poetry para la gestión del entorno virtual y la instalación de dependencias
- Se utilizará asdf para la gestión de versiones de Python y Poetry
- Se utilizará el archivo pyproject.toml como única fuente de verdad para la configuración del proyecto

## Calidad de código y estilo

- Se utilizará ruff para linting y formateo del código. Su configuración estará en el archivo pyproject.toml
- Se utilizará pytest para testing. Su configuración estará en el archivo pyproject.toml

## Automatización de tareas

- Se utilizará un archivo Makefile para simplificar la ejecución de tareas comunes de desarrollo como setup, format, lint, test, check (format + test), etc.

## Commit Messages

- Se utilizará la convención de commit messages de Conventional Commits.
- Se utilizará .pre-commit-config.yaml para la configuración de pre-commit hooks.
- En el pre-commit se validará el formato del código, corrigiendo aquello que sea posible automáticamente y el formato de los commit messages.
- En el pre-push se ejecutarán los tests.

## Testing

- Se utilizará pytest para testing. Su configuración estará en el archivo pyproject.toml
- Se utilizará coverage para medir la cobertura de los tests. Su configuración estará en el archivo pyproject.toml

## Tipado

- Se utilizará mypy para tipado estático. Su configuración estará en el archivo pyproject.toml
- Se utilizarán type hints en el código.

## Integración y despliegue continuo

- Se utilizará GitHub Actions para automatizar el ciclo de vida de la integración, pruebas y distribución.
- Las validaciones se realizarán en cada push a ramas de desarrollo y en cada pull request hacia la rama main.
- Los merges en main se realizarán mediante pull requests.
- Los merges en main desencadenarán el workflow de release.

### Release

El workflow de release se encargará de:

1. Ejecutar todas las validaciones del workflow de CI.
2. Construir los binarios para las plataformas objetivo (ver sección "Empaquetado y distribución").
3. Crear una nueva "Release" en GitHub.
4. Adjuntar los binarios generados a la release.

## Empaquetado y distribución

El objetivo es distribuir Ticket Please como un binario ejecutable único para facilitar su uso en diferentes sistemas operativos.

- Herramienta de Empaquetado: Se utilizará PyInstaller para convertir el script de Python en un ejecutable standalone.
- Plataformas Objetivo:
  - macOS (x86_64 y arm64)
  - Linux (x86_64)
  - Windows (x86_64)
- Proceso: El proceso de construcción será gestionado por el workflow de release.yml en GitHub Actions, que ejecutará PyInstaller en máquinas virtuales de cada uno de los sistemas operativos objetivo. Los artefactos resultantes (ejecutables) se publicarán en la página de Releases del repositorio.
