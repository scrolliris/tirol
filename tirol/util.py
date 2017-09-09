"""Utility module.
"""
import json
from os import path

from bleach import clean as _clean
from markupsafe import Markup
from pyramid.decorator import reify
from pyramid.events import subscriber
from pyramid.events import BeforeRender

from .env import Env


@subscriber(BeforeRender)
def add_template_utilities(evt):  # type: (dict) -> None
    """Adds utility functions for templates.
    """
    ctx, req = evt['context'], evt['request']
    util = getattr(req, 'util', None)

    # `util` in template
    if util is None and req is not None:
        util = TemplateUtility(ctx, req)

    evt['util'] = util
    evt['var'] = util.var

    evt['clean'] = clean


class TemplateUtility(object):
    """
    The utility for templates.
    """
    def __init__(self, ctx, req, **kwargs):
        self.context, self.req = ctx, req

        if getattr(req, 'util', None) is None:
            req.util = self
        self.__dict__.update(kwargs)

    @reify
    def manifest_json(self):
        manifest_file = path.join(
            path.dirname(__file__), '..', 'static', 'manifest.json')
        data = {}
        if path.isfile(manifest_file):
            with open(manifest_file) as data_file:
                data = json.load(data_file)

        return data

    @reify
    def var(self):  # pylint: disable=no-self-use
        """ Return a dict has variables
        """
        env = Env()
        return {  # external services
            'gitlab_url': env.get('GITLAB_URL', '/'),
            'tinyletter_url': env.get('TINYLETTER_URL', '/'),
            'twitter_url': env.get('TWITTER_URL', '/'),
            'typekit_id': env.get('TYPEKIT_ID', ''),
            'userlike_script': env.get('USERLIKE_SCRIPT', '/'),
        }

    def is_matched(self, matchdict):
        return self.req.matchdict == matchdict

    def static_url(self, path):
        from . import STATIC_DIR
        return self.req.static_url(STATIC_DIR + '/' + path)

    def static_path(self, path):
        from . import STATIC_DIR
        return self.req.static_path(STATIC_DIR + '/' + path)

    def built_asset_url(self, path):
        path = self.manifest_json.get(path, path)
        return self.static_url(path)

    def allow_svg(self, size):  # type: (str) -> 'function'
        """Return actual allow_svg as function allowing given size
        """
        def _allow_svg(tag, name, value):  # type: (str, str, str) -> bool
            """Returns True if tag is svg and it has allowed attrtibutes
            """
            if tag == 'svg' and name in ('width', 'height', 'class'):
                return True
            else:
                if name == 'viewBox':
                    return value == size
            return False
        return _allow_svg


# tag filters

def clean(**kwargs):  # type: (**dict) -> 'function'
    """Returns sanitized value except allowed tags and attributes

    >>> ${'<a href="/"><em>link</em></a>'|n,clean(
            tags=['a'], attributes=['href'])}
    "<a href=\"/\">link</a>"
    """
    def __clean(text):  # type: (str) -> Markup
        return Markup(_clean(text, **kwargs))

    return __clean