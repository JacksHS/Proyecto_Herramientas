import os
import re
from datetime import datetime


def count_lines(filepath):
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        return len(f.readlines())


def count_car_listings(html_path):
    with open(html_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    return len(re.findall(r'<div class="auto">', content))


def collect_stats():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    extensions = {".html": 0, ".css": 0}
    file_count = 0
    total_lines = 0
    files_detail = []

    for dirpath, _, filenames in os.walk(root):
        if ".git" in dirpath:
            continue
        for f in filenames:
            ext = os.path.splitext(f)[1].lower()
            if ext in extensions:
                fp = os.path.join(dirpath, f)
                lines = count_lines(fp)
                total_lines += lines
                file_count += 1
                rel = os.path.relpath(fp, root)
                files_detail.append((rel, lines))
                extensions[ext] += 1

    index_path = os.path.join(root, "index.html")
    car_count = count_car_listings(index_path) if os.path.exists(index_path) else 0

    return {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_files": file_count,
        "total_lines": total_lines,
        "html_files": extensions[".html"],
        "css_files": extensions[".css"],
        "car_listings": car_count,
        "files": files_detail,
    }


def generate_report(stats):
    lines = []
    lines.append("# Estadísticas del Proyecto - AutoMarket Perú\n")
    lines.append(f"**Generado:** {stats['date']}\n")
    lines.append("---\n")
    lines.append("## Resumen\n")
    lines.append(f"- Total de archivos: **{stats['total_files']}**")
    lines.append(f"- Total de líneas de código: **{stats['total_lines']}**")
    lines.append(f"- Archivos HTML: **{stats['html_files']}**")
    lines.append(f"- Archivos CSS: **{stats['css_files']}**")
    lines.append(f"- Autos listados: **{stats['car_listings']}**\n")
    lines.append("---\n")
    lines.append("## Detalle por archivo\n")
    lines.append("| Archivo | Líneas |")
    lines.append("|--------|-------|")
    for rel, count in sorted(stats["files"]):
        lines.append(f"| {rel} | {count} |")
    lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    stats = collect_stats()
    report = generate_report(stats)
    out_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "stats.md"
    )
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(report)
    print("Stats generated successfully:")
    print(f"  Files: {stats['total_files']}")
    print(f"  Lines: {stats['total_lines']}")
    print(f"  Cars:  {stats['car_listings']}")
