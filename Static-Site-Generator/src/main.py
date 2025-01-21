from textnode import TextNode, TextType
from os import listdir, path, mkdir, makedirs
import shutil
from make_html_doc import markdown_to_html_node
from markdown import extract_title

## dangerous
def copy_dir(source, destination):
    print(f"Trying to copy from {source} to {destination}...")
    if "..\\" in destination:
        raise Exception("Are you sure you're allowed to do that?")
    
    if path.exists(destination):
        shutil.rmtree(destination)
    mkdir(destination)

    # use recursion for every nested directory
    for dir in listdir(source):
        if not path.isfile(path.join(source, dir)):
            copy_dir(path.join(source, dir), path.join(destination, dir))
        else:
            shutil.copy(path.join(source, dir), destination)

    print(f"...finished copying from {source} to {destination}.")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    ##get necessary data
    content, template = "", ""
    with open(from_path, "r") as file:
        content = file.read()

    with open(template_path, "r") as file:
        template = file.read()

    title = extract_title(content)
    content = markdown_to_html_node(content).to_html()   

    ## fill in content
    template = template.replace("{{ Title }}", title).replace("{{ Content }}", content)

    ## ave finished file
    makedirs(path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(template)
    
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for dir in listdir(dir_path_content):
        if not path.isfile(path.join(dir_path_content, dir)):
            generate_pages_recursive(path.join(dir_path_content, dir), template_path, path.join(dest_dir_path, dir))
        else:
            if dir.endswith(".md"):
                generate_page(path.join(dir_path_content, dir), template_path, path.join(dest_dir_path, dir.replace(".md", ".html")))


def main():
    testNode = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    print(testNode)

    copy_dir("static", "public")

    #generate_page("content/index.md", "template.html", "public/index.html")
    generate_pages_recursive("content", "template.html", "public")

main()