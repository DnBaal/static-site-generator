from textnode import TextNode, TextType


def main():
    node = TextNode("Hello", TextType.LINK, "http://example.com")
    print(node)


if __name__ == "__main__":
    main()
