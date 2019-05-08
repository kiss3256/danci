# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3

class DanciPipeline(object):

    def __init__(self):
        self.connection = sqlite3.connect('danci.db')
        self.cursor = self.connection.cursor()

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS ROOTS
            (id   INTEGER PRIMARY KEY,
            root  VARCHAR(32) NOT NULL,
            description VARCHARP(80));''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS WORDS
            (id   INTEGER PRIMARY KEY,
            word  VARCHAR(32) NOT NULL,
            definition  VARCHAR(120) NOT NULL,
            p_id  INT,
            FOREIGN KEY (p_id) REFERENCES ROOTS(ID));''')


    def process_item(self, item, spider):
        self.cursor.execute('INSERT INTO ROOTS(root, description) VALUES(?,?)',
            (item['root'], item['description']))

        p_id = self.cursor.lastrowid
        for word in item['words']:
            self.cursor.execute('INSERT INTO WORDS(word, definition, p_id) VALUES(?,?,?)',
                (word['word'], word['definition'], p_id))

        self.connection.commit()
