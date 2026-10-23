#include <vector>
#include <unordered_map>
#include <unordered_set>

using namespace std;

class Solution {
public:
    vector<int> findCustomers(vector<vector<int>>& customer, vector<int>& product) {
        unordered_set<int> allProducts(product.begin(), product.end());
        unordered_map<int, unordered_set<int>> customerProducts;
        for (const auto& c : customer) {
            customerProducts[c[0]].insert(c[1]);
        }
        vector<int> result;
        for (const auto& [id, prods] : customerProducts) {
            if (prods.size() == allProducts.size()) {
                result.push_back(id);
            }
        }
        return result;
    }
};
