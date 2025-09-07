# Dzogchen Lineage Tree - Interactive Visualization

An interactive web visualization of the Dzogchen Buddhist lineage transmission tree, featuring hierarchical flow diagrams with hover tooltips, search functionality, and lineage filtering.

## Features

- **Interactive Visualization**: Hierarchical flow chart showing transmission relationships
- **Color-coded Lineages**: Different colors for Mind-Mind, Symbolic, and Aural transmissions
- **Search Functionality**: Find specific teachers by English or Tibetan names
- **Filter by Lineage**: Focus on Vimalamitra, Vairocana, or Padmasambhava branches
- **Hover Tooltips**: Detailed information about each teacher
- **Click to Highlight**: Show complete transmission paths
- **Zoom & Pan**: Navigate the full lineage tree

## Getting Started

### Prerequisites
- Node.js (v16 or higher)
- npm or yarn

### Installation & Development

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

3. Open your browser and navigate to `http://localhost:3000`

### Build for Production

```bash
npm run build
```

## Data Source

The visualization uses CSV data containing information about 51+ teachers in the Dzogchen lineage, including:
- English and Tibetan names
- Historical dates
- Detailed descriptions
- Transmission relationships
- Lineage classifications

## Technology Stack

- **D3.js** - Data visualization and SVG manipulation
- **Vite** - Build tool and development server
- **Vanilla JavaScript** - Core application logic
- **CSS3** - Styling and animations

## Usage

- **Search**: Type in the search box to find specific teachers
- **Filter**: Use lineage buttons to focus on specific transmission branches
- **Navigate**: Click and drag to pan, use mouse wheel to zoom
- **Explore**: Hover over nodes for detailed information
- **Highlight**: Click on any teacher to see their complete lineage path