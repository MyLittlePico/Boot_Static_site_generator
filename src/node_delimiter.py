from textnode import TextNode, TextType
from extract_markdown import extract_markdown_links, extract_markdown_images

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT: 
            new_nodes.append(node)
            continue
        splitted = node.text.split(delimiter)
        if len(splitted)% 2 == 0: 
            raise Exception("No matched delimiter found")
        
        for i in range(len(splitted)):
            if splitted[i] == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(splitted[i],TextType.TEXT))
            else :
                new_nodes.append(TextNode(splitted[i],text_type))
    
    return new_nodes

# example : This is a paragraph with a ![Description of image](url/of/image.jpg)
def split_nodes_image(old_nodes):
    new_nodes = []
    for node in  old_nodes:
        if node.text_type != TextType.TEXT: 
            new_nodes.append(node)
            continue
        matches = extract_markdown_images(node.text)
        match_count = len(matches)
        current_text = node.text
        for i in range(match_count):
            sections = current_text.split(f"![{matches[i][0]}]({matches[i][1]})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0],TextType.TEXT)) # append text 
            new_nodes.append (TextNode(matches[i][0], TextType.IMAGE, url = matches[i][1] )) # append url
            current_text = sections[1]
        if current_text != "" :
            new_nodes.append(TextNode(current_text,TextType.TEXT))
    return new_nodes
            

# example : This is a paragraph with a [link](https://www.google.com).
def split_nodes_link(old_nodes):
    new_nodes = []
    for node in  old_nodes:
        if node.text_type != TextType.TEXT: 
            new_nodes.append(node)
            continue
        matches = extract_markdown_links(node.text)
        match_count = len(matches)
        current_text = node.text
        for i in range(match_count):
            sections = current_text.split(f"[{matches[i][0]}]({matches[i][1]})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0],TextType.TEXT)) # append text 
            new_nodes.append (TextNode(matches[i][0], TextType.LINK, url = matches[i][1] )) # append url
            current_text = sections[1]
        if current_text != "" :
            new_nodes.append(TextNode(current_text,TextType.TEXT))

    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes,'**',TextType.BOLD)
    nodes = split_nodes_delimiter(nodes,'_',TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes,'`',TextType.CODE)

    return nodes

