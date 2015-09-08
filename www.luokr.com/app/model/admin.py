#coding=utf-8

import re
import random, hashlib

class AdminModel:

    @staticmethod
    def generate_randauid(strs = '-_0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', size = 64):
        auid = ''
        while size > 0:
            auid = auid + random.choice(strs)
            size = size - 1
        return auid

    @staticmethod
    def generate_randsalt(strs = '0123456789abcdefghijklmnopqrstuvwxyz', size = 8):
        salt = ''
        while size > 0:
            salt = salt + random.choice(strs)
            size = size - 1
        return salt

    @staticmethod
    def generate_password(pswd, salt):
        return hashlib.md5('AL.pswd:' + hashlib.md5(str(pswd) + '#'  + str(salt)).hexdigest()).hexdigest()

    @staticmethod
    def generate_authword(atms, salt):
        return hashlib.md5('AL.auth:' + hashlib.md5(str(atms) + '$'  + str(salt)).hexdigest()).hexdigest()

    @staticmethod
    def get_user_by_usid(datum, usid):
        return datum.single('select * from users where user_id = ?', (usid,))

    @staticmethod
    def get_user_by_name(datum, name):
        return datum.single('select * from users where user_name = ?', (name,))

    @staticmethod
    def get_user_by_mail(datum, mail):
        return datum.single('select * from users where user_mail = ?', (mail,))

    @staticmethod
    def chk_is_user_name(name):
        if re.match(r'^[A-Za-z][-_A-Za-z0-9]{2,}$', name):
            return True
        else:
            return False

    @staticmethod
    def chk_is_user_mail(mail):
        if re.match(r'^[^@\.]+(?:\.[^@\.]+)*@[^@\.]+(?:\.[^@\.]+)+$', mail):
            return True
        else:
            return False

    @staticmethod
    def chk_user_if_perm(user, perm):
        try:
            user = dict(user)
            return user and 'user_perm' in user and user['user_perm'] & perm == perm
        except:
            return False

    @staticmethod
    def chk_user_is_live(user):
        return AdminModel.chk_user_if_perm(user, 0x00000001)

    @staticmethod
    def chk_user_is_root(user):
        return AdminModel.chk_user_if_perm(user, 0x7FFFFFFF)
