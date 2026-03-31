from markdowns import BlockType, markdown_to_blocks, block_to_block_type
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType,text_node_to_html_node
from node_delimiter import text_to_textnodes


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        match (block_to_block_type(block)):
            case BlockType.PARAGRAPH :                     
                inner_text = extract_paragraph_text(block)
                children = text_to_children(inner_text)                            
                html_nodes.append(ParentNode(tag='p', children=children))

            case BlockType.HEADING :
                inner_text =  extract_heading_text(block)
                children = text_to_children(inner_text) 
                html_nodes.append(ParentNode(tag=tag_for_heading(block), children=children))  

            case BlockType.CODE :
                inner_text = extract_code_text(block)
                leaf = LeafNode(tag="code", value=inner_text)
                html_nodes.append(ParentNode(tag='pre', children=[leaf]))     

            case BlockType.QUOTE :
                inner_text = extract_quote_text(block)
                children = text_to_children(inner_text) 
                html_nodes.append(ParentNode(tag='blockquote', children=children))        
                 
            case BlockType.UNORDERED_LIST :
                item_texts = extract_list_text(block)
                inner_parents = []
                for item_text in item_texts:
                    children = text_to_children(item_text)
                    inner_parents.append(ParentNode(tag='li', children=children))
                html_nodes.append(ParentNode(tag='ul', children=inner_parents))  

            case BlockType.ORDERED_LIST :
                item_texts = extract_list_text(block)
                inner_parents = []
                for item_text in item_texts:
                    children = text_to_children(item_text)
                    inner_parents.append(ParentNode(tag='li', children=children))
                html_nodes.append(ParentNode(tag='ol', children=inner_parents))
            case _:
                pass
    return ParentNode('div',html_nodes)

def text_to_children(text):
    html_nodes = []
    text_nodes = text_to_textnodes(text)
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))
    return html_nodes

def extract_paragraph_text(text):
    return text.replace("\n", " ")

def extract_heading_text(text):
    for i in range(6):
        if text[i] != "#":
            return text[i+1:]
    return text[7:]

def tag_for_heading(text):
    level = 0
    for char in text:
        if char == "#":
            level += 1
        else:
            break
    return f"h{level}"

def extract_code_text(text):
    return text[4:-3]

def extract_quote_text(text):
    lines = text.split("\n")
    new_line = ""
    for line in lines:
        new_line += line[1:].strip()
    return new_line

def extract_list_text(text): # return list of text for each line
    lines = text.split("\n")
    new_lines = []
    for line in lines:
        item = line.split(" ", 1)
        new_lines.append(item[1])
    return new_lines
