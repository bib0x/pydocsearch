#!/usr/bin/env python3
import argparse
import json
import os
import sys
import yaml

from collections import ChainMap
from itertools import chain, takewhile

class Message():
    RED    = '31;1m'
    BLUE   = '34;1m'
    GREEN  = '32;1m'
    YELLOW = '33;1m'

    @classmethod
    def custom(cls, state, message, color):
        return f"\033[{color}{state}\033[0m {message}"

    @classmethod
    def info(cls, message, colored=True):
        state = '[*]'
        if not colored:
            return f"{state} {message}"
        return cls.custom(state, message, cls.BLUE)

    @classmethod
    def success(cls, message, colored=True):
        state = '[+]'
        if not colored:
            return f"{state} {message}"
        return cls.custom(state, message, cls.GREEN)

    @classmethod
    def error(cls, message, colored=True):
        state = '[-]'
        if not colored:
            return f"{state} {message}"
        return cls.custom(state, message, cls.RED)

    @classmethod
    def matched(cls, message, terms):
        colored = f"\033[{cls.RED}{terms}\033[0m"
        return message.replace(terms, colored)


class Docsearch():
    def __init__(self, options, paths):
        self.opts = options
        self.paths = paths
        self.results = []
        self.env = { k:v for k,v in os.environ.items() if k.startswith('DOCSEARCH_') }
        self.topic_ext = ".yaml"
        self.colored = options['colored']
        self.search = options['search']
        self.mcolored = options['matched']
        self.colored_mode = 'enabled' if self.colored else 'disabled'
        self.mcolored_mode = 'enabled' if self.mcolored else 'disabled' 

    def execute(self):
        """ Dispatch command line arguments """
        if self.opts['inventory']:
            topics = self.gather_inventory()
            for topic in topics:
                print(topic[:-len(self.topic_ext)])
        elif self.opts['env']:
            self.show_env()
        elif self.opts['topic'] and self.opts['pwd']:
            self.show_path_topic()
        elif self.opts['topic'] or self.opts['search']:
            self.show_topic()

    def gather_inventory(self):
        """ Create a list of unique topics (aka YAML files) """
        topics = []
        for path, dirs, filenames in chain.from_iterable(os.walk(p) for p in self.paths):
            if not '.git' in path:
                for filename in takewhile(lambda f: f.endswith(self.topic_ext), filenames):
                    topics.append(filename)
        return sorted(list(set(topics)))

    def show_env(self):
        """ Show useful environment variables """
        for k, v in self.env.items():
            key_out_format = Message().info(f"{k}") if self.colored else f"[*] {k}"
            if k == 'DOCSEARCH_COLORED':
                print("")
                print(key_out_format)
                print(f"color mode {self.colored_mode}")
            elif k == 'DOCSEARCH_MCOLORED':
                print("")
                print(key_out_format)
                print(f"color mode {self.mcolored_mode}")
            elif k == 'DOCSEARCH_PATH':
                print("")
                print(key_out_format)
                for path in self.paths:
                    print(path)
        print("")

    def show_path_topic(self):
        """ Show topic absolute paths """
        for path, topic_file in self._gathering_topics():
            print(os.path.join(path, topic_file))

    def _gathering_topics(self):
        """ Gather topics'YAML files absolute paths """
        topic = self.opts['topic']
        topic_file = f"{topic}.yaml" if topic else None
        for path, dirs, filenames in chain.from_iterable(os.walk(p) for p in self.paths):
            if not '.git' in path:
                if not topic:
                    for filename in takewhile(lambda f: f.endswith(self.topic_ext), filenames):
                        yield (path, filename)
                elif topic_file in filenames:
                    yield (path, topic_file)
                    
    def show_topic(self):
        """ Show topic content based on search parameter """
        data = None
        for path, topic_file in self._gathering_topics():
            topic_path = os.path.join(path, topic_file)
            with open(topic_path, 'r') as ifs:
                try:
                    yamldata = ifs.read()
                    data = yaml.safe_load(yamldata)
                    topic = topic_file[:-len(self.topic_ext)] 
                    self._do_search(data, topic)
                except Exception as e:
                    print(e)

    def _do_search(self, data, topic):
        """ Filter and search topic data from YAML file content """
        if not data:
            raise Exception('No data received from YAML file.')
        if self.opts['links'] and 'links' in data:
            filtered_data = { 'links': data['links'] }
        elif self.opts['cheats'] and 'cheats' in data:
            filtered_data = { 'cheats': data['cheats'] }
        elif self.opts['glossary'] and 'glossary' in data:
            filtered_data = { 'glossary': data['glossary'] }
        else:
            filtered_data = data
        for category, elements in filtered_data.items():
            for element in elements:
                if 'description' in element and 'data' in element:
                    description = element['description']
                    data = element['data']
                    if not self.search or self.search in element['description']:
                        self._print_search(topic, element)

    def _print_search(self, topic, element):
        """ Print formatted search results """
        if self.opts['json']:
            print(json.dumps(element))
            return

        description = element['description']
        data = element['data']
        message = f"[{topic}] {description}"

        if self.colored:
            message = Message().custom(f"[{topic}]", description, Message().YELLOW)
        if self.mcolored and self.search:
            message = Message().matched(message, self.search)

        print(message)
        for d in data:
            print(f"- {d}")
        print("")



def main(paths):
    options = {
        'cheats': True,
        'colored': True,
        'env': False,
        'glossary': True,
        'inventory': False,
        'json': False,
        'links': True,
        'matched': False,
        'pwd': False,
        'search': "",
        'topic': ""
    }

    parser = argparse.ArgumentParser(prog='docsearch')
    parser.add_argument('-C', '--cheats', action='store_true', 
            help='Restrict search on cheats matches')
    parser.add_argument('-G', '--glossary', action='store_true', 
            help='Restrict search on glossary matches')
    parser.add_argument('-L', '--links', action='store_true',
            help='Restrict search on glossary matches')
    parser.add_argument('-c', '--colored', action='store_true',
            help='Enable colored output')
    parser.add_argument('-e', '--env', action='store_true',
            help='Show used DOCSEARCH_* environment variables')
    parser.add_argument('-i', '--inventory', action='store_true',
            help='List all topics')
    parser.add_argument('-j', '--json', action='store_true',
            help='JSON output')
    parser.add_argument('-m', '--matched', action='store_true',
            help='Colorize matched terms')
    parser.add_argument('-p', '--pwd', action='store_true',
            help='Show topics fullpath on matched terms')
    parser.add_argument('-s', '--search', action='store',
            help='Keyword or term to search')
    parser.add_argument('-t', '--topic', action='store',
            help='Search on a specific topic')
    args = parser.parse_args()

    parsed_options = { k:v for k,v in vars(args).items() }
    options = dict(ChainMap(parsed_options, options))

    active_status = ['1', 'true', 'active']

    colored = os.getenv("DOCSEARCH_COLORED")
    if colored and colored.lower() in active_status:
        options['colored'] = True

    match_colored = os.getenv("DOCSEARCH_MCOLORED")
    if match_colored and match_colored.lower() in active_status:
        options['matched'] = True

    docsearch = Docsearch(options, paths)
    docsearch.execute()


if __name__ == "__main__":
    # Mandatory configuration
    envpaths = os.getenv("DOCSEARCH_PATH")
    if not envpaths:
        print("You need to declare DOCSEARCH_PATH environment variable.")
        sys.exit(-1)

    paths = envpaths.split(":")
    main(paths)
