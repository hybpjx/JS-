# -*- coding: utf-8 -*-
# @Time    : 2022/8/19 13:18
# @Author  : lzc
# @Email   : hybpjx@163.com
# @File    : CustomException.py
# @Software: PyCharm

# 时间错误的异常
class TimeErrorException(Exception):
    pass


# 更新成功主动抛出的异常
class UpdateSuccessException(Exception):
    pass


# 状态码不是404的异常
class Exclude200Exception(Exception):
    pass


# 针对selenium 和Pyppeteer 的错误
class NextPageException(Exception):
    pass


# 针对selenium 的错误
class NOTFOUNDRESOURCEException(Exception):
    pass


# 针对selenium_zip不一致 的错误
class NOZIPLengthEqual(Exception):
    pass
