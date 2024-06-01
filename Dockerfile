# 選擇 Python 基礎映像檔
FROM python:3.12-slim

# 設定工作目錄
WORKDIR /app

# 複製應用程式需求檔案
COPY requirements.txt .

# 安裝依賴
RUN pip install --no-cache-dir -r requirements.txt

# 複製應用程式代碼
COPY . .

# 設定環境變數（如有需要）
# ENV MY_ENV_VAR=value

# 指定容器啟動命令
RUN python ./main.py init

CMD ["python", "main.py"]