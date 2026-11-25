#!/usr/bin/env python3
"""Build a redirect-only copy of the site for its old address.

The manual moved from https://geoflac.github.io/des3d/ to
https://geoflac.github.io/DynEarthSol/. GitHub Pages cannot redirect on the
server, so des3d's own Pages site keeps serving this output instead:

* one small page for every HTML page of the real build, at the same path,
  that forwards to the same path under the new address (query string and
  #anchor kept);
* a 404.html that does the same for any other path;
* verbatim copies of the directories given with --copy (downloadable
  files), so direct download links and scripts that fetch them keep working.

Usage:
  python3 scripts/make_redirect_site.py build redirect-site \
      --new-base https://geoflac.github.io/DynEarthSol/ \
      --old-base /des3d/ --copy downloads --copy tutorial
"""

import argparse
import html
import json
import shutil
from pathlib import Path

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Moved to {url}</title>
<link rel="canonical" href="{url}">
<meta name="robots" content="noindex">
<meta http-equiv="refresh" content="0; url={url}">
<script>location.replace({url_js} + location.search + location.hash);</script>
</head>
<body>
<p>The DynEarthSol manual has moved. This page is now at <a href="{url}">{url}</a>.</p>
</body>
</html>
"""

NOT_FOUND = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Moved to {base}</title>
<meta name="robots" content="noindex">
<script>
  var rest = location.pathname.replace(/^{old_re}/, '');
  location.replace({base_js} + rest + location.search + location.hash);
</script>
</head>
<body>
<p>The DynEarthSol manual has moved to <a href="{base}">{base}</a>.</p>
</body>
</html>
"""


def new_url(base: str, rel: Path) -> str:
    """URL of a built page under the new base (trailingSlash: false)."""
    parts = rel.as_posix()
    if parts == 'index.html':
        return base
    if parts.endswith('/index.html'):
        return base + parts[: -len('index.html')]
    return base + parts[: -len('.html')]


def page(url: str) -> str:
    return PAGE.format(url=html.escape(url, quote=True), url_js=json.dumps(url))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    ap.add_argument('build', type=Path, help='output of yarn build')
    ap.add_argument('out', type=Path, help='directory to write the redirect site to')
    ap.add_argument('--new-base', required=True, help='new site root, with trailing slash')
    ap.add_argument('--old-base', required=True, help='old path prefix, e.g. /des3d/')
    ap.add_argument('--copy', action='append', default=[],
                    help='directory under build/ to copy verbatim (repeatable)')
    args = ap.parse_args()

    base = args.new_base if args.new_base.endswith('/') else args.new_base + '/'
    old = '/' + args.old_base.strip('/') + '/'

    if args.out.exists():
        shutil.rmtree(args.out)
    args.out.mkdir(parents=True)

    # Copied directories first: files in them, HTML included, are kept as is.
    for name in args.copy:
        src = args.build / name
        if not src.is_dir():
            raise SystemExit(f'--copy {name}: {src} is not a directory')
        shutil.copytree(src, args.out / name)
    copied = tuple(name.strip('/') + '/' for name in args.copy)

    count = 0
    for src in sorted(args.build.rglob('*.html')):
        rel = src.relative_to(args.build)
        if rel.as_posix() == '404.html' or rel.as_posix().startswith(copied):
            continue
        dst = args.out / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(page(new_url(base, rel)), encoding='utf-8')
        count += 1

    old_re = old.replace('/', r'\/').rstrip('\\/') + r'\/?'
    (args.out / '404.html').write_text(
        NOT_FOUND.format(base=html.escape(base, quote=True),
                         base_js=json.dumps(base), old_re=old_re),
        encoding='utf-8')
    (args.out / '.nojekyll').write_text('', encoding='utf-8')

    if count == 0:
        raise SystemExit(f'no HTML pages found under {args.build}')
    print(f'{count} redirect pages, 404 fallback to {base}, copied: {", ".join(args.copy) or "nothing"}')


if __name__ == '__main__':
    main()
