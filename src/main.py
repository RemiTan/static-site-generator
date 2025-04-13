import os
import shutil
import sys

from blocks import markdown_to_html_node


def reset_public_folder():
    shutil.rmtree("docs/")
    shutil.copytree("static/", "docs/")


def extract_title(markdown):
    lines = markdown.split("\n")
    title = lines[0]
    if not title.startswith("# "):
        raise Exception("No header")

    title = title[2:].strip()
    return title


def generate_page(base_path, from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as from_file:
        content_from_file = "".join(from_file.readlines())

    with open(template_path, "r") as template_file:
        content_template = "".join(template_file.readlines())

    html_node = markdown_to_html_node(content_from_file)
    html = html_node.to_html()
    title = extract_title(content_from_file)

    content = content_template.replace("{{ Title }}", title)
    content = content.replace("{{ Content }}", html)

    content = content.replace('href="/', f'href="{base_path}')
    content = content.replace('src="/', f'src="{base_path}')

    current_folder = ""
    for folder in dest_path.split("/")[:-1]:
        current_folder = os.path.join(current_folder, folder)
        if not os.path.isdir(current_folder):
            os.mkdir(current_folder)

    with open(dest_path, "w") as dest_file:
        dest_file.write(content)


def generate_pages_recursive(base_path, dir_path_content, template_path, dest_dir_path):
    objs = os.listdir(dir_path_content)
    for obj in objs:
        from_path_obj = os.path.join(dir_path_content, obj)
        dest_path_obj = os.path.join(dest_dir_path, obj)
        if os.path.isfile(from_path_obj):
            dest_path_obj = dest_path_obj.replace(".md", ".html")
            generate_page(
                base_path,
                from_path_obj,
                template_path,
                dest_path_obj,
            )
        else:
            generate_pages_recursive(
                base_path,
                from_path_obj,
                template_path,
                dest_path_obj,
            )


def main():
    reset_public_folder()
    arg = sys.argv[0]
    base_path = arg if arg != "" else "/"
    generate_pages_recursive(base_path, "./content/", "./template.html", "./docs/")


main()
