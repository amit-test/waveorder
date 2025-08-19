import os
import re
import requests

ultimate_replacements = [
        ["https://github.com/user-attachments/assets/a0a8bffb-bf81-4401-9ace-3b4955436b57", "<video src=\"_static/videos/parts.mp4\" controls autoplay></video>", "parts.mp4"],
    ]

def fix_markdown_links(html_file):
    with open(html_file, 'r+') as f:
        content = f.read()
        # Example: Replace relative paths that point to .md with .html
        content = re.sub(r'(href=\".*?).md', r'\1.html', content)
        # Example: Replace relative paths that point to -- with - for html targets
        content = re.sub(r'(?<=[\w])--(?=[\w])', r'-', content)
        # Replace : ultimate_replacements
        content = replace_github_videos(content)
        f.seek(0)
        f.write(content)
        f.truncate()

def replace_github_videos(source:str):
    for replacements in ultimate_replacements:
        content = source.replace(replacements[0], replacements[1])
        download_video(replacements[0], replacements[2])
    return content

def download_video(src_url, filename):    
    output_dir = os.environ.get("READTHEDOCS_OUTPUT", "_build/html/_static/videos/")
    resp = requests.get(src_url) # making requests to server
    with open(os.path.join(output_dir,filename), "wb") as f: # opening a file handler to create new file 
        f.write(resp.content) # writing content to file

if __name__ == "__main__":
    output_dir = os.environ.get("READTHEDOCS_OUTPUT", "_build/html")
    for root, _, files in os.walk(output_dir):
        for file in files:
            if file.endswith(".html"):
                fix_markdown_links(os.path.join(root, file))
