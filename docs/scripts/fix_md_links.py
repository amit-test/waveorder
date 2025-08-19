import os
import re
import requests

ultimate_replacements = [
        ["https://github.com/user-attachments/assets/a0a8bffb-bf81-4401-9ace-3b4955436b57", "<video src=\"_static/videos/parts.mp4\" controls autoplay></video>", "parts.mp4", False],
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
    pre = "<a class=\"github reference external\" href=\""
    post = "\">user-attachments/assets</a>"
    for replacements in ultimate_replacements:
        content = source.replace(pre+replacements[0]+post, replacements[1])
        if not replacements[3]:
            success = download_video(replacements[0], replacements[2])
            if success:
                replacements[3] = True
    return content

def download_video(src_url, filename):    
    output_dir = os.environ.get("READTHEDOCS_OUTPUT", "_build/html")
    resp = requests.get(src_url) # making requests to server
    full_mp4_path = os.path.join(output_dir, "html/_static/videos", filename)
    with open(full_mp4_path, "wb") as f: # opening a file handler to create new file 
        f.write(resp.content) # writing content to file
        print("File {src} downloaded to {dl}".format(src=src_url, dl=full_mp4_path))
        return True
    return False

if __name__ == "__main__":
    output_dir = os.environ.get("READTHEDOCS_OUTPUT", "_build/html")
    try:
        full_videos_path = os.path.join(output_dir, "html/_static/videos/")
        # Create the directory and any missing parent directories
        os.makedirs(full_videos_path, exist_ok=True)
        print(f"Directory '{full_videos_path}' created successfully.")
    except OSError as e:
        print(f"Error creating directory: {e}")

    for root, _, files in os.walk(output_dir):
        for file in files:
            if file.endswith(".html"):
                fix_markdown_links(os.path.join(root, file))
