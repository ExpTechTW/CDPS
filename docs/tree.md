# 目錄樹
## directory tree
```
CDPS/
    config.yml    // 配置文件
    main.py    // 入口點
    core/
        boostrap.py    // 環境檢查
        config.py    // 配置讀取
        CWAReportSQL.py
        entrypoint.py
        state.py    // 狀態管理
        __init__.py
        __main__.py
        api/
            sql/
                sql.py
                __init__.py
        cli/
            cli_entry.py    // CLI 入口
            cli_gendefault.py    // CLI 生成默認(覆蓋) 配置
            cli_init.py    // CLI 初始化 項目
            cli_run.py    // CLI 執行項目
            cli_version.py    // CLI 顯示版本資訊
            __init__.py
        constants/
            core_constant.py    // 常量
            __init__.py
        resources/
            default_config.yml    // 默認配置文件
        utils/
            file_util.py
            lazy_item.py
            logger.py
            resources_util.py
            yaml_data_storage.py
            __init__.py
    docs/
    logs/
    schemas/
```
