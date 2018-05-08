# -*- coding:utf-8 -*-
'''
如果想默认运行当前测试文件下的所有测试用例，可以直接使用 unittest.main()方法。
那么 main()方法在查找测试用例时按照两个规则:
首先，该测试类必须继承 unittest.TestCase 类;
其次，该测试类下面的方法必 须以“test”开头
'''


import unittest
from Calculator import Calculator

class CountTest(unittest.TestCase):

    # setUp()方法用于测试用例执行前的初始化工作，例如初始化变量、生成数据库测试数据、打开浏览器等
    def setUp(self):
        self.cal = Calculator(8, 4)

    # tearDown()方法与setUp()方法相呼应，用于测试用例执行之后的善后工作，例如清除数据库测试数据、关闭文件、关闭浏览器等
    def tearDown(self):
        pass

    # unittest 要求测试方法必须以“test”开头。例如，test_add、test_sub 等
    def test_add(self):
        result = self.cal.add()
        self.assertEqual(result, 12)

    def test_sub(self):
        result = self.cal.sub()
        self.assertEqual(result, 4)

    def test_mul(self):
        result = self.cal.mul()
        self.assertEqual(result, 32)

    def test_div(self):
        result = self.cal.div()
        self.assertEqual(result, 2)


if __name__ == "__main__":
    # unittest.main()
    # 构造测试集,调用 unittest.TestSuite()类中的 addTest()方法向测试套件中添加测试用例
    suite = unittest.TestSuite()
    suite.addTest(CountTest("test_add"))
    suite.addTest(CountTest("test_sub"))
    suite.addTest(CountTest("test_mul"))
    suite.addTest(CountTest("test_div"))
    # 执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)
