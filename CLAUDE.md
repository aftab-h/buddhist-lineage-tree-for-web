# Buddhist Lineage Tree - Interactive Visualization

## Overview
This is an interactive web-based visualization of the Dzogchen lineage tree, displaying the transmission of Buddhist teachings across centuries. The application maps the relationships between teachers and students, showing how these profound teachings were passed down through different transmission modes.

## The Three Main Lineages
The visualization organizes the post-symbolic transmission period into three primary lineage branches:

**IMPORTANT**: These three lineages must maintain fixed order: **Vairocana → Vimalamitra → Padmasambhava (left to right)**. This order cannot be changed as it preserves the historical and hierarchical relationships.

1. **Vairocana Lineage** (Left/Green)
   - Begins with Vairocana in the 8th century
   - Continues through disciples like Pang Sang-gyé Gönpo, Yudra Nyingpo
   - Generally sparser in later periods

2. **Vimalamitra Lineage** (Center/Green)
   - Begins with Vimalamitra in the 8th century
   - Most densely populated lineage, especially in later centuries
   - Continues through Nyang Tingzin Zanpo, Longchenpa, and many modern teachers

3. **Padmasambhava Lineage** (Right/Purple)
   - Begins with Padmasambhava in the 8th century
   - Flows through Yeshe Tsogyel, Princess Pemasel, and various treasure revealers
   - Includes many terma (treasure) revelations

## Transmission Modes
The visualization uses color coding to represent different types of dharma transmission:

- **Blue (Mind-to-Mind)**: Direct mind-to-mind transmission between enlightened beings (positions 0-100 - these are ordinal stacking positions representing hierarchical order before linear time, not actual historical years)
- **Purple (Symbolic)**: Transmission through symbols, gestures, and direct pointing-out instructions
- **Green (Aural)**: Oral transmission through spoken teachings and explanations

## Architecture & Spacing Strategy

### Early Period - Shared Ancestors (Positions 0-100)
- **Pre-Linear Time**: These positions represent ordinal hierarchical stacking, not historical years, as this period exists before linear time
- **Compact Positioning**: Blue nodes are tightly grouped in the center
- **Fixed Width**: 400px width to keep the foundational lineage compact
- **Centered Layout**: All early Mind-to-Mind transmission nodes cluster around the middle

### Later Period - Three Lineage Trees (Post-100)
- **Fixed Sequential Order**: Vairocana → Vimalamitra → Padmasambhava (left to right) - this order is mandatory and cannot be changed
- **Dynamic Width Calculation**: Each lineage gets width based on node density in crowded periods using `calculateOptimalLineageWidth()`
- **Sequential Positioning**: Lineages positioned one after another based on actual rightmost node positions + spacing
- **D3 Tree Layout**: Uses D3's tree algorithm within each lineage for proper hierarchical branching

### Positioning Algorithm
1. **Lineage Separation**: Split nodes into the three main lineages plus shared ancestors
2. **Width Calculation**: `calculateOptimalLineageWidth()` determines space needed based on maximum nodes in any time period
3. **Sequential Placement**: Position lineages left-to-right with calculated spacing
4. **D3 Tree Layout**: Within each lineage, use D3's tree algorithm for proper hierarchical positioning
5. **Chronological Y-Axis**: Vertical positioning based on historical time periods

### Key Technical Details
- **Base Spacing**: 200px minimum gap between lineages
- **Node Spacing**: 300px per node in crowded time periods
- **Time Layers**: Chronological positioning using `timeLayer` values from CSV data
- **Collision Detection**: Prevents overlapping while maintaining hierarchical relationships

## Data Structure
The lineage data comes from `dzogchen_lineage.csv` with the following exact column structure:

### CSV Column Structure (1-14):
1. **Name_English** - Teacher names in English (source of truth for all name references)
2. **Name_Wylie_Tibetan** - Tibetan transliteration using Wylie system
3. **Name_Tibetan** - Tibetan script
4. **Name_Chinese** - Chinese names where applicable
5. **Dates** - Birth and death years (e.g., "1308-1364") or time periods
6. **Description_English** - Brief description of the master's role/significance
7. **Description_Tibetan** - Tibetan description
8. **Description_Chinese** - Chinese description
9. **Transmission_Mode** - Mind-to-Mind, Symbolic, or Aural
10. **Lineage** - Which of the three main lineages (Vairocana, Vimalamitra, Padmasambhava, or "All lineages")
11. **Received_Teachings_From** - Teacher(s) this master learned from (semicolon-separated names)
12. **Gave_Teachings_To** - Student(s) this master taught (semicolon-separated names)
13. **Eminated as** - Names of entities that emanated as this master (semicolon-separated)
14. **Position_Date** - Numeric chronological positioning value (used for Y-axis positioning)

### Key Field Usage Notes:
- **Name_English (Column 1)**: This is generally canonical source of truth for all name references
- **Received_Teachings_From (Column 11)**: Teacher-student relationships (solid lines), names must match Column 1 exactly
- **Gave_Teachings_To (Column 12)**: Student-teacher relationships (solid lines), names must match Column 1 exactly
- **Eminated as (Column 13)**: Spiritual emanation relationships, names must match Column 1 exactly
- **Position_Date (Column 14)**: Always numeric values for chronological positioning (0-2000+)
- **Multiple names**: Use semicolon (;) separation, no commas within relationship fields

## Visual Features
- **Interactive Tooltips**: Hover over nodes for detailed teacher information
- **Search Functionality**: Find specific teachers by name
- **Lineage Filtering**: Focus on individual lineages
- **Responsive Design**: Adapts to different screen sizes
- **Century Markers**: Timeline visualization along the bottom

## Scalability Requirements & Current Challenges

### Scalability Needs
This visualization must be **highly scalable** because:
- **Continuous Growth**: More nodes are regularly added, especially in the Aural transmission category
- **Dense Bottom Sections**: Later centuries (18th-21st) have many contemporary teachers
- **Visibility Maintenance**: Must remain readable as the dataset expands

### Current Architecture Challenge
We face a **fundamental spacing problem**:

1. **Dense Vimalamitra Lineage**: The center lineage (Vimalamitra) becomes extremely dense, especially at the bottom
2. **Excessive Width Calculation**: `calculateOptimalLineageWidth()` gives Vimalamitra very wide allocation (potentially 300px × many nodes)
3. **Sequential Positioning Problem**: Since we position Padmasambhava after Vimalamitra's rightmost extent, it gets pushed way out to the right
4. **Poor User Experience**: Padmasambhava lineage becomes difficult to read and navigate due to excessive horizontal distance

### The Spacing Dilemma
- **Need Dynamic Spacing**: Bottom sections with many overlapping nodes need room to spread out
- **Must Maintain Order**: Cannot change Vairocana → Vimalamitra → Padmasambhava sequence
- **Avoid Over-Expansion**: Current dynamic width causes Vimalamitra to dominate horizontal space
- **Preserve Readability**: All three lineages must remain accessible and readable

### Architectural Goals
The spacing system must:
1. **Scale gracefully** as more nodes are added
2. **Balance density** between the three lineages
3. **Maintain fixed left-to-right order** while preventing excessive pushing
4. **Keep all lineages** within reasonable viewing distance
5. **Prevent overlap** in dense time periods without sacrificing overall layout

## Goals
This visualization aims to:
1. Make the complex Dzogchen lineage accessible and navigable
2. Preserve the historical accuracy of teacher-student relationships
3. Show the evolution and branching of transmission methods over time
4. Provide an educational tool for understanding Buddhist lineage history
5. **Scale effectively** as the dataset grows, maintaining readability across all lineages

The spacing and layout algorithms balance historical accuracy with visual clarity, ensuring that the dense network of relationships remains readable while preserving the authentic structure of the lineage transmissions.