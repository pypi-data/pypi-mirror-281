# 计算机登录用户: jk
# 系统日期: 2024/6/25 17:00
# 项目名称: chipeak_cv_data_tool
# 开发者: zhanyong
import os
from pathlib import Path
from ccdt.dataset import *


class BaseXml(BaseLabelme):
    def __init__(self, *args, **kwargs):
        # 在这里定义labelme数据结构格式初始化
        super(BaseXml, self).__init__(*args, **kwargs)

    def labelme2xml(self):
        """
        labelme转xml数据集
        """
        pass
