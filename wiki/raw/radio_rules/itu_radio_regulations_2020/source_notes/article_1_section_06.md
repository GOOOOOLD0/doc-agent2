---
title: 第1条 — 第6节
created: 2026-07-29
updated: 2026-07-29
type: source
tags: [regulation, radio_rules]
sources: [raw/radio_rules/itu_radio_regulations_2020/source/source.pdf]
confidence: low
source_doc: 无线电规则：2020年第1卷——条款
source_version: 2020
source_location: 第15页 至 第32页
node_id: 1
chunk_id: article_01_section_06
---

# 第1条 — 第6节

## 一句话总结

本节定义无线电发射与设备的技术特性术语，涵盖辐射/发射的区分、发射类别与单边带变体、无用发射（带外/杂散）的分类体系、频率参数（指配/特征/基准频率、必要带宽、占用带宽）、极化方式、功率定义（峰包/平均/载波）、天线增益与等效辐射功率，以及对流层/电离层散射等传播概念，共计29项定义（1.137–1.165），并附有中/法/英/西/阿/俄六语种无用发射术语对照表。

## 源文件

原始内容参见: `chunks\article_01\section_06.md`

## 关键条款 / 关键观点

- **辐射与发射的区分**（1.137–1.138）：辐射是能量以无线电波形式向外发出（任何来源），发射特指由无线电发射电台产生的辐射。接收机本振能量是辐射而非发射——这一区分在干扰分析中至关重要。
- **发射类别与单边带**（1.139–1.143）：发射类别以标准符号标示调制方式等特性，单边带发射按载波抑制程度分为全载波、减载波和抑制载波三种。
- **无用发射三分法**（1.144–1.146B）：无用发射 = 带外发射 + 杂散发射。带外域紧邻必要带宽（以带外发射为主），杂散域为带外域以外（以杂散发射为主）。这两项定义由WRC-03修订完善。附六语种术语对照表：带外发射（out-of-band emission）、杂散发射（spurious emission）、无用发射（unwanted emissions）。
- **频率参数体系**（1.147–1.153）：指配频段=必要带宽+2×频率容限（空间电台另加2×最大多普勒频移），指配频率为频段中心，基准频率相对于指配频率固定，频率容限为最大容许偏差，必要带宽为恰好保证信息传输的带宽，占用带宽为功率占比β/2（默认0.5%）所确定的带宽。
- **极化**（1.154–1.155）：定义右旋（顺时针）极化波和左旋（逆时针）极化波，以传播方向为参考。
- **功率定义**（1.156–1.159）：三种功率形式——峰包功率（PX/pX）、平均功率（PY/pY）、载波功率（PZ/pZ），分别对应调制包络峰值、长时间平均和无调制状态。符号p为瓦、P为分贝。
- **天线增益与等效功率**（1.160–1.163）：三种基准天线的增益（全向Gi、半波振子Gd、短垂直Gv），对应e.i.r.p.、e.r.p.和e.m.r.p.。
- **传播机制**（1.164–1.165）：定义对流层散射和电离层散射两种超视距传播机制。

## 涉及概念

- 辐射（radiation）、发射（emission）、发射类别（class of emission）
- 单边带发射（SSB）：全载波/减载波/抑制载波单边带发射
- 带外发射（out-of-band emission）、杂散发射（spurious emission）、无用发射（unwanted emissions）
- 带外域（out-of-band domain）、杂散域（spurious domain）
- 指配频段（assigned frequency band）、指配频率（assigned frequency）、特征频率（characteristic frequency）
- 基准频率（reference frequency）、频率容限（frequency tolerance）
- 必要带宽（necessary bandwidth）、占用带宽（occupied bandwidth）
- 右旋极化波（right-hand polarized wave）、左旋极化波（left-hand polarized wave）
- 峰包功率（peak envelope power）、平均功率（mean power）、载波功率（carrier power）
- 天线增益（antenna gain）：全向增益（Gi）、半波振子增益（Gd）、短垂直天线增益（Gv）
- 等效全向辐射功率（e.i.r.p.）、有效辐射功率（e.r.p.）、有效单极辐射功率（e.m.r.p.）
- 对流层散射（tropospheric scatter）、电离层散射（ionospheric scatter）
- 多语种术语对照：中/法/英/西/阿/俄六语种（1.149条附表）

## 涉及机构

- ITU-R（国际电信联盟无线电通信部门）：占用带宽定义（1.153）引用ITU-R建议书确定β/2值；功率关系载明在ITU-R建议书中
- WRC-03（2003年世界无线电通信大会）：第1.146A条（带外域）和第1.146B条（杂散域）由WRC-03增补

## 可能影响

- 无用发射三分法（带外/杂散/无用）是无线电设备型号核准、电磁兼容（EMC）标准制定的核心概念框架
- 功率定义（峰包/平均/载波）直接影响发射机功率限值和频率协调中的干扰计算
- e.i.r.p./e.r.p./e.m.r.p.三种等效功率定义是卫星和地面业务功率通量密度限制的基础
- 必要带宽和占用带宽的定义是频谱占用管理和频率指配的技术依据

## 待核查问题

- 第1.146A/B（带外域/杂散域）标注WRC-03修订，与较早版本的"无用发射"定义体系有差异，需注意版本适用性
- 第1.149条附表中西班牙文"杂散发射"为"Emisión no esencial"（非必要发射），与其他语种的"杂散/寄生"含义不完全对应，存在翻译差异
- 第1.153条占用带宽定义中β/2默认值0.5%，但ITU-R建议书可能对特定发射类别有不同规定，实际应用需查阅最新ITU-R建议书
- 第1.156条功率符号p/P的区别（瓦/分贝）在应用公式时需注意，避免混淆

^[raw/radio_rules/itu_radio_regulations_2020/source_notes/article_1_section_06.md]
