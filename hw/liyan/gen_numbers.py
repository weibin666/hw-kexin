fw = open("phone_numbers.txt", "w", encoding="utf-8")
test_numbers = [f"1380013800{i}" for i in range(10)]  # 示例号码
for num in test_numbers:
    fw.write(f"{num}\n")
fw.close()
