from functions.file_handler import copy_files
from functions.markdown_to_html import generate_pages_recursive
import sys

def main() -> None:
    base_path = sys.argv[1] if sys.argv is not None and len(sys.argv) > 0 else "/"
    root: str = "/Users/derekball/Library/Mobile Documents/com~apple~CloudDocs/Mailbox Cloud Drive/OX Drive/My files.localized/Programming/git/py-boot-site"
    src: str = f"{root}/static"
    dest: str = f"{root}/docs"
    template_html: str = f"{root}/template.html"
    content_dir: str = f"{root}/content"
    copy_files(src, dest)
    generate_pages_recursive(content_dir, template_html, dest, base_path)
    
if __name__ == "__main__":
    main()