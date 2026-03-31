from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from files import copy_tree_to_tree, generate_pages_recursive

def main():
    copy_tree_to_tree ("static", "public")
    generate_pages_recursive("content", "template.html", "public")

main()