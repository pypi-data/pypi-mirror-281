from parsel import Selector

__all__ = [
    "bs_get_text",
    "bs_get_text2",
    "bs_html",
    "html2md",
    "Selector",
]

NON_BREAKING_ELEMENTS = [
    "a",
    "abbr",
    "acronym",
    "audio",
    "b",
    "bdi",
    "bdo",
    "big",
    "button",
    "canvas",
    "cite",
    "code",
    "data",
    "datalist",
    "del",
    "dfn",
    "em",
    "embed",
    "font",
    "i",
    "iframe",
    "img",
    "input",
    "ins",
    "kbd",
    "label",
    "map",
    "mark",
    "meter",
    "noscript",
    "object",
    "output",
    "picture",
    "progress",
    "q",
    "ruby",
    "s",
    "samp",
    "script",
    "select",
    "slot",
    "small",
    "span",
    "strong",
    "sub",
    "sup",
    "svg",
    "template",
    "textarea",
    "time",
    "u",
    "tt",
    "var",
    "video",
    "wbr",
]
BLOCK_TAGS = [
    "p",
    "div",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "ul",
    "ol",
    "li",
    "table",
    "tr",
    "thead",
    "tbody",
    "tfoot",
    "form",
]


def bs_html(
    markup: str = "",
    features: str = "lxml",
    builder=None,
    parse_only=None,
    from_encoding=None,
    exclude_encodings=None,
    element_classes=None,
):
    """
    使用 BeautifulSoup 解析网页

    markup: 网页源码
    features: 默认使用 lxml 解析
    """
    from bs4 import BeautifulSoup

    return BeautifulSoup(
        markup=markup,
        features=features,
        builder=builder,
        parse_only=parse_only,
        from_encoding=from_encoding,
        exclude_encodings=exclude_encodings,
        element_classes=element_classes,
    )


def bs_get_text(
    soup,
    strip_tags: list = ["style", "script"],
) -> str:
    """
    基于 BeautifulSoup 提取网页文本v1

    soup: BeautifulSoup 对象或html文本
    strip_tags: 需要删除的节点
    """
    import re

    if isinstance(soup, str):
        soup = bs_html(soup)
    if strip_tags:
        for node in soup(strip_tags):
            node.extract()
    for node in soup.find_all():
        if node.name not in NON_BREAKING_ELEMENTS:
            node.append("\n") if node.name == "br" else node.append("\n\n")
    return re.sub(
        "\n\n+",
        "\n\n",
        soup.get_text().strip().replace("\xa0", " ").replace("\u3000", " "),
    )


def bs_get_text2(
    soup,
    strip_tags: list = ["style", "script"],
):
    """
    基于 BeautifulSoup 提取网页文本v2

    soup: BeautifulSoup 对象或html文本
    """
    from bs4 import element
    import re

    if isinstance(soup, str):
        soup = bs_html(soup)
    if strip_tags:
        for node in soup(strip_tags):
            node.extract()

    def traverse(node):
        if isinstance(node, element.NavigableString):
            if node.strip():
                yield node.strip()
        else:
            if node.name in BLOCK_TAGS:
                yield "\n"
            for child in node.children:
                yield from traverse(child)
            if node.name in BLOCK_TAGS:
                yield "\n"

    return re.sub(
        "\n\n+",
        "\n\n",
        "".join(traverse(soup)).strip().replace("\xa0", " ").replace("\u3000", " "),
    )


def html2md(
    string: str,
    baseurl: str = "",
    ignore_links: bool = True,
    ignore_images: bool = True,
    ignore_tables: bool = True,
) -> str:
    """
    ## HTML 转 Markdown

    默认忽略链接、忽略图像、忽略表格
    """
    import html2text
    import re

    converter = html2text.HTML2Text(baseurl=baseurl)
    converter.ignore_links = ignore_links  # 忽略链接
    converter.ignore_images = ignore_images  # 忽略图像
    converter.ignore_tables = ignore_tables  # 忽略表格
    if ignore_tables:
        string = re.sub("<table.*?</table>", "", string)
    content = converter.handle(string)
    return content
