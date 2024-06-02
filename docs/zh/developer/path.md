## 擴充內的檔案讀取
```py
with open("./plugins/${擴充名稱}/test.txt", 'r', encoding='utf-8') as file:
     content = file.read()
     print(content)
```

## 擴充 的 config 讀取
```py
with open("./config/${擴充名稱}.json", 'r', encoding='utf-8') as file:
     content = file.read()
     print(content)
```