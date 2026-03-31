from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from files import copy_tree_to_tree, generate_pages_recursive
import sys

def main():

    if len(sys.argv) >= 2:
        basepath = sys.argv[1]
    else :
        basepath = "/"

    copy_tree_to_tree ("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath )

main()