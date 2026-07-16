# Parallel Evaluation — Graph

```mermaid
graph TD
    START([START]) --> A[calculate_sr]
    START --> B[calculate_bpb]
    START --> C[calculate_boundry_precent]
    A --> D[summary]
    B --> D
    C --> D
    D --> END([END])
```

**Pattern:** Fan-out + fan-in via multiple `START → node` edges. All three
metric nodes run in parallel; their results merge into a single summary
node. Uses a custom `replace_value` reducer so partial state is safe.
