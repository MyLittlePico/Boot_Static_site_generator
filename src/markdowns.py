from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    new_blocks = []
    for block in blocks:
        new_block = block.strip()
        if new_block != "":
            new_blocks.append(new_block)
    return new_blocks

def block_to_block_type(block):
    match block[0]:
        case "#":
            if len(block.split("\n")) != 1:
                return BlockType.PARAGRAPH
            for i in range(6):
                if block[i+1] == " " :
                    return BlockType.HEADING
                if block[i+1] != "#" :
                    return BlockType.PARAGRAPH
            return BlockType.PARAGRAPH
        case "`":
            if block[0:4] == "```\n" and block[-4:] == "\n```":
                return BlockType.CODE
            else :
                return BlockType.PARAGRAPH

        case ">":
            lines = block.split("\n")
            for line in lines:
                if line[0] != ">":
                    return BlockType.PARAGRAPH
            return BlockType.QUOTE

        case "-":
            lines = block.split("\n")
            for line in lines:
                if not line.startswith("- "):
                    return BlockType.PARAGRAPH
            return BlockType.UNORDERED_LIST            
        case "1":
            lines = block.split("\n")
            number = 1
            for line in lines:
                if not line.startswith(f"{number}. "):
                    return BlockType.PARAGRAPH
                number += 1
            return BlockType.ORDERED_LIST     
        case _:
            return BlockType.PARAGRAPH


def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block_to_block_type(block) == BlockType.HEADING:
            if block[0:2] == "# ":
                return block[2:]
    raise Exception("no title found")