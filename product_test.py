import unittest
from product import Product
from wiki.web.routes import search_products


class MyTestCase(unittest.TestCase):
    def test_get_title(self):
        Product("Basketball", "Barely been used and in good shape.", "40", 0)
        self.assertEqual("Basketball", Product.productList[0].get_title())

    def test_get_description(self):
        Product("Basketball", "Barely been used and in good shape.", "40", 0)
        self.assertEqual("Barely been used and in good shape.", Product.productList[0].get_description())

    def test_getJson(self):
        product = Product("Basketball", "Barely been used and in good shape.", "40", 0)
        productDict = product.getJson()
        self.assertEqual(productDict["title"], "Basketball")
        self.assertEqual(productDict["description"], "Barely been used and in good shape.")
        self.assertEqual(productDict["price"], 40)
        self.assertEqual(productDict["bought"], 0)


if __name__ == '__main__':
    unittest.main()
