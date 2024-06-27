#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os


class Configuration:
    def __init__(self, folder, name='config'):
        self.folder = folder
        self.file = os.path.join(folder, name + '.properties')
        self.props = self.load()

    def load(self):
        props = {}
        if not os.path.exists(self.file):
            print('[Warning] config file\'{}\' is not exists'.format(self.file))
            return props
        with open(self.file, "rt", encoding="utf-8") as f:
            for line in f:
                key_value = line.split('=')
                key = key_value[0].strip()
                if key != '':
                    value = '='.join(key_value[1:]).strip()
                    props[key] = value
        return props

    def replace_macro_in_value(self, macro: str, replacer: str):
        for k in self.props:
            v = self.props[k]
            if macro in v:
                self.props[k] = v.replace(macro, replacer)

    def save(self, props=None):
        if props is None:
            props = {}
        with open(self.file, 'w+', encoding='utf-8') as out:
            for key in props.keys():
                value = props[key]
                out.write(key + '=' + value + '\n')

    def get(self, key='key', default='default_value', save_if_no=True):
        value = self.props.get(key)
        if value is None:
            if save_if_no:
                return self.set(key, default)
            else:
                return default
        return value

    def set(self, key='key', value='value'):
        self.props[key] = value
        self.save(self.props)
        return value
