import os
import shutil
from markdown_to_html import markdown_to_html_node
from markdowns import extract_title

def copy_tree_to_tree (src_dir, dest_dir):
    if not os.path.exists(src_dir):
        print(f"directory {src_dir} not exist")
        return
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
        print(f"Removing old directory {dest_dir}")
    print(f"Creating new {dest_dir} directory...")
    os.mkdir(dest_dir)
    copy_items (src_dir, dest_dir)

def copy_items (src_dir, dest_dir):
    src_items = os.listdir(src_dir)
    for item in src_items:
        item_path = os.path.join(src_dir, item)
        if os.path.isfile(item_path):
            shutil.copy(item_path, dest_dir)
            print(f"copy {item_path} to {dest_dir}")
        else :
            dest_path = os.path.join(dest_dir,item)
            print(f"Creating {dest_path}")
            os.mkdir(dest_path)
            copy_items (item_path, dest_path)


def generate_page(from_path, template_path, dest_path, basepath ):
    print (f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown = ""
    template = ""

    with open(from_path) as file:
        markdown = file.read()
    with open(template_path) as file:
        template = file.read()
    
    htmlnodes = markdown_to_html_node(markdown)
    html_text = htmlnodes.to_html()
    title = extract_title(markdown)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_text)
    template = template.replace("href=\"/", f"href=\"{basepath}")
    template = template.replace("src=\"/", f"src=\"{basepath}")

    write_text_to_dir(template,dest_path)

def write_text_to_dir(text, dest_path):

    os.makedirs(os.path.dirname(dest_path), exist_ok = True)
    with open(dest_path, "w") as file:
        file.write(text)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath ):
    items = os.listdir(dir_path_content)
    for item in items:
        item_path = os.path.join(dir_path_content,item)
        if os.path.isdir(item_path):
            new_dest_path = os.path.join(dest_dir_path, item)
            generate_pages_recursive(item_path, template_path, new_dest_path, basepath )
        elif item.endswith(".md"):
            html_item = item.replace(".md",".html")
            new_dest_path = os.path.join(dest_dir_path, html_item)
            generate_page(item_path, template_path, new_dest_path, basepath )
