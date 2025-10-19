import execjs
import os

class PYEXJS:
    cwd = os.path.abspath(__file__).replace('py_ex_js.py', 'node_modules')

    def ggzy_zwfwb_tj_gov_cn(self, url: str) -> str:
        file_path = os.path.abspath(__file__).replace('py_ex_js.py', 'js/ggzy_zwfwb_tj_gov_cn.js')
        with open(file_path, 'r') as f:
            ctx = execjs.compile(f.read(), cwd=self.cwd)
            result = ctx.call('ggzy', url)
        return result

    def hanghangcha(self, response: str) -> str:
        file_path = os.path.abspath(__file__).replace('py_ex_js.py', 'js/hanghangcha.js')
        with open(file_path, 'r') as f:
            ctx = execjs.compile(f.read(), cwd=self.cwd)
            result = ctx.call('hhc', response)
        return result

    def www_hengan_com(self, param: str) -> str:
        file_path = self.replace_file_path('js/www_hengan_com.js')
        param = '{"request_url":"/api/cmscontent/appContentService/getFrontPagination","url_param":{"viewType":1,"tenantId":171474,"columnId":255,"currentPage":1,"pageSize":8,"order":1},"requst_type":"get"}'
        result = self.py_exec_js('md5Sign', param=param, fp=file_path)
        return result


    def www_xyzq_com_cn(self, tmpstr: str) -> str:
        file_path = self.replace_file_path('js/www_xyzq_com_cn.js')
        result = self.py_exec_js('xyzq', tmpstr, file_path)
        return result

    def yuanrenxue_2023_match1(self):
        file_path = self.replace_file_path('js/yuanrenyue_2023_match1.js')
        result = self.py_exec_js('match1', '', file_path)
        return result

    def bp(self, pwd='ZhangTong360_123'):
        file_path = self.replace_file_path('js/bp_new.js')
        result = self.py_exec_js('encrypt_', pwd, file_path)
        return result
    
    def gdgpo_czt_gd_gov_cn(self):
        file_path = self.replace_file_path('js/gdgpo_czt_gd_gov_cn.js')
        result = self.py_exec_js('encrypt', '/gpmall-bpoc/notice/v1/ignore/getNoticeList$$1721889976111', file_path)
        return result
    
    def yrx_challenge_web_57(self, response):
        file_path = self.replace_file_path('js/yrx_challenge_web_57.js')
        result = self.py_exec_js('decryptData', response, file_path)
        return result


    def py_exec_js(self, fn, param, fp):
        with open(fp, 'r') as f:
            ctx = execjs.compile(f.read(), cwd=self.cwd)
            result = ctx.call(fn, param)
        return result


    def replace_file_path(self, file_name):
        file_path = os.path.abspath(__file__).replace('py_ex_js.py', file_name)
        return file_path




if __name__ == '__main__':
    param = 'oVZqmKfS5w7LwRrL/MwY904EGhD9Nkb9sADpWuXTOZuQ26VLELLdfbvYQKqPUjy7ONJcmh7tuE7q6CmyS9RLcJit7ZZgoKty0AZ4/pwMftkwbE7E4Zc0jX3fHdB9qkR5C4lGMl76KyrXSFYjNuGhHhITKBrcLLInBSZWbdrZZIudA9RE96r0j+iDgLMYhfg/RVYUmYmgjZGXP47Wir/CCPTUDlS9dyD4d2tR5UYBtmMR1FDyLeRTzRV1Y/l7/bz5/Wjza53BHXKTxIy8ogCfqv2BVSeliLZzzzKcl/lNuE7q6CmyS9TlIdXFwCDGBKty0AZ4/pwMsNln7rh7Ol2oA/9tZeasVA=='
    aa = PYEXJS()
    print(aa.yrx_challenge_web_57(param))