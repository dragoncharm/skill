# Incremental Standards (User-Added Rules)

Rules in this file were supplied by the user or the team after the bundled standard documents were packaged. This is the newest layer of policy: when a rule here conflicts with a bundled document under `references/standards/`, the rule here wins unless the user explicitly says otherwise.

Nothing here overrides an explicit user instruction given in the current conversation.

## Entry Format

Append each new rule below using this format. One rule per entry; never delete an entry, mark it superseded instead.

```markdown
## IS-<YYYYMMDD>-<NNN> — <short title>

- Added: <YYYY-MM-DD>
- Scope: <languages / frameworks / databases / domestic or international domain, or "all">
- Strength: <强制 | 必须 | 严禁 | 禁止 | 推荐 | 建议>
- Source: <user statement, meeting, or team decision>
- Rule: <the requirement, stated precisely enough to check against code>

<Optional notes, examples, or exceptions.>
```

Number entries sequentially per day (`001`, `002`, …). Record the user's wording in `Source` faithfully enough that later sessions can trace why the rule exists.

## Superseding an Entry

When the user amends or cancels an existing rule, add a new entry that states the change and add `Superseded by: IS-<new id>` to the old entry. Do not rewrite the old rule text.

## Entries

<!-- Append new entries below this line. -->

## IS-20261030-001 — 最小开发与项目一致性：用户开发偏好

- Added: 2026-10-30
- Scope: 使用本 skill 时的代码开发、重构、任务切换和开发记录维护；不限语言、数据库及国内外项目，项目示例只用于说明。
- Strength: 推荐
- Source: 用户在开发对话中确认了整理后的14项习惯，并授权“可以写入开发规范skill 并同步到zcode codex qoder等开发工具”。
- Rule: 默认按以下用户开发偏好选择实现方式；这些偏好不代表公司正式强制条款，也不取消适用的安全、正确性和强制规范要求。有实际业务边界或项目约束需要采用不同方式时，简要说明取舍，不机械套用。

1. **以最小开发为基准。** 围绕当前任务完成必要修改，控制变更范围；没有实际需求时，不提前建设跨任务的通用框架、扩展能力或额外层级。
2. **优先复用现有实现。** 先检索当前模块和邻近实现中的函数、服务、工具及常量，确认语义和行为适用后再复用，避免重复开发。
3. **贴近项目现有写法。** 参考同模块、同类接口的成熟实现，保持结构、命名和注释风格一致；例如当前项目的 modifyUsagePrice，不将该具体接口当作其他项目的固定模板。
4. **让主业务流程直接易读。** 顺序清晰的小段逻辑优先留在业务方法中，用分段注释组织，不要求每个处理步骤都对应一个独立函数。
5. **按实际价值拆分函数。** 具备独立完整的业务规则、存在实际重复，或能明显降低复杂度时再提取；不单凭行数判断，避免仅包装一句抛异常或一次简单调用的小函数。
6. **按必要性增加类和层级。** 单个接口、单一入口的编排不默认增加 Manager、Facade 等中转层；确有独立业务边界或复杂度收益时可拆分，并说明实际用途。
7. **分清数据访问与业务判断。** Mapper 保留必要的关联、过滤和持久化；业务流程、候选匹配及唯一性决策放在业务层，避免把完整业务规则堆入复杂 SQL，也不机械地把数据库过滤全部搬到内存。
8. **优先使用已有常量。** 业务值优先引用对应领域常量，普通数字按项目既有 NumberConst 等惯例复用；不重复定义，不借用数值相同但语义不同的业务常量，也不为此次调整新建通用数字常量类。
9. **按实际需要使用注解。** 增加 @Qualifier 等注解时核对 Bean 定义和实际选择需求；需要消除歧义或明确选择实现时使用，不因邻近代码存在就机械照搬。
10. **给关键处理段写简短中文注释。** 说明该段做什么或为何需要处理，保持项目同类接口的风格；按逻辑段说明，避免逐行复述代码或堆砌无信息量的注释。
11. **新增异常码先检查冲突。** 核对已有占用后选择适合当前项目的连续区间，保持代码与多语言资源同步；不要将某次任务采用的起始编号推广为所有项目的固定编号。
12. **保护其他任务的开发内容。** 修改、重构、回滚和恢复限定在当前任务范围；共享文件按增量合并，不整份覆盖后续或其他任务的修改。
13. **按用户要求暂存并保留恢复依据。** 用户要求撤下当前任务修改或回滚时，先保存代码、开发记录及必要差异或补丁，再只处理该任务；恢复时核对后续变化。没有回滚请求时，不因提到任务切换而自动撤下代码。
14. **开发记录随实现维护。** 已有任务记录时持续更新同一份，写清最终方案、实际变更、验证结果和暂存恢复状态；区分本轮执行、沿用结果及未执行项，不重复生成多份完整记录。


## IS-20261030-002 — 优先明确类型，减少不必要的Object使用

- Added: 2026-10-30
- Scope: Java及具有类似Object顶层类型的业务代码；新增或本次授权重构涉及的参数、返回值、字段和集合元素类型。
- Strength: 推荐
- Source: 用户要求“同时在开发规范中增加一条，尽量少或不使用object类”。
- Rule: 优先使用明确的业务类型和适当的泛型，尽量少用或不用Object承载类型已知的业务数据，提高编译期类型检查和代码可读性；本条为用户开发偏好，不将Object一律判为公司强制违规。

- 业务结构已知时，优先复用现有DTO、领域对象、具体标量类型及带明确元素类型的集合，避免不必要的Object参数/返回值/字段、List<Object>、Object[]或Map<String, Object>。
- 不为去掉Object而引入无约束泛型、额外包装层或不必要的新DTO，也不要借助强制类型转换掩盖业务类型；数据类型的选择须同时遵循最小开发原则。
- 框架或接口固定签名（如equals(Object)）、真正异构的数据和运行时才能确定结构的动态边界可以保留Object；在边界集中完成必要的校验和转换，避免在类型明确的业务流程中层层传递。
- 存量代码仅在本次授权范围内逐步收敛，不因新增规则自动扩大重构范围。本条不限制java.util.Objects.equals等工具方法的正常使用。
