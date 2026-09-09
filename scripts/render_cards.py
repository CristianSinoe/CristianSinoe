"""Render the static terminal cards. Python standard library only."""
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'


def text(x, y, value, size=20, color='#e5edff'):
    return f'<text x="{x}" y="{y}" font-family="monospace" font-size="{size}" fill="{color}">{escape(value)}</text>'


def card(filename, title, command, body, height, description):
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="{height}" viewBox="0 0 1100 {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>
<rect width="1100" height="{height}" rx="18" fill="#0b1020"/>
<rect x="1" y="1" width="1098" height="{height-2}" rx="18" fill="none" stroke="#29334f"/>
<path d="M25 1H360" stroke="#00e5ff" stroke-width="2"/><path d="M360 1H520" stroke="#ff2d95" stroke-width="2"/>
<circle cx="30" cy="30" r="4" fill="#ff2d95"/><circle cx="47" cy="30" r="4" fill="#ffc857"/><circle cx="64" cy="30" r="4" fill="#00e5ff"/>
{ text(88, 35, title, 13, '#9baaca') }
{ text(985, 35, '>_', 15, '#00e5ff') }
<path d="M24 58H1076" stroke="#29334f"/>
{ text(34, 100, '$ ' + command, 20, '#00e5ff') }
{body}
</svg>'''
    (ASSETS / filename).write_text(svg + '\n', encoding='utf-8')


def main():
    card('intro.svg', '00 / CONNECT', 'cat introduction.txt',
         text(34, 151, 'Desarrollo web / APIs / Simulación / Experimentos con Python') +
         text(34, 195, 'Construyo interfaces, conecto servicios y convierto ideas', 19, '#9baaca') +
         text(34, 224, 'en proyectos que funcionan.', 19, '#9baaca') +
         text(34, 278, '[ EXPLORAR REPOSITORIOS > ]', 16, '#ff2d95'), 315,
         'Desarrollo web, APIs, simulación y experimentos con Python. Explorar repositorios.')

    rows = [('LENGUAJES', ['Java', 'Python', 'JavaScript', 'TypeScript', 'HTML', 'CSS']),
            ('FRONTEND', ['React', 'Vite']),
            ('BACKEND / DATOS', ['Spring Boot', 'PostgreSQL', 'Prisma']),
            ('HERRAMIENTAS', ['Git', 'GitHub', 'Docker'])]
    body = text(34, 140, 'Tecnologías presentes en mis repositorios. Siempre aprendiendo.', 17, '#9baaca')
    for i, (label, items) in enumerate(rows):
        y = 185 + i * 80
        body += text(34, y, label, 13, '#a78bfa')
        x = 245
        for item in items:
            width = len(item) * 11 + 28
            body += f'<rect x="{x}" y="{y-25}" width="{width}" height="38" rx="7" fill="#121b30" stroke="#294159"/>'
            body += text(x+14, y, item, 18, '#e5edff')
            x += width + 10
    body += '<path d="M34 463H1066" stroke="#29334f"/>'
    body += text(34, 502, 'REST APIs / WebSockets / JWT / OTP', 18, '#00e5ff')
    body += text(34, 535, 'Spring Security / JPA / Hibernate', 18, '#9baaca')
    card('stack.svg', '02 / TECH ARSENAL', 'stack --list', body, 570,
         'Lenguajes: Java, Python, JavaScript, TypeScript, HTML, CSS. Frontend: React, Vite. Backend: Spring Boot, PostgreSQL, Prisma. Herramientas: Git, GitHub, Docker. REST APIs, WebSockets, JWT, OTP, Spring Security, JPA e Hibernate.')

    projects = [
        ('gridbot', '03.1 / MISSION CONTROL', 'GRIDBOT', ['Simulador de robots sobre una cuadrícula.', 'Interfaz web, API con WebSocket y motor de simulación compartido.'], 'TypeScript / React / Vite / Prisma / Docker'),
        ('auth', '03.2 / MISSION CONTROL', 'Auth MFA', ['Autenticación multifactor con registro e inicio de sesión.', 'Códigos OTP por correo y acceso protegido con JWT.'], 'Java / Spring Boot / React / PostgreSQL'),
        ('tutorlink', '03.3 / MISSION CONTROL', 'TutorLink', ['Proyecto académico: una parte de mi recorrido construyendo', 'software y llevando ideas al código.'], 'JavaScript / Proyecto académico'),
        ('python', '03.4 / MISSION CONTROL', 'Laboratorio Python', ['Prácticas y experimentos de inteligencia artificial:', 'clasificación de correo y redes de Hopfield.'], 'Python / Inteligencia artificial / Aprendizaje')]
    for slug, title, name, lines, stack in projects:
        body = text(34, 151, name, 30)
        body += text(34, 198, lines[0], 19, '#9baaca') + text(34, 229, lines[1], 19, '#9baaca')
        body += text(34, 278, stack, 17, '#a78bfa')
        body += text(34, 328, '[ ABRIR PROYECTO > ]', 15, '#ff2d95')
        card(f'project-{slug}.svg', title, 'projects --open ' + slug, body, 362, name + '. ' + ' '.join(lines) + ' ' + stack)

    body = ''
    interests = [('SIMULACIÓN', 'Conectar interfaces con simulaciones y lógica en acción.'),
                 ('SEGURIDAD', 'Construir autenticación y proteger APIs.'),
                 ('INTELIGENCIA ARTIFICIAL', 'Experimentar con Python y aprender haciendo.'),
                 ('FULL STACK', 'Trabajar en interfaz, backend y datos.')]
    for i, (label, value) in enumerate(interests):
        y = 150 + i * 82
        body += text(34, y, label, 13, '#a78bfa') + text(34, y+32, value, 20)
    card('beyond.svg', '05 / BEYOND THE CODE', 'cat interests.txt', body, 458,
         ' '.join(value for _, value in interests))
    card('footer.svg', '06 / NEXT CONNECTION', 'echo $MINDSET',
         text(34, 159, 'Código, propósito y un poco de caos.', 28) +
         text(34, 210, 'Explora un proyecto, revisa el código y acompaña', 19, '#9baaca') +
         text(34, 240, 'el siguiente experimento.', 19, '#9baaca') +
         text(34, 294, '[ EXPLORAR TODOS LOS PROYECTOS > ]', 16, '#ff2d95'), 331,
         'Código, propósito y un poco de caos. Explorar todos los proyectos.')


if __name__ == '__main__':
    main()
