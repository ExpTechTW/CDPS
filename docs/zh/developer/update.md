## 1.0.18
### 🌟 新增
- pip 依賴檢查
- @new_thread 裝飾器
### 🐞 修正
- Config 類不是 單例類 的問題
- Log `__init__` 覆蓋天數的問題
> [!WARNING]
> plugin 內的 task 現在改為 task_run [參考這裡](https://github.com/ExpTechTW/CDPS/blob/master/docs/zh/developer/thread.md#task_run)

## 1.0.17 (hotfix)
### 🐞 修正
- 初始化崩潰

## 1.0.16 (hotfix)
### 🐞 修正
- 初始化崩潰

## 1.0.15
### 🌟 新增
- 事件 裝飾器
- `onCommandEvent`
- `cdps version` ( In Program Command )
- `cdps exit` ( In Program Command )
- `cdps plugin reload {plugin}` ( In Program Command )
### 🔌 優化
- Command 錯誤處理方式
### 🐞 修正
- Log 錯字