import pandas as pd

class Solution:
    def find_customers(self, customer: pd.DataFrame, product: pd.DataFrame) -> pd.DataFrame:
        total_products = product['product_key'].nunique()
        grouped = customer.groupby('customer_id')['product_key'].nunique().reset_index()
        result = grouped[grouped['product_key'] == total_products][['customer_id']]
        return result

def find_customers(customer: pd.DataFrame, product: pd.DataFrame) -> pd.DataFrame:
    return Solution().find_customers(customer, product)
