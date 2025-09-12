from textnode import TextType, TextNode, TextTypeSyntax

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
        else:
            parts = node.text.split(delimiter)
            #print(len(parts))
            new_parts = []
            for i in range(len(parts)):
                if i % 2 == 0:
                    new_parts.append(TextNode(parts[i], TextType.PLAIN))
                else:
                    new_parts.append(TextNode(parts[i], text_type))
            new_nodes.extend(new_parts)
    return new_nodes

def split_nested_delimiter(old_nodes: list[TextNode], outer_text_type = TextType.PLAIN):
    new_nodes = []
    for node in old_nodes:
        print(f"-----> Current Node: {node}")
        delimiter = get_outer_delimiter(node)
        print(f"----> Delimiter: {delimiter}")
        if delimiter is None:
            new_nodes.append(node)
        else:      
            if delimiter is None:
                new_nodes.append(node)
            else:
                text_type = TextType.PLAIN
                match delimiter:
                    case TextTypeSyntax.BOLD:
                        text_type = TextType.BOLD
                    case TextTypeSyntax.ITALIC:
                        text_type = TextType.ITALIC
                    case TextTypeSyntax.CODE:
                        text_type = TextType.CODE
                parts = node.text.split(delimiter)
                #print(f"-----> Text type: {text_type}")
                #print(f"-----> Parts: {parts}")
                new_parts = []
                for i in range(len(parts)):
                    if i % 2 == 0: #Represents a block before/after a split element
                        new_parts.append(TextNode(parts[i], outer_text_type))
                    else: #Represent an element within the delimiter
                        text_node = TextNode(parts[i], text_type)
                        nested_nodes = split_nested_delimiter([text_node], text_type)
                        new_parts.append(nested_nodes)
                new_nodes.extend(new_parts)
    return new_nodes

        

def get_outer_delimiter(node: TextNode):
    first_index = None
    first_delim = None

    for delim in TextTypeSyntax.ALL_OPTIONS:
        index = node.text.find(delim)
        if index != -1:
            if first_index is None or index < first_index:
                first_index = index
                first_delim = delim
    
    return first_delim