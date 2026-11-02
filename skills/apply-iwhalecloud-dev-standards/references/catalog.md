# iWhaleCloud Standards Catalog

This catalog routes tasks to a text snapshot of 58 internal standards imported on 2026-08-13. Read only the relevant documents under `standards/`. The original screenshot attachments are not bundled; treat image-only requirements as unavailable evidence.

## Status Markers

- Unmarked filename: current formal source unless the document body says otherwise.
- `旧版-保留期`: legacy source; do not use by default.
- `公开评审`: provisional review draft; label conclusions.
- `建设中`: incomplete draft; label conclusions and expect gaps.
- `暂缺`: placeholder without authoritative rules.

## Route by Technology or Task

| Scope | Reference subtree | Use for |
| --- | --- | --- |
| Java | `standards/Java开发规范/` | Language rules, JVM operations, Java security, and Web application security |
| JavaScript | `standards/JavaScript开发规范/` | ES5, ES6, Vue, and React code |
| Go | `standards/Golang规范/` | Go language and coding rules |
| Python | `standards/Python规范/` | Python language and coding rules |
| C/C++ | `standards/C++开发规范/` | C/C++ programming and security rules |
| Mobile | `standards/APP规范/` | Android Java/Kotlin, iOS Objective-C/Swift, React Native, and app delivery |
| MySQL | `standards/MySQL规范/` | Data modeling, SQL development, operations, and security |
| Oracle | `standards/Oracle规范/` | Data modeling, SQL development, and operations |
| PostgreSQL | `standards/PostgreSQL规范/` | Data modeling, SQL development, and operations |
| QMDB | `standards/QMDB规范/` | SQL and operations; the OMDB modeling document is marked missing |
| Redis | `standards/Redis规范(建设中)/` | Provisional Redis design, development, and operations rules |
| HBase | `standards/HBase规范/` | PHOENIX/HBase operations; SQL is under construction and modeling is missing |
| TimesTen | `standards/TimesTen规范/` | SQL and operations; modeling is marked missing |
| ClickHouse | `standards/ClickHouse规范/` | Provisional data-modeling rules |
| DevOps/ZCM | `standards/DevOps接入规范/` | ZCM application development and operations access |
| International platform | `standards/国际平台开发规范/` | ZDubbo, ZMQ, ZSmart R9 DMS, V8 Timer, framework, and tracing rules |
| Security and supply chain | `standards/安全规范及规定/` | Product design/R&D security, security red lines, open-source and third-party components, delivery/operations security |
| Configuration management | `standards/配置管理规范/` | Domestic configuration and international release/framework-version management |
| Certification overview | `standards/认证体系概览.md` | Certification-system context, not a substitute for technical rules |

## Selection Checklist

Combine every matching layer:

1. general security and red-line documents;
2. language and framework documents;
3. database design, SQL, operations, and security documents;
4. domestic or international platform/configuration documents;
5. delivery or DevOps documents when the task reaches build, release, or operations.

Search filenames first:

```bash
rg --files references/standards | rg 'Java|Vue|MySQL|安全|DevOps'
```

Search rules second:

```bash
rg -n -i '关键词|规则编号|强制|禁止|推荐' references/standards/<matching-subtree>
```

Open enough surrounding text to capture the rule, exceptions, explanation, and examples. Do not cite a search hit without reading its context.
