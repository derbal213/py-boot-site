import unittest
from functions.block import markdown_to_blocks, block_to_block_type, BlockType

class TestBlock(unittest.TestCase):
    test_md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""

    block_md ="""
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

### This is a header
#on two lines?

```This is a code block
across two lines```

1. This is an ordered list
2. With multiple items

- This is an unordered list
- with items

>This is a quote
>That goes onto two lines
>-Michael Scott
"""

    def test_markdown_to_blocks(self):
        blocks = markdown_to_blocks(self.test_md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_block_to_block_type_all(self):
        blocks = markdown_to_blocks(self.block_md)
        expected_types = [BlockType.PARAGRAPH, BlockType.PARAGRAPH, BlockType.HEADING, BlockType.CODE, BlockType.ORDERED_LIST, BlockType.UNORDERED_LIST, BlockType.QUOTE]
        self.assertListEqual(expected_types,
            list(map(block_to_block_type, blocks)))
        # for i in range(len(blocks)):
        #     actual = block_to_block_type(blocks[i])
        #     expected = expected_types[i]
        #     self.assertEqual(expected, actual)

    def test_block_to_block_type_none(self):
        blocks = markdown_to_blocks("This has only a single block")
        self.assertEqual(1, len(blocks))

        actual = block_to_block_type(blocks[0])
        self.assertEqual(BlockType.PARAGRAPH, actual)

    def test_block_type_heading_too_many(self):
        blocks = markdown_to_blocks("####### This header has too many #s")
        self.assertEqual(1, len(blocks))

        actual = block_to_block_type(blocks[0])
        self.assertEqual(BlockType.PARAGRAPH, actual)

    def test_block_type_heading_no_space(self):
        blocks = markdown_to_blocks("###This header forgot a space")
        self.assertEqual(1, len(blocks))

        actual = block_to_block_type(blocks[0])
        self.assertEqual(BlockType.PARAGRAPH, actual)

    def test_valid_code_single_line(self):
        blocks = markdown_to_blocks("```This is a single line code block```")
        self.assertEqual(1, len(blocks))

        actual = block_to_block_type(blocks[0])
        self.assertEqual(BlockType.CODE, actual)

    def test_code_missing_end(self):
        blocks = markdown_to_blocks("```This code block forgot its end tag")
        self.assertEqual(1, len(blocks))

        actual = block_to_block_type(blocks[0])
        self.assertEqual(BlockType.PARAGRAPH, actual)

    def test_unordered_missing_second_line_dash(self):
        blocks = markdown_to_blocks("- This is line one\nThis is line two")
        self.assertEqual(1, len(blocks))

        actual = block_to_block_type(blocks[0])
        self.assertEqual(BlockType.PARAGRAPH, actual)

    def test_unordered_missing_space(self):
        blocks = markdown_to_blocks("- This is line one\n-This is line 2")
        self.assertEqual(1, len(blocks))

        actual = block_to_block_type(blocks[0])
        self.assertEqual(BlockType.PARAGRAPH, actual)

    def test_ordered_missing_space(self):
        blocks = markdown_to_blocks("1. This is line one\n2.This is line 2")
        self.assertEqual(1, len(blocks))

        actual = block_to_block_type(blocks[0])
        self.assertEqual(BlockType.PARAGRAPH, actual)

    def test_ordered_missing_num(self):
        blocks = markdown_to_blocks("1. This is line one\n3. This is line 2")
        self.assertEqual(1, len(blocks))

        actual = block_to_block_type(blocks[0])
        self.assertEqual(BlockType.PARAGRAPH, actual)

    def test_ordered_one_mixed(self):
        blocks = markdown_to_blocks("1. This is line one 2. This is just a two with a period\n2. This is line 2")
        self.assertEqual(1, len(blocks))

        actual = block_to_block_type(blocks[0])
        self.assertEqual(BlockType.ORDERED_LIST, actual)

    def test_ordered_two_on_first_line(self):
        blocks = markdown_to_blocks("1. This is line one 2. This is line 2\n3. This is line 3")
        self.assertEqual(1, len(blocks))

        actual = block_to_block_type(blocks[0])
        self.assertEqual(BlockType.PARAGRAPH, actual)

    def test_ordered_missing_period(self):
        blocks = markdown_to_blocks("1. This is line one\n2 This is line 2\n3. This is line 3")
        self.assertEqual(1, len(blocks))

        actual = block_to_block_type(blocks[0])
        self.assertEqual(BlockType.PARAGRAPH, actual)

    def test_quote_missing_second_line(self):
        blocks = markdown_to_blocks(">This is a quote across\nmultiple lines")
        self.assertEqual(1, len(blocks))
        
        actual = block_to_block_type(blocks[0])
        self.assertEqual(BlockType.PARAGRAPH, actual)

    def test_proper_multiline_quote(self):
        blocks = markdown_to_blocks(">This is a quote line one\n>And this is line two\n>And this is line three")
        self.assertEqual(1, len(blocks))
        actual = block_to_block_type(blocks[0])
        self.assertEqual(BlockType.QUOTE, actual)

