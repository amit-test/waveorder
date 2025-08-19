import os
import re

def fix_markdown_links(html_file):
    with open(html_file, 'r+') as f:
        content = f.read()
        # Example: Replace relative paths that point to .md with .html
        content = re.sub(r'(href=\".*?).md', r'\1.html', content)
        # Example: Replace relative paths that point to -- with - for html targets
        content = re.sub(r'(?<=[\w])--(?=[\w])', r'-', content)
        f.seek(0)
        f.write(content)
        f.truncate()

if __name__ == "__main__":
    output_dir = os.environ.get("READTHEDOCS_OUTPUT", "_build/html")
    for root, _, files in os.walk(output_dir):
        for file in files:
            if file.endswith(".html"):
                fix_markdown_links(os.path.join(root, file))
