#!/usr/bin/env python

import os
from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint
from xml.dom.minidom import Element


class LinksParser(HTMLParser):
    in_list = False
    index = 0
    link = None
    links = []

    def take_link(self, attrs):
        return None

    def handle_starttag(self, tag, attrs):
        if tag == 'ul':
            self.in_list = 'ul'
            self.index = 0
        elif tag == 'ol':
            self.in_list = 'ol'
            self.index = 0
        elif tag == 'li':
            self.index += 1
        elif tag == 'a':
            attrs = dict(attrs)
            take = self.take_link(attrs)
            if take is not None:
                self.link = attrs
                self.link['text'] = u''
                self.link.update(take)

    def handle_entityref(self, name):
        if self.link:
            self.link['text'] += unichr(name2codepoint[name])

    def handle_charref(self, name):
        if self.link:
            if name.startswith('x'):
                c = unichr(int(name[1:], 16))
            else:
                c = unichr(int(name))
            self.link['text'] += c

    def handle_data(self, data):
        if self.link:
            self.link['text'] += data

    def handle_endtag(self, tag):
        if tag == 'a' and self.link:
            self.links.append(self.link)
            self.link = None
        elif tag == 'ul':
            self.in_list = False
        elif tag == 'ol':
            self.in_list = False

    @classmethod
    def parse(cls, data):
        parser = cls()
        parser.feed(data)
        parser.close()
        return parser.links

