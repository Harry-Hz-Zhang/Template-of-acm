---
topic: "最大子数组和"
category: "10-dp"
source: "动态规划 DP.md"
---

# 最大子数组和

```C++
auto maxSubArray = [](const std::vector<int>& arr) -> int {
	int maxSum = arr[0];
	int currSum = arr[0];
	for (size_t i = 1; i < arr.size(); ++i) {
		currSum = std::max(arr[i], currSum + arr[i]);
		maxSum = std::max(maxSum, currSum);
	}
	return maxSum;
};
```

