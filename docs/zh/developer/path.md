## 擴充內的檔案讀取
```py
with open("./plugins/${擴充名稱}/test.txt", 'r', encoding='utf-8') as file:
     content = file.read()
     print(content)
```
