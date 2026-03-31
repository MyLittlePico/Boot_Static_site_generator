import unittest
from markdowns import markdown_to_blocks, block_to_block_type
from markdowns import BlockType

class TestMarkdown_To_Blocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


class TestBlock_To_Block_Type(unittest.TestCase):
    def test_block_to_block_type_0(self):
        block = """# Heading 1"""
        type =  block_to_block_type(block)
        self.assertEqual(type, BlockType.HEADING)
    
    def test_block_to_block_type_1(self):
        block = """###### Heading 6"""
        type =  block_to_block_type(block)
        self.assertEqual(type, BlockType.HEADING)

    def test_block_to_block_type_2(self):
        block = """####### NOT Heading 7"""
        type =  block_to_block_type(block)
        self.assertEqual(type, BlockType.PARAGRAPH)
    
    def test_block_to_block_type_3(self):
        block = """# Heading 1
## Heading 2
### Heading 3"""
        type =  block_to_block_type(block)
        self.assertEqual(type, BlockType.PARAGRAPH)

    def test_block_to_block_type_4(self):
        block = """```
This is code
```"""
        type =  block_to_block_type(block)
        self.assertEqual(type, BlockType.CODE)
        
    def test_block_to_block_type_5(self):
        block = """```
This is not code
`"""
        type =  block_to_block_type(block)
        self.assertEqual(type, BlockType.PARAGRAPH)
    
    def test_block_to_block_type_6(self):
        block = """> This is a quote.
> This is a quote.
> This is a quote."""
        type =  block_to_block_type(block)
        self.assertEqual(type, BlockType.QUOTE)
    
    def test_block_to_block_type_7(self):
        block = """> This is not quote.
  This is not quote.
> This is not quote."""
        type =  block_to_block_type(block)
        self.assertEqual(type, BlockType.PARAGRAPH)

    def test_block_to_block_type_8(self):
        block = """- Item 1
- Item 2
- Item 3"""
        type =  block_to_block_type(block)
        self.assertEqual(type, BlockType.UNORDERED_LIST)

    def test_block_to_block_type_9(self):
        block = """1. Item 1
2. Item 2
3. Item 3"""
        type =  block_to_block_type(block)
        self.assertEqual(type, BlockType.ORDERED_LIST)