# radio_regulations_2020 解析记录

- 共识别到 10 个章、62 个条。(来源文件类型: .pdf, 位置单位: 页)


## chunk_articles.py 追加记录

- 第1条跨 18 页,超过单条款常规篇幅,建议做款级二次切分。
- 经人工判断:第1条(术语定义)内容为款级编号的定义集合,无类似第5条的独立脚注编号体系,不做二次切分,以整条为单位处理。

## semantic 语义加工记录

- 第1条:200款,text_layer原文质量高。清洗22处(页码残留+特殊Unicode字符+脚注分隔符),交叉引用12条(均为决议/脚注/《组织法》款号,均标[待链接])
- 第2条:7款,text_layer原文质量高。频段划分表被展平为连续文字,已在清洗中恢复为Markdown表格。清洗3处(页码残留+脚注标记结构化)
- 第3条:15款,text_layer原文质量高。清洗3处(1处文字层artifact+2处页码残留),交叉引用4条(附录1/2/3→[待链接],第16条→已链接)

## generate_wiki_pages.py 页面生成

- wiki/concepts/regulations/radio_regulations_2020/articles/1.md
- wiki/concepts/regulations/radio_regulations_2020/articles/2.md
- wiki/concepts/regulations/radio_regulations_2020/articles/3.md
- fix: generate_wiki_pages.py 中 method 由硬编码 "ocr" 改为 "text_layer"

## build_index.py 检索索引

- toc_index.md: 3/62 条已处理
- topic_index.md: 40 个主题关键词
