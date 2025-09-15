from functions.file_handler import copy_files
from functions.markdown_to_html import generate_pages_recursive
import sys

def main():
    if sys.argv is not None and len(sys.argv) > 0:
        base_path = sys.argv[1]
    else:
        base_path = "/"
    print(base_path)
    src = "/Users/derekball/Library/Mobile Documents/com~apple~CloudDocs/Mailbox Cloud Drive/OX Drive/My files.localized/Programming/git/py-boot-site/static"
    dest = "/Users/derekball/Library/Mobile Documents/com~apple~CloudDocs/Mailbox Cloud Drive/OX Drive/My files.localized/Programming/git/py-boot-site/public"
    template_html = "/Users/derekball/Library/Mobile Documents/com~apple~CloudDocs/Mailbox Cloud Drive/OX Drive/My files.localized/Programming/git/py-boot-site/template.html"
    content_dir = "/Users/derekball/Library/Mobile Documents/com~apple~CloudDocs/Mailbox Cloud Drive/OX Drive/My files.localized/Programming/git/py-boot-site/content"
    copy_files(src, dest)
    generate_pages_recursive(content_dir, template_html, dest, base_path)
    
if __name__ == "__main__":
    main()