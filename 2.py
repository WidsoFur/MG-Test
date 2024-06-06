import re

urls = [
    "http://server.com/downloads/life_changing_plans.pdf",
    "http://server.com/downl/life_changing_plans.doc",
    "https://server-dot.com/root.pdf"
]
#имя файла с любым расширением, идущим после последнего слэша и до конца строки.
pattern = re.compile(r'/([^/]+\.[^/]+)$')

for url in urls:
    match = pattern.search(url)
    if match:
        print(match.group(1))
