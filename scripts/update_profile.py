"""Generate a self-contained profile dashboard using Python 3 and authenticated gh."""
import json
import os
import re
import subprocess
from collections import Counter
from datetime import datetime, timezone
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COLORS = ['#00e5ff', '#ff2d95', '#a78bfa', '#ffc857', '#5ee6a8', '#92a4c7']


def api(*args):
    result = subprocess.run(['gh', 'api', *args], check=True, capture_output=True, text=True, timeout=90)
    data = json.loads(result.stdout)
    if isinstance(data, dict) and data.get('errors'):
        raise RuntimeError('GitHub GraphQL returned errors')
    return data


def fetch(owner):
    repos = []
    page = 1
    while True:
        batch = api(f'users/{owner}/repos?type=owner&per_page=100&page={page}')
        repos.extend(r for r in batch if not r['fork'] and not r['private'])
        if len(batch) < 100:
            break
        page += 1
    query = '''query($login:String!){user(login:$login){contributionsCollection{
      startedAt endedAt totalCommitContributions totalPullRequestContributions
      totalIssueContributions contributionCalendar{totalContributions weeks{
      contributionDays{date weekday contributionCount contributionLevel}}}}}}'''
    result = api('graphql', '-f', f'query={query}', '-f', f'login={owner}')
    user = result['data']['user']
    if not user:
        raise RuntimeError('GitHub user not found')
    return repos, user['contributionsCollection']


def render(repos, activity, updated):
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="690" viewBox="0 0 1200 690" role="img" aria-labelledby="title desc">',
             '<title id="title">GitHub / Live telemetry</title>',
             '<desc id="desc">Repositorios públicos propios sin forks, lenguajes principales y actividad de GitHub.</desc>',
             '<rect width="1200" height="690" rx="18" fill="#0b1020"/>',
             '<rect x="1" y="1" width="1198" height="688" rx="18" fill="none" stroke="#29334f"/>']

    def text(x, y, value, size=14, color='#97a7c6'):
        parts.append(f'<text x="{x}" y="{y}" font-family="monospace" font-size="{size}" fill="{color}">{escape(str(value))}</text>')

    def rect(x, y, w, h, color, radius=4, label=None):
        parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{color}">')
        if label:
            parts.append(f'<title>{escape(label)}</title>')
        parts.append('</rect>')

    text(35, 40, '> github --telemetry', 19, '#00e5ff')
    text(845, 40, f'ACTUALIZADO {updated} UTC', 12)
    calendar = activity['contributionCalendar']
    metrics = [(len(repos), 'REPOS PÚBLICOS'),
               (sum(r['stargazers_count'] for r in repos), 'ESTRELLAS'),
               (calendar['totalContributions'], 'CONTRIBUCIONES'),
               (activity['totalCommitContributions'], 'COMMITS'),
               (activity['totalPullRequestContributions'], 'PULL REQUESTS')]
    for i, (value, label) in enumerate(metrics):
        x = 35 + i * 230
        rect(x, 66, 210, 92, '#121b30')
        text(x + 16, 109, f'{value:,}', 31, COLORS[i])
        text(x + 16, 139, label, 12)
    text(35, 189, 'LENGUAJE PRINCIPAL / repositorios, sin forks', 14, '#e1e9ff')
    languages = Counter(r['language'] for r in repos if r.get('language'))
    ranking = languages.most_common()
    if len(ranking) > 6:
        ranking = ranking[:5] + [('Otros', sum(n for _, n in ranking[5:]))]
    maximum = max(languages.values(), default=1)
    for i, (language, count) in enumerate(ranking):
        col, row = i % 2, i // 2
        x, y = 35 + col * 585, 219 + row * 43
        text(x, y, language, 13, '#d8e4ff')
        text(x + 445, y, f'{count} repos', 12)
        rect(x, y + 9, 530, 6, '#1c2840', 3)
        rect(x, y + 9, round(530 * count / maximum, 2), 6, COLORS[i], 3)
    if not ranking:
        text(35, 235, 'Todavía no hay lenguajes detectados.')
    start, end = activity['startedAt'][:10], activity['endedAt'][:10]
    text(35, 365, 'CONTRIBUTION MATRIX', 14, '#00e5ff')
    text(670, 365, f'PERÍODO {start} / {end}', 13)
    levels = {'NONE': '#1b253b', 'FIRST_QUARTILE': '#124c64', 'SECOND_QUARTILE': '#137c93',
              'THIRD_QUARTILE': '#13b8c5', 'FOURTH_QUARTILE': '#00e5ff'}
    weeks = calendar['weeks']
    step = min(20, 1090 / max(len(weeks), 1))
    days = []
    for col, week in enumerate(weeks):
        for day in week['contributionDays']:
            days.append(day)
            rect(round(62 + col * step, 2), 392 + day['weekday'] * 20, round(step - 4, 2), 16,
                 levels[day['contributionLevel']], 3,
                 f"{day['date']}: {day['contributionCount']} contribuciones")
    for y, label in [(424, 'L'), (464, 'M'), (504, 'V')]:
        text(35, y, label, 11)
    active = sum(d['contributionCount'] > 0 for d in days)
    best = current = 0
    for day in sorted(days, key=lambda d: d['date']):
        current = current + 1 if day['contributionCount'] else 0
        best = max(best, current)
    text(35, 567, f'{active} días activos  /  mejor racha del período: {best} días', 14, '#d8e4ff')
    text(905, 567, 'MENOS', 10)
    for i, color in enumerate(levels.values()):
        rect(948 + i * 22, 554, 16, 16, color, 3)
    text(1068, 567, 'MÁS', 10)
    text(35, 620, 'Repos y estrellas: públicos propios. Actividad: período indicado arriba.', 12)
    text(35, 649, 'Lenguajes por número de repositorios; no representan nivel de dominio.', 12)
    parts.append('</svg>')
    return '\n'.join(parts) + '\n'


def main():
    owner = os.environ.get('PROFILE_USERNAME', 'CristianSinoe')
    if not re.fullmatch(r'[A-Za-z0-9-]+', owner):
        raise ValueError('Invalid GitHub username')
    repos, activity = fetch(owner)
    svg = render(repos, activity, datetime.now(timezone.utc).strftime('%Y-%m-%d'))
    target = ROOT / 'assets' / 'metrics.svg'
    target.parent.mkdir(exist_ok=True)
    temporary = target.with_suffix('.tmp')
    temporary.write_text(svg, encoding='utf-8')
    temporary.replace(target)
    print(f'Updated dashboard: {len(repos)} public repositories')


if __name__ == '__main__':
    main()
