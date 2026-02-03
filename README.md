# obstacle-avoidance

```markdown
# End-to-End Wall Effect Perception for Vector-Thrust UAVs

## 📋 A) 项目主档更新 (Project Spec Update)

### 1. 新增/修订的已确认事实 (Confirmed Facts)
*   **硬件 (Hardware):** 正六旋翼构型 (Hexacopter)，矢量喷口角度固定不可调 (Fixed-Tilt/Pre-tilted)，无舵机角度反馈数据。
*   **场景 (Scenario):** 固定墙面，无动态障碍物，无需验证材质泛化性。
*   **定位 (Localization):** 有室内定位系统，但仅作为真值 (Ground Truth) 验证控制效果，**严禁**作为神经网络输入。
*   **进度 (Progress):** MLP Demo 跑通，二分类准确率 100%（简单切片），已完成 `pyulog` 解析与 csv 转换。

### 2. 当前系统定义 (System Definition)
*   **任务 (Task):** 端到端监督学习 (End-to-End Supervised Learning)。
*   **输入 (Input):** `IMU (Acc_x/y/z, Gyro_x/y/z)` + `Motor (PWM/RPM 1~6)` + `Height (Optional)`。
*   **输出 (Output - Two Stage):** 
    *   Stage 1: 状态检测报警 (Classification: 0/1)。
    *   Stage 2: 避障速度指令 (Regression: $v_x, v_y$)。
*   **约束 (Constraints):** 实时性优先（低延迟）。

### 3. 数据与标注/真值现状 (Data status)
*   **来源 (Source):** 真机飞行日志 (`.ulg` -> `.csv`)。
*   **标注 (Labeling):** 目前仅实施方案一（基于时间段手动打标：无墙=0，有墙=1）。
*   **数据段 (Segments):** 已有 Baseline (30-45s), Wall (80-95s), Ground (125-140s) 三段切片。

### 4. 实验与指标现状 (Experiments & Metrics)
*   **基线 (Baseline):** 对比普通四旋翼模式 (Standard Quadrotor Mode)。
*   **可视化 (Visualization):** 已规划 Raw Time-Series, Time-Averaged, RMS, PSD 四类图表。
*   **验证 (Validation):** 通过预实验数据可视化（波形/分布/电机差值）验证了可行性。

### 5. 待确认字段 (TBD / UNKNOWN)
*   采样频率 (Hz) 与滑动窗口长度 (Sequence Length)。
*   控制性能的具体量化指标 (RMS Error vs. Position Drift vs. Control Effort)。
*   回归任务（输出速度）的标签来源（飞手指令 or 计算值）。
*   机载电脑型号及算力限制。

---

## 🚀 B) 执行优先交接单 (Handoff)

### 1. 本周目标 (Goal)
完成预实验数据的全方位可视化分析，并基于此设计回归任务的数据采集方案。

### 2. 关键事实 (Key Facts)
*   **Object:** Fixed-Tilt Hexacopter.
*   **Scenario:** Static Wall.
*   **Method:** PyTorch MLP (Supervised).
*   **Input:** IMU (9-axis) + Motor (6-ch).
*   **Loc:** GT Only, No Input.
*   **Status:** Classification Demo 100% Acc (Risk: Overfitting).

### 3. 本周最小闭环 (MVP Actions)
1.  **动作:** 运行全套可视化代码 (Raw/Mean/RMS/PSD)。 → **产出:** 4张分析图表。 → **验收:** 确认电机转速差与IMU震动在有墙时的显著性。
2.  **动作:** 尝试 1D-CNN 模型代码。 → **产出:** CNN vs MLP 对比结果。 → **验收:** 确认 CNN 是否有性能提升。

### 4. 阻塞点 (Blockers)
*   **Blocker:** 缺乏回归任务标签。 → **Action:** 确认下一批实验如何记录“期望避障速度”。

### 5. 本周必须回答的问题 (Must-Answer Questions)
1.  **采样频率是多少 Hz？** (决定滑动窗口大小，直接影响模型输入维度)
2.  **回归任务的 Label (速度指令) 怎么获取？** (决定能否开展 Stage 2 的训练)

### 6. 可延后 (Optional)
*   基于【HYP：探索更多方法】尝试 LSTM/TCN。
*   论文具体的章节文字润色。
```
