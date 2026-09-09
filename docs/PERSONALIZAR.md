# Personalizar el perfil

El README se muestra en el perfil cuando estos archivos se publican en la rama `main` del repositorio público `CristianSinoe/CristianSinoe`.

- `README.md`: presentación, tecnologías, enlaces y proyectos. La redacción en primera persona es editable.
- `assets/header.svg`: banner vectorial propio; paleta cian `#00e5ff`, magenta `#ff2d95` y fondo `#070b14`. El cursor respeta la preferencia de movimiento reducido.
- `assets/metrics.svg`: última instantánea de datos reales; funciona desde la primera publicación.
- `scripts/update_profile.py`: generador sin dependencias Python externas. Requiere Python 3 y GitHub CLI autenticado (`gh auth login` localmente).
- `.github/workflows/profile.yml`: actualización diaria a las 12:23 UTC, manual desde Actions y al cambiar el generador.

## Actualizar localmente

```sh
python3 scripts/update_profile.py
```

En Actions se usa el `GITHUB_TOKEN` automático; no hace falta agregar un token personal. El workflow necesita permiso `contents: write` y que las reglas de la rama permitan su commit. Si el job falla, permanece la última imagen publicada. Revisar la ejecución inicial en Actions después de publicar; todavía no se ha ejecutado desde GitHub en esta preparación local.

Repositorios y estrellas: proyectos públicos propios sin forks, incluyendo archivados. Lenguajes: cantidad de repositorios por lenguaje principal; excluye repositorios sin lenguaje y agrupa los menos frecuentes si hay más de seis. Actividad: intervalo devuelto por `contributionsCollection`; incluye los datos visibles para el token. La mejor racha se limita al período mostrado. No se guardan nombres ni contenido de repositorios privados.

Los iconos del stack dependen de skillicons.dev y las insignias de shields.io. El banner y el panel son archivos locales. Los enlaces y textos alternativos siguen disponibles si los servicios de iconos fallan.

Fuentes técnicas: [GitHub GraphQL](https://docs.github.com/en/graphql/reference), [actions/checkout](https://github.com/actions/checkout). Los proyectos y tecnologías se comprobaron con los repositorios públicos del perfil.
