import re
import datetime
import os
from collections import Counter

LOG_REGEX = """(?P<ip>\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3})?(?P<ip2>, \\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3})?-? - ?\\S* \\[(?P<timestamp>\\d{2}\\/\\w{3}\\/\\d{4}:\\d{2}:\\d{2}:\\d{2} (\\+|\\-)\\d{4})\\]\\s+\"(?P<method>\\S{3,10}) (?P<path>\\S+) HTTP\\/1\\.\\d" (?P<response_status>\\d{3}) (?P<bytes>\\d+) "(?P<referer>(\\-)|(.+))?" "(?P<useragent>.+)"""
regex = re.compile(LOG_REGEX)
PAGE_HTML = """
<!doctype html>
<html lang="fr">
<head>
    <meta name="robots" content="noindex">
    <meta charset="utf-8">
    <title>Oxfam - compteur d'entrées sur l'impact des banques</title>
    <style>td,th{border: 1px solid black; padding: 5px}</style>

</head>
<body>
    <div style="margin: auto; max-width: 400px">
        <table style="border-collapse: collapse">
            <tbody>
                <tr>
                    <th>Nombre de visites sur la page</th>
                    <td>__VISITS__</td>
                </tr>
            <tbody>
                <tr>
                    <th>Nombre de visiteurs uniques sur la page</th>
                    <td>__UNIQUE_VISITS__</td>
                </tr>
            <tbody>
                <tr>
                    <th>Nombre de calculs effectués</th>
                    <td>__ENTRIES__</td>
                </tr>
            <tbody>
                <tr>
                    <th>Nombre de visiteurs qui ont effectué un calcul</th>
                    <td>__UNIQUE_ENTRIES__</td>
                </tr>
            </tbody>
        </table>
    </div>
    <div style="margin: auto; max-width: 400px; margin-top: 30px">
        Mis à jour: __UPDATED_AT__
    </div>
</body>
</html>
"""


def match_line(line):
    match = regex.match(line)
    if match:
        match = match.groupdict()
    return match


def iterate_file(file_path):
    with open(file_path, "r") as fh:
        for line in fh:
            match = match_line(line)
            if not line:
                continue
            yield match


def iterate_files():
    for file in os.listdir("{{ logs_base_path }}"):
        file_path = os.path.join("{{ logs_base_path }}", file)
        if not os.path.isfile(file_path) or not file.startswith(
            "access_impact_banques.log"
        ):
            continue
        print("parsing file", file_path)
        for line in iterate_file(file_path):
            yield line


def build_data():
    home_counter = Counter()
    entry_counter = Counter()
    for line in iterate_files():
        if not line:
            continue
        if line["path"] == "/entry":
            entry_counter[line["ip"]] += 1
        elif line["path"] == "/":
            home_counter[line["ip"]] += 1
    return {
        "unique_visits": len(home_counter),
        "visits": sum(home_counter.values()),
        "unique_entries": len(entry_counter),
        "entries": sum(entry_counter.values()),
        "updated_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


def generate_statistic_page():
    data = build_data()
    page_html = PAGE_HTML
    for key, value in data.items():
        page_html = page_html.replace(f"__{key.upper()}__", str(value))
    target_path = os.environ["STATISTIC_PAGE_PATH"]
    with open(target_path, "w") as f:
        f.write(page_html)


if __name__ == "__main__":
    generate_statistic_page()
