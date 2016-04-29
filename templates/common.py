#!/usr/bin/env python
# fileencoding=utf-8
import re
from bson.objectid import ObjectId
import logging

def combined(val):
    """
    判断val是不是dict或者list
    :param val:
    :return: none
    """
    if isinstance(val, list) or isinstance(val, dict):
        return True
    return False


def encode_object(val):
    """
    Object2str
    :param val:
    :return:
    """
    ans = val
    if isinstance(ans, ObjectId):
        tid = str(ans)
        ans = 'ObjectId:' + tid
    return ans


def decode_object(val):
    """
    str2Object
    :param val:
    :return:
    """
    ans = val
    if isinstance(ans, str) or isinstance(ans, unicode):
        res = re.search(r'^(ObjectId:)([0-9a-fA-F]+)', ans)
        if res:
            ans = ObjectId(res.group(2))
    return ans


def recover_id_form(raw):
    """
    恢复Object类型的变量，方法与changeIdForm类似。
    :param raw:
    :return:
    """
    if not combined(raw): return
    sf = True if isinstance(raw, dict) else False
    if sf:
        for r in raw:
            if combined(raw[r]):
                recover_id_form(raw[r])
            else:
                raw[r] = decode_object(raw[r])
    else:
        for i, r in enumerate(raw):
            if combined(raw[i]):
                recover_id_form(raw[i])
            else:
                raw[i] = decode_object(raw[i])


def change_id_form(raw):
    """
    Object类型在压成json文件时不支持，所以预先把raw_q中所有Object类型的数据转成字符串，
    并在前添加'Object:'在需要时通过正则进行还原。
    该函数大致思路为dfs遍历成员，如果是list或dict的话，递归遍历，否则检查是否是Object类型，
    如果是就转换格式。
    :param raw:
    :return:
    """
    if not combined(raw): return
    sf = True if isinstance(raw, dict) else False
    if sf:
        for r in raw:
            if combined(raw[r]):
                change_id_form(raw[r])
            else:
                raw[r] = encode_object(raw[r])
    else:
        for i, r in enumerate(raw):
            if combined(raw[i]):
                change_id_form(raw[i])
            else:
                raw[i] = encode_object(raw[i])


def show_pretty_dict(val, deep=0):
    """
    格式化输出，用来调试
    :param val:
    :param deep:
    :return: None
    """
    if isinstance(val, dict):
        for r in val:
            if combined(val[r]):
                # print '\t' * deep, r
                tb = u'\t' * deep
                tb += unicode(r)
                tb += u' : '
                logging.info(tb)
                show_pretty_dict(val[r], deep + 1)
            else:
                # print '\t' * deep, r, val[r]
                tb = u'\t' * deep
                tb += unicode(r)
                tb += u' : '
                tb += unicode(val[r])
                logging.info(tb)
    elif isinstance(val, list):
        for i, r in enumerate(val):

            if combined(val[i]):
                # print '\t' * deep, i
                tb = u'\t' * deep
                tb += unicode(i)
                tb += u' : '
                logging.info(tb)
                show_pretty_dict(val[i], deep + 1)
            else:
                # print '\t' * deep, i, val[i]
                tb = u'\t' * deep
                tb += unicode(i)
                tb += u' : '
                tb += unicode(val[i])
                logging.info(tb)

    else:
        # print '\t' * deep, val
        tb = u'\t' * deep
        tb += u' : '
        tb += unicode(val)
        logging.info(tb)
