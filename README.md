# End-to-End Wall-Effect Perception for Fixed-Tilt Vector-Thrust Hexacopters

> **Project README / Handoff Doc**  
> This document is meant to preserve **all project-relevant details** while staying practical for day-to-day execution.  
> **No guessing**: anything not confirmed is explicitly marked **TBD** (only when it matters).

---

## 1) One-line Objective (可验收目标)

Build an **end-to-end supervised learning** pipeline that maps **onboard IMU + motor signals** to:
1) **Stage 1:** *wall-present vs wall-absent* **alarm**, and  
2) **Stage 2:** a **real-time avoidance velocity command** \(`v_x, v_y`\),  
for a **fixed wall** near-field scenario using a **fixed-tilt vector-thrust hexacopter**, with **low-latency** as the priority.

---

## 2) Locked Facts (已确认事实)

### Platform / Hardware
- Airframe: **regular hexacopter** (正六旋翼构型).
- Vector thrust: **fixed tilt / pre-tilted** nozzle angle (**not adjustable**).
- **No servo angle feedback** is available in logs (since angle is fixed and not logged).

### Scenario / Scope
- Environment: **static wall only**.
- **No dynamic obstacles**.
- **No need** to prove generalization across wall materials (glass/rough surfaces etc. out of scope).

### Localization / Ground Truth (GT)
- Indoor localization system exists, but:
  - Used **only as Ground Truth** to evaluate control/performance.
  - **Strictly forbidden** as a neural network input (保持“盲飞”输入原则).

### Current Progress
- PyTorch **MLP demo** is running end-to-end.
- Stage 1 (classification) achieved **100% accuracy** on a **simple sliced dataset** → **high risk of overfitting**.
- Log processing: `.ulg` parsing using **pyulog**, and conversion to **CSV** is already done.

---

## 3) Task Definition / System I/O (系统定义与输入输出)

### Learning Paradigm
- **End-to-End Supervised Learning**.

### Inputs (X)
Confirmed channels (do not assume extra axes/sensors):
- **IMU**
  - Accelerometer: `Acc_x, Acc_y, Acc_z`
  - Gyroscope: `Gyro_x, Gyro_y, Gyro_z`
- **Motors**
  - `Motor_1 ... Motor_6` (PWM or RPM; exact field name TBD but 6-channel motor signals are used)
- **Height** *(optional)*

> Note: Do **not** assume magnetometer / “9-axis IMU” unless explicitly confirmed.

### Outputs (Y) — Two Stage
- **Stage 1 (Classification):** `wall_present ∈ {0,1}`
  - **Semantics locked:** `0 = no wall`, `1 = wall present`
- **Stage 2 (Regression):** avoidance velocity command \(`v_x, v_y`\)

### Primary Constraint
- **Real-time first** → prioritize **low latency** and stable behavior over complex pipelines.

---

## 4) Data & Labeling Status (数据与标注现状)

### Data Source
- **Real flight logs**: `.ulg → .csv`

### Labeling (current implementation)
- **Stage 1 labels:** manual labeling **by time segments**.
  - Sliced segments currently used:
    - **Baseline:** `30–45 s`
    - **Wall:** `80–95 s`
    - **Ground:** `125–140 s`

> "Ground" segment is kept as a third regime in data slicing (useful for stress-testing / negative controls), but the *classification task itself* is currently defined as **wall vs no-wall**.

### Pre-validation (已做验证)
- Pre-experiment visualization/inspection planned and partially used to validate feasibility:
  - waveform / distribution
  - motor differences
  - IMU vibration signatures

---

## 5) Experiments & Evaluation (实验与评估)

### Baseline / Comparison
- Compare against **standard quadrotor mode** (普通四旋翼模式 / standard mode) as baseline behavior.

### Metrics (important but not locked yet)
We need a metric set to support the claim “more stable than baseline” near the wall. Candidate metrics:
- **A) Attitude stability:** RMS error of roll/pitch (lower is better)
- **B) Position holding:** XYZ drift (requires GT)
- **C) Control effort:** motor output fluctuation/smoothness

> TBD (must choose soon if it blocks writing/experiments).

### Planned Visualization (图表计划)
- Raw time-series
- Time-averaged
- RMS
- PSD

---

## 6) Known Risks / Failure Modes (风险与失败模式)

### Risk: Stage 1 “100% accuracy” is likely overfitting
Because current dataset is sliced very cleanly, accuracy can be inflated.

**Minimum validation action (建议保留为必做项):**
- Add **intermediate-distance / transitional trajectories** (not only “far” vs “very close”),
- then run **confusion tests** where signals are less separable.

### Risk: Stage 2 label availability
Stage 2 needs supervised labels for \(`v_x, v_y`\), which are not yet defined/available.

---

## 7) Blockers (阻塞点) — Only what truly blocks near-term progress

1) **Stage 2 labels (must):** how to obtain ground-truth avoidance velocity commands.
2) **Sampling / windowing (must):** log sampling frequency and chosen sequence length (impacts model input tensor definition).
3) **Metric choice (soon):** select 1–2 primary metrics to support the “stability improvement” claim.

---

## 8) Next Actions (执行清单：动作 → 产出 → 验收)

### This Week (MVP loop)
1) **Run full visualization suite** (Raw / Mean / RMS / PSD)  
   - Output: 4 sets of plots  
   - Acceptance: demonstrate consistent signal differences for wall-present vs wall-absent (esp. motor differential + IMU vibration signatures)

2) **Overfitting check via transitional data**  
   - Output: a new evaluation slice containing intermediate distances / approach trajectories  
   - Acceptance: Stage 1 performance remains meaningful (accuracy drops are acceptable; interpretability improves)

3) **Design Stage 2 data collection plan** (label source decision)  
   - Output: a clear labeling method + logging requirement checklist  
   - Acceptance: can run a pilot flight that produces at least one usable labeled sample sequence for Stage 2

---

## 9) Minimal TBD (只保留“重要且会影响结论/实现”的 TBD)

- **TBD-1:** Log sampling frequency (Hz) and time alignment status between IMU and motor channels
- **TBD-2:** Sequence length (window size) and stride (defines model input tensor)
- **TBD-3:** Stage 2 label definition: pilot stick command vs computed “ideal” velocity (or other)
- **TBD-4:** Which primary metric(s) will be used to quantify stability improvement vs baseline
- **TBD-5:** Whether indoor localization logs will be recorded in each run (GT only) and in what format (for drift/trajectory evaluation)

---

## 10) Notes / Guardrails (写作与实现护栏)

- Keep the “GT-only” principle explicit in the paper: localization is **evaluation-only**, not a model input.
- Avoid unconfirmed hardware claims in the manuscript (e.g., “9-axis IMU”, exact tilt angle) unless measured and logged.
- When reporting Stage 1 results, always mention dataset slicing and include a harder test (transitional trajectories) to avoid “too clean” claims.

---

## 11) Optional (可延后，不阻塞本周闭环)
- Try alternative temporal models (e.g., 1D-CNN/TCN/LSTM) **only after** Stage 1 generalization checks and Stage 2 labeling plan are in place.
- Writing polish / chapter structure refinement (do after metrics + Stage 2 labeling are decided).

---
