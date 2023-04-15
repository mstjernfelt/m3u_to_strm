from flask import Flask, render_template, request, redirect, url_for
import os
import re

app = Flask(__name__)

def parse_m3u(file_path):
    content = open(file_path, 'r').read()
    matches = re.finditer(r'#EXTINF:(-?\d+),(.+)\n(.+)', content)
    items = []
    for match in matches:
        item = {
            'duration': int(match.group(1)),
            'title': match.group(2),
            'url': match.group(3)
        }
        items.append(item)
    return items

def write_m3u_file(file_path, items):
    with open(file_path, 'w') as f:
        f.write('#EXTM3U\n')
        for item in items:
            f.write(f"#EXTINF:{item['duration']},{item['title']}\n")
            f.write(f"{item['url']}\n")

def get_groups(items):
    groups = set()
    for item in items:
        group_match = re.search(r'group-title="([^"]+)"', item['title'])
        if group_match:
            groups.add(group_match.group(1))
    return sorted(groups)

#@app.route("/", methods=["GET", "POST"])
@app.route("/")
def index():
    print('test')

    if request.method == "POST":
        items = []
        for title, url in zip(request.form.getlist('title'), request.form.getlist('url')):
            duration = -1
            items.append({'duration': duration, 'title': title, 'url': url})
        write_m3u_file("C:/BrightCom/GitHub/mstjernfelt/m3u_to_strm/.local/Monsteriptv/output_playlist.m3u", items)
        return redirect(url_for("index"))

    items = parse_m3u("C:/BrightCom/GitHub/mstjernfelt/m3u_to_strm/.local/Monsteriptv\playlist.m3u")
    groups = get_groups(items)
    selected_group = request.args.get("group")

    if selected_group:
        items = [item for item in items if f'group-title="{selected_group}"' in item['title']]

    return render_template("index.html", items=items, groups=groups, selected_group=selected_group)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5050)))
