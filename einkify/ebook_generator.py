import os
import shutil
import tempfile
import re
import zipfile
from typing import List, Tuple
from uuid import uuid4
from datetime import datetime, timezone
from PIL import Image

from .image_processor import get_image_paths


def get_title(input_file: str) -> str:
    return os.path.splitext(os.path.basename(input_file))[0]


def create_cover(image_path: str, output_directory: str) -> str:
    cover_path = os.path.join(
        output_directory, f"cover{os.path.splitext(image_path)[1]}"
    )
    shutil.copy(image_path, cover_path)

    return cover_path


def copy_images(
    image_path_maps: List[Tuple[str, str]],
    image_directory: str,
    output_directory: str,
) -> None:
    new_image_paths = []
    for image_path_map in image_path_maps:
        image_path, flat_image_path = image_path_map

        new_image_path = os.path.join(output_directory, flat_image_path)
        shutil.copy(os.path.join(image_directory, image_path), new_image_path)

        new_image_paths.append(new_image_path)

    return new_image_paths


def write_file(output_path: str, lines: List[str]) -> None:
    with open(output_path, "w+", encoding="UTF-8") as stream:
        stream.writelines([f"{line}\n" for line in lines])


def map_paths(file_paths: List[str]) -> List[Tuple[str, str]]:
    file_path_maps = []
    for file_path in file_paths:
        file_path_maps.append(
            (
                file_path,
                re.sub(r"-+", "-", re.sub(r"[^\w\-_\.]", "-", file_path)),
            )
        )

    return file_path_maps


def write_style_file(output_directory: str) -> str:
    style_file_path = os.path.join(output_directory, "style.css")

    write_file(
        style_file_path,
        [
            "@page {",
            "margin: 0;",
            "}",
            "body {",
            "display: block;",
            "margin: 0;",
            "padding: 0;",
            "}",
        ],
    )

    return style_file_path


def write_image_xhtml_files(
    image_path_maps: List[Tuple[str, str]],
    image_directory: str,
    output_directory: str,
) -> List[str]:
    xhtml_paths = []
    for image_path_map in image_path_maps:
        image_path, flat_image_path = image_path_map
        image = Image.open(os.path.join(image_directory, image_path))
        width, height = image.size

        xhtml_path = os.path.join(
            output_directory, f"{os.path.splitext(flat_image_path)[0]}.xhtml"
        )
        xhtml_paths.append(xhtml_path)

        write_file(
            xhtml_path,
            [
                '<?xml version="1.0" encoding="UTF-8"?>',
                "<!DOCTYPE html>",
                '<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">',
                "<head>",
                f"<title>{os.path.splitext(flat_image_path)[0]}</title>",
                '<link href="style.css" type="text/css" rel="stylesheet"/>',
                f'<meta name="viewport" content="width={width}, height={height}"/>',
                "</head>",
                '<body style="">',
                '<div style="text-align:center;top:0.0%;">',
                f'<img width="{width}" height="{height}" src="../Images/{flat_image_path}"/>',
                "</div>",
                "</body>",
                "</html>",
            ],
        )

    return xhtml_paths


def write_toc_file(
    title: str, book_uuid: str, first_page_path: str, output_directory: str
) -> str:
    toc_path = os.path.join(output_directory, "toc.ncx")

    write_file(
        toc_path,
        [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<ncx version="2005-1" xml:lang="en-US" xmlns="http://www.daisy.org/z3986/2005/ncx/">',
            "<head>",
            f'<meta name="dtb:uid" content="urn:uuid:{book_uuid}"/>',
            '<meta name="dtb:totalPageCount" content="0"/>',
            '<meta name="dtb:maxPageNumber" content="0"/>',
            '<meta name="generated" content="true"/>',
            "</head>",
            f"<docTitle><text>{title}</text></docTitle>",
            "<navMap>",
            f'<navPoint id="Text"><navLabel><text>{title}</text></navLabel><content src="Text/{first_page_path}"/></navPoint>',
            "</navMap>",
            "</ncx>",
        ],
    )

    return toc_path


def write_nav_file(
    title: str, first_page_path: str, output_directory: str
) -> str:
    nav_path = os.path.join(output_directory, "nav.xhtml")

    write_file(
        nav_path,
        [
            '<?xml version="1.0" encoding="utf-8"?>',
            "<!DOCTYPE html>",
            '<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">',
            "<head>",
            f"<title>{title}</title>",
            '<meta charset="utf-8"/>',
            "</head>",
            "<body>",
            '<nav xmlns:epub="http://www.idpf.org/2007/ops" epub:type="toc" id="toc">',
            "<ol>",
            f'<li><a href="Text/{first_page_path}">{title}</a></li>',
            "</ol>",
            "</nav>",
            '<nav epub:type="page-list">',
            "<ol>",
            f'<li><a href="Text/{first_page_path}">{title}</a></li>',
            "</ol>",
            "</nav>",
            "</body>",
            "</html>",
        ],
    )

    return nav_path


def generate_page_items(xhtml_paths: List[str]) -> List[Tuple[str, str]]:
    page_items = []

    for xhtml_path in xhtml_paths:
        page_items.append(
            generate_item(xhtml_path, "page", "Text", "application/xhtml+xml")
        )

    return page_items


def generate_image_items(image_paths: List[str]) -> List[Tuple[str, str]]:
    image_items = []

    for image_path in image_paths:
        image = Image.open(image_path)
        image_items.append(
            generate_item(image_path, "img", "Images", image.format.lower())
        )

    return image_items


def generate_item(
    item_path: str, prefix: str, href_dir: str, media_type: str
) -> Tuple[str, str]:
    item_base = os.path.basename(item_path)
    item_id = f"{prefix}_Images_{os.path.splitext(item_base)[0]}"
    item_href = f"{href_dir}/{item_base}"
    return (
        item_id,
        f'<item id="{item_id}" href="{item_href}" media-type="image/{media_type}"/>',
    )


def create_metadata(title: str, book_uuid: str) -> List[str]:
    current_utc_time = datetime.now(timezone.utc)
    modified_time = current_utc_time.strftime("%Y-%m-%dT%H:%M:%SZ")

    return [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<package version="3.0" unique-identifier="BookID" xmlns="http://www.idpf.org/2007/opf">',
        '<metadata xmlns:opf="http://www.idpf.org/2007/opf" xmlns:dc="http://purl.org/dc/elements/1.1/">',
        f"<dc:title>{title}</dc:title>",
        "<dc:language>en-US</dc:language>",
        f'<dc:identifier id="BookID">urn:uuid:{book_uuid}</dc:identifier>',
        "<dc:creator>Unknown</dc:creator>",
        f'<meta property="dcterms:modified">{modified_time}</meta>',
        '<meta name="cover" content="cover"/>',
        '<meta property="rendition:orientation">portrait</meta>',
        '<meta property="rendition:spread">portrait</meta>',
        '<meta property="rendition:layout">pre-paginated</meta>',
        "</metadata>",
    ]


def create_manifest(
    cover_image_path: str, xhtml_files: List[str], image_paths: List[str]
) -> List[str]:
    cover_image = Image.open(cover_image_path)

    manifest_lines = [
        "<manifest>",
        '<item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>',
        '<item id="nav" href="nav.xhtml" properties="nav" media-type="application/xhtml+xml"/>',
        f'<item id="cover" href="Images/{os.path.basename(cover_image_path)}" media-type="image/{cover_image.format.lower()}" properties="cover-image"/>',
        '<item id="css" href="Text/style.css" media-type="text/css"/>',
    ]

    page_items = generate_page_items(xhtml_files)
    image_items = generate_image_items(image_paths)

    for page_item in page_items:
        manifest_lines.append(page_item[1])

    manifest_lines += [image_item[1] for image_item in image_items]
    manifest_lines.append("</manifest>")

    return manifest_lines


def create_spine(xhtml_files: List[str]) -> List[str]:
    # TODO: change this depending on manga selected
    spine_lines = ['<spine page-progression-direction="rtl" toc="ncx">']
    page_items = generate_page_items(xhtml_files)

    for page_item in page_items:
        spine_lines.append(f'<itemref idref="{page_item[0]}"/>')

    spine_lines += ["</spine>", "</package>"]

    return spine_lines


def write_content_file(
    title: str,
    book_uuid: str,
    xhtml_files: List[str],
    image_paths: List[str],
    cover_image_path: str,
    output_directory: str,
) -> str:
    content_path = os.path.join(output_directory, "content.opf")

    metadata_lines = create_metadata(title, book_uuid)
    manifest_lines = create_manifest(cover_image_path, xhtml_files, image_paths)
    spine_lines = create_spine(xhtml_files)

    write_file(
        content_path,
        metadata_lines + manifest_lines + spine_lines,
    )


def write_container_file(output_directory: str) -> str:
    container_path = os.path.join(output_directory, "container.xml")

    write_file(
        container_path,
        [
            '<?xml version="1.0"?>',
            '<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">',
            "<rootfiles>",
            '<rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>',
            "</rootfiles>",
            "</container>",
        ],
    )

    return container_path


def write_mime_type_file(output_directory: str) -> str:
    mime_type_path = os.path.join(output_directory, "mimetype")

    write_file(mime_type_path, ["application/epub+zip"])

    return mime_type_path


def create_epub(title: str, epub_directory: str, output_path: str) -> str:
    if not output_path:
        output_path = f"{title}.kepub.epub"

    epub_file = zipfile.ZipFile(
        output_path, mode="w", compression=zipfile.ZIP_DEFLATED
    )

    for root, _, files in os.walk(epub_directory):
        for file in files:
            file_path = os.path.join(root, file)
            relative_file_path = os.path.relpath(file_path, epub_directory)
            epub_file.write(file_path, arcname=relative_file_path)

    epub_file.close()

    return output_path


def create_directories(parent_directory: str) -> List[str, str, str, str]:
    oebps_directory = os.path.join(parent_directory, "OEBPS")
    text_directory = os.path.join(oebps_directory, "Text")
    images_directory = os.path.join(oebps_directory, "Images")
    meta_directory = os.path.join(parent_directory, "META-INF")

    for directory in [text_directory, images_directory, meta_directory]:
        os.makedirs(directory, exist_ok=True)

    return oebps_directory, text_directory, images_directory, meta_directory


def make_ebook(title: str, image_directory: str, output_path: str) -> str:
    temp_directory = tempfile.TemporaryDirectory()
    temp_epub_directory = os.path.join(temp_directory.name, "ebook")
    book_uuid = str(uuid4())

    (
        oebps_directory,
        text_directory,
        images_directory,
        meta_directory,
    ) = create_directories(temp_epub_directory)

    image_paths = get_image_paths(image_directory)
    image_path_maps = map_paths(image_paths)

    cover_image_path = create_cover(
        os.path.join(image_directory, image_paths[0]), images_directory
    )
    new_image_paths = copy_images(
        image_path_maps, image_directory, images_directory
    )
    xhtml_paths = write_image_xhtml_files(
        image_path_maps, image_directory, text_directory
    )

    first_page_path = os.path.basename(xhtml_paths[0])

    write_style_file(text_directory)
    write_toc_file(title, book_uuid, first_page_path, oebps_directory)
    write_nav_file(title, first_page_path, oebps_directory)
    write_content_file(
        title,
        book_uuid,
        xhtml_paths,
        new_image_paths,
        cover_image_path,
        oebps_directory,
    )
    write_container_file(meta_directory)
    write_mime_type_file(temp_epub_directory)

    epub_file_path = create_epub(title, temp_epub_directory, output_path)
    temp_directory.cleanup()

    return epub_file_path
