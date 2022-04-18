import unittest
from product import Product


class MyTestCase(unittest.TestCase):
    def test_get_title(self):
        Product("Basketball", "Barely been used and in good shape.", "40")
        self.assertEqual("Basketball", Product.productList[0].get_title())

    def test_get_description(self):
        Product("Basketball", "Barely been used and in good shape.", "40")
        self.assertEqual("Barely been used and in good shape.", Product.productList[0].get_description())

if __name__ == '__main__':
    unittest.main()
