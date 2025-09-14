#!/usr/bin/env node

const fs = require('fs').promises;
const path = require('path');

// Configuration
const CONFIG = {
    imagesDir: './images/optimized',
    outputFile: './image-manifest.json',
    supportedFormats: ['.jpg', '.jpeg', '.png', '.webp', '.gif']
};

// Colors for console output
const colors = {
    green: '\x1b[32m',
    blue: '\x1b[34m',
    yellow: '\x1b[33m',
    reset: '\x1b[0m'
};

function log(message, color = 'reset') {
    console.log(colors[color] + message + colors.reset);
}

// Parse image filename to extract node name and index
function parseImageFilename(filename) {
    const ext = path.extname(filename).toLowerCase();
    if (!CONFIG.supportedFormats.includes(ext)) {
        return null;
    }

    const baseName = path.basename(filename, ext);

    // Match pattern: nodename-number (e.g., "garab-dorje-1", "longchenpa-drime-ozer-2")
    const match = baseName.match(/^(.+)-(\d+)$/);
    if (!match) {
        return null;
    }

    return {
        nodeName: match[1],
        index: parseInt(match[2]),
        filename: filename
    };
}

// Generate the manifest
async function generateManifest() {
    log('\n🗂️  Image Manifest Generator', 'blue');
    log('===============================', 'blue');

    try {
        // Read the images directory
        const files = await fs.readdir(CONFIG.imagesDir);
        log(`Found ${files.length} files in ${CONFIG.imagesDir}`, 'blue');

        // Parse image files and group by node name
        const imageMap = {};
        let processedImages = 0;

        for (const file of files) {
            const parsed = parseImageFilename(file);
            if (parsed) {
                const { nodeName, index, filename } = parsed;

                if (!imageMap[nodeName]) {
                    imageMap[nodeName] = {};
                }

                imageMap[nodeName][index] = `images/optimized/${filename}`;
                processedImages++;
            }
        }

        // Convert to ordered arrays for each node
        const manifest = {};
        for (const [nodeName, indexMap] of Object.entries(imageMap)) {
            // Sort by index and create ordered array
            const sortedIndexes = Object.keys(indexMap).map(Number).sort((a, b) => a - b);
            manifest[nodeName] = sortedIndexes.map(index => indexMap[index]);
        }

        // Write manifest file
        const manifestJson = JSON.stringify(manifest, null, 2);
        await fs.writeFile(CONFIG.outputFile, manifestJson, 'utf8');

        // Summary
        const nodeCount = Object.keys(manifest).length;
        const totalImages = processedImages;

        log('\n📊 Manifest Generation Summary:', 'blue');
        log(`   Nodes with images: ${nodeCount}`);
        log(`   Total images: ${totalImages}`);
        log(`   Manifest size: ${Math.round(manifestJson.length / 1024 * 10) / 10}KB`);
        log(`\n✅ Manifest generated: ${CONFIG.outputFile}`, 'green');

        // Show sample entries
        log('\n📋 Sample manifest entries:', 'yellow');
        const sampleNodes = Object.keys(manifest).slice(0, 3);
        sampleNodes.forEach(nodeName => {
            log(`   "${nodeName}": [${manifest[nodeName].length} images]`);
        });

    } catch (error) {
        log(`❌ Error generating manifest: ${error.message}`, 'red');
        process.exit(1);
    }
}

// Run the script
if (require.main === module) {
    generateManifest().catch(error => {
        log(`Fatal error: ${error.message}`, 'red');
        process.exit(1);
    });
}

module.exports = { generateManifest, CONFIG };