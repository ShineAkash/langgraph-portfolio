# Tweet Generator with Optimize Loop — Graph

```mermaid
graph TD
    START([START]) --> A[generate]
    A --> B[evaluate]
    B --> C{verdict?}
    C -- "Approved" --> END([END])
    C -- "Needs Improvement" --> D[optimize]
    D --> B
```

**Pattern:** A self-correcting loop. A termination guard (`max_iterations`)
prevents infinite loops. Conditional routing decides: exit or feed back
through `optimize → evaluate` again.
