# Personalizar el perfil

El README se muestra en el perfil cuando estos archivos se publican en la rama `main` del repositorio público `CristianSinoe/CristianSinoe`.

- `README.md`: presentación, tecnologías, enlaces y proyectos. La redacción en primera persona es editable.
- `assets/header.svg`: banner vectorial propio; paleta cian `#00e5ff`, magenta `#ff2d95` y fondo `#070b14`. El cursor respeta la preferencia de movimiento reducido.
- `scripts/render_cards.py`: contenido y diseño de las tarjetas estáticas; regenerar con `python3 scripts/render_cards.py`. Los proyectos son imágenes enlazadas desde el README.
- `assets/about.svg`: presentación y frase personal.
- `assets/metrics.svg`: última instantánea de datos reales; funciona desde la primera publicación.
- `scripts/update_profile.py`: generador sin dependencias Python externas. Requiere Python 3 y GitHub CLI autenticado (`gh auth login` localmente).
- `.github/workflows/profile.yml`: actualización diaria a las 12:23 UTC, manual desde Actions y al cambiar el generador.

## Actualizar localmente

```sh
python3 scripts/update_profile.py
```

En Actions se usa el `GITHUB_TOKEN` automático; no hace falta agregar un token personal. El workflow necesita permiso `contents: write` y que las reglas de la rama permitan su commit. Si el job falla, permanece la última imagen publicada. Revisar las ejecuciones en Actions después de publicar cambios en el generador.

Repositorios y estrellas: proyectos públicos propios sin forks, incluyendo archivados. Lenguajes: cantidad de repositorios por lenguaje principal; excluye repositorios sin lenguaje y agrupa los menos frecuentes si hay más de seis. Actividad: intervalo devuelto por `contributionsCollection`; incluye los datos visibles para el token. La mejor racha se limita al período mostrado. No se guardan nombres ni contenido de repositorios privados.

Todas las tarjetas son SVG locales con fondo oscuro fijo, independiente del tema de GitHub. Los enlaces se definen en el README para que las tarjetas de proyectos sean clicables. Cada imagen incluye texto alternativo; la presentación también está disponible como texto desplegable.

Fuentes técnicas: [GitHub GraphQL](https://docs.github.com/en/graphql/reference), [actions/checkout](https://github.com/actions/checkout). Los proyectos y tecnologías se comprobaron con los repositorios públicos del perfil.
