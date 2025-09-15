from functions.file_handler import copy_files
from functions.markdown_to_html import generate_pages_recursive

def main():

    src = "/Users/derekball/Library/Mobile Documents/com~apple~CloudDocs/Mailbox Cloud Drive/OX Drive/My files.localized/Programming/git/py-boot-site/static"
    dest = "/Users/derekball/Library/Mobile Documents/com~apple~CloudDocs/Mailbox Cloud Drive/OX Drive/My files.localized/Programming/git/py-boot-site/public"
    template_html = "/Users/derekball/Library/Mobile Documents/com~apple~CloudDocs/Mailbox Cloud Drive/OX Drive/My files.localized/Programming/git/py-boot-site/template.html"
    content_dir = "/Users/derekball/Library/Mobile Documents/com~apple~CloudDocs/Mailbox Cloud Drive/OX Drive/My files.localized/Programming/git/py-boot-site/content"
    copy_files(src, dest)
    generate_pages_recursive(content_dir, template_html, f"{dest}")
    
if __name__ == "__main__":
    main()