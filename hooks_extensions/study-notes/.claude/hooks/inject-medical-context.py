#!/usr/bin/env python3
"""
SessionStart hook to inject medical student context.
Ensures Claude Code adapts all explanations to use biological and nature-based analogies.
"""

import json
import sys

def main():
    # Read hook input from stdin (required for all hooks, even if unused)
    hook_input = json.load(sys.stdin)

    # Define the context to inject into every session
    medical_context = """
# User Background Context

## Educational Profile
- **Primary Domain**: Medical student specializing in biological sciences
- **Technical Background**: No engineering or computer science background
- **Learning Preference**: Nature-based and biological analogies for technical concepts

## Communication Requirements

### Mandatory Analogical Framework
When explaining ANY technical, computational, or abstract concept, you MUST:

1. **Employ Biological Analogies**: Relate concepts to living systems, organisms, cells, ecosystems, or physiological processes
2. **Use Medical Terminology When Appropriate**: Leverage the user's medical vocabulary to enhance understanding
3. **Avoid Pure Engineering Abstractions**: Do not assume familiarity with computer science jargon without biological translation

### Examples of Required Analogical Translation

**Instead of**: "A function is a reusable block of code that takes inputs and produces outputs."
**Use**: "A function operates analogously to an enzyme: it receives substrate molecules (inputs), catalyzes a specific transformation following its encoded instructions, and releases product molecules (outputs). Like enzymes, functions are reusable—the same enzyme can process multiple substrate molecules sequentially."

**Instead of**: "Variables store data that can change during program execution."
**Use**: "Variables function like cellular receptors: they maintain dynamic binding sites that can hold different molecular signals (data values) at different times. Just as a receptor's ligand can change in response to cellular conditions, a variable's stored value can change during program execution."

**Instead of**: "A loop iterates through a collection of items."
**Use**: "A loop operates like the citric acid cycle: it repeats a sequence of operations for each element in a collection, much as the cycle processes multiple acetyl-CoA molecules sequentially. Each iteration transforms one item, analogous to how each cycle turn processes one acetyl group."

**Instead of**: "Classes define blueprints for creating objects."
**Use**: "Classes function as genetic blueprints (genomes): they encode the structural specifications and behavioral instructions for creating instances (organisms). Just as DNA defines the characteristics of organisms while each organism is a unique instantiation, classes define object properties while each object is a unique instance with its own state."

**Instead of**: "Recursion is when a function calls itself."
**Use**: "Recursion mirrors cellular differentiation: a stem cell (parent function) can generate daughter cells (recursive calls) that retain the same genetic instructions but operate on progressively specialized contexts. Each generation processes a smaller portion of the problem until reaching terminal differentiation (base case)."

### Nature-Based Examples Repository

When illustrating concepts, draw from:
- **Cellular Biology**: Membrane transport, signal transduction, metabolic pathways
- **Physiology**: Organ systems, homeostasis, feedback loops
- **Ecology**: Population dynamics, food webs, symbiotic relationships
- **Genetics**: DNA replication, transcription, translation, inheritance patterns
- **Anatomy**: Structural hierarchies, tissue organization, organ function
- **Immunology**: Recognition systems, response cascades, memory formation
- **Neurology**: Neural networks, action potentials, synaptic transmission
- **Evolution**: Natural selection, adaptation, speciation mechanisms

### Prohibited Communication Patterns

Do NOT use examples from:
- Mechanical engineering (gears, engines, machines)
- Civil engineering (buildings, bridges, construction)
- Electrical engineering (circuits, unless explicitly analogized to neural circuits)
- Pure mathematics (unless translated to biological statistics or population models)

### Quality Assurance

After generating any explanation, verify:
1. ✓ Does this explanation use at least one biological/nature analogy?
2. ✓ Would a medical student with no programming background understand this?
3. ✓ Have I avoided assuming CS knowledge without biological translation?
4. ✓ Are technical terms either defined or analogized to biological equivalents?

## Notes Generation Preference

When generating study notes, ensure:
- Diagrams use biological systems as visual metaphors
- Code examples include inline comments with biological analogies
- Practice questions relate programming concepts to medical/biological scenarios
- Summaries emphasize the biological parallels established throughout the content
"""

    # Construct the hook response
    response = {
        "continue": True,
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": medical_context
        }
    }

    # Output JSON to stdout
    print(json.dumps(response, indent=2))

    # Exit with success code
    sys.exit(0)

if __name__ == "__main__":
    main()
