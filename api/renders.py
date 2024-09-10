from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer, BaseRenderer

class PlainTextRenderer(BaseRenderer):
    media_type = 'text/plain'
    format = 'txt'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return str(data).encode('utf-8')
