import base64
import os
import requests
import shutil

from bs4 import BeautifulSoup as bs
from markdownify import MarkdownConverter
from urllib.parse import unquote


class EdTagsConverter(MarkdownConverter):
    '''
    Custom converter for EdStem HTML tags.
    '''

    def convert_link(self, el, text, convert_as_inline):
        return super().convert_a(el, text, convert_as_inline)

    def convert_break(self, el, text, convert_as_inline):
        return super().convert_br(el, text, convert_as_inline)

    def convert_heading(self, el, text, convert_as_inline):
        n = int(el.attrs.get('level', None)) or 1
        return super().convert_hn(n, el, text, convert_as_inline)

    def convert_paragraph(self, el, text, convert_as_inline):
        return super().convert_p(el, text, convert_as_inline)

    def convert_callout(self, el, text, convert_as_inline):
        block_form = super().convert_blockquote(el, text, convert_as_inline)
        callout_type = el.attrs.get('type', None) or 'info'

        return f'!!! {callout_type}' + block_form.replace('> ', '  ')

    def convert_image(self, el, text, convert_as_inline):
        download = self.options.get('download_images', False)
        embed = self.options.get('embed_images', False)

        if download or embed:
            r = self.download_image(el)

        if embed:
            mime_type = r.headers['Content-Type']
            content = base64.b64encode(r.raw.read())

            f = '![{}](data:{};base64,{})'

            image = f.format(
                el.attrs.get('alt', ''),
                mime_type,
                content.decode("utf-8")
            )
            return image + '\n\n'

        if download:
            filename = r.headers['content-disposition'] \
                .split(';')[1] \
                .split('=')[1]
            filename = filename.replace('"', '')
            filename = unquote(filename)
            filename = filename.replace(' ', '_')
            filename = filename.replace(' ', '_')

            root_images_path = self.options.get('image_path', None)
            if root_images_path and os.path.isdir(root_images_path or ''):
                filepath = os.path.join(root_images_path, filename)
                with open(filepath, 'wb') as f:
                    shutil.copyfileobj(r.raw, f)

            el.attrs['src'] = filepath  # replace src with local path

        return super().convert_img(el, text, convert_as_inline) + '\n\n'

    def convert_bold(self, el, text, convert_as_inline):
        return super().convert_strong(el, text, convert_as_inline)

    def convert(self, html):
        soup = bs(html, 'lxml-xml')
        return self.convert_soup(soup)

    def download_image(self, el):
        src = el.attrs.get('src', None)

        # download image and save to file or embed as base64
        r = requests.get(src, stream=True)
        if r.status_code == 200:
            r.raw.decode_content = True
            return r

        raise Exception(f'Failed to download image: {src}')
