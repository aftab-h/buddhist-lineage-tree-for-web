#!/usr/bin/env node

const fs = require('fs').promises;
const path = require('path');
const sharp = require('sharp');

// Configuration
const CONFIG = {
    inputDir: process.env.INPUT_DIR || './images',
    outputDir: process.env.OUTPUT_DIR || './images/optimized',
    backupDir: process.env.BACKUP_DIR || './images/originals',
    maxSize: 600,          // Max width/height in pixels (increased from 300 for ~100KB target)
    quality: 85,           // JPEG quality (increased from 80 for better quality)
    format: 'jpeg',       // Output format
    supportedFormats: ['.jpg', '.jpeg', '.png', '.webp', '.tiff', '.bmp']
};

// Colors for console output
const colors = {
    green: '\x1b[32m',
    red: '\x1b[31m',
    yellow: '\x1b[33m',
    blue: '\x1b[34m',
    reset: '\x1b[0m'
};

function log(message, color = 'reset') {
    console.log(colors[color] + message + colors.reset);
}

// Ensure directories exist
async function createDirectories() {
    try {
        await fs.mkdir(CONFIG.outputDir, { recursive: true });
        await fs.mkdir(CONFIG.backupDir, { recursive: true });
        log(`✓ Created directories`, 'green');
    } catch (error) {
        log(`Error creating directories: ${error.message}`, 'red');
    }
}

// Get all image files from directory
async function getImageFiles(dir) {
    try {
        const files = await fs.readdir(dir);
        return files.filter(file => {
            const ext = path.extname(file).toLowerCase();
            return CONFIG.supportedFormats.includes(ext);
        });
    } catch (error) {
        log(`Error reading directory: ${error.message}`, 'red');
        return [];
    }
}

// Get file size in KB
async function getFileSize(filePath) {
    try {
        const stats = await fs.stat(filePath);
        return Math.round(stats.size / 1024);
    } catch (error) {
        return 0;
    }
}

// Optimize single image
async function optimizeImage(inputPath, outputPath, backupPath) {
    try {
        const originalSize = await getFileSize(inputPath);
        
        // Backup original (if not already backed up)
        try {
            await fs.access(backupPath);
        } catch {
            await fs.copyFile(inputPath, backupPath);
        }

        // Process image with Sharp
        await sharp(inputPath)
            .resize(CONFIG.maxSize, CONFIG.maxSize, {
                fit: 'inside',           // Maintain aspect ratio
                withoutEnlargement: true // Don't upscale small images
            })
            .jpeg({ 
                quality: CONFIG.quality,
                progressive: true        // Better for web loading
            })
            .toFile(outputPath);

        const optimizedSize = await getFileSize(outputPath);
        const savings = Math.round(((originalSize - optimizedSize) / originalSize) * 100);
        
        return {
            success: true,
            originalSize,
            optimizedSize,
            savings: savings > 0 ? savings : 0
        };
    } catch (error) {
        return {
            success: false,
            error: error.message
        };
    }
}

// Main processing function
async function processImages() {
    log('\n🖼️  Buddhist Lineage Tree - Image Optimizer', 'blue');
    log('==========================================', 'blue');

    // Create directories
    await createDirectories();

    // Get all image files
    const imageFiles = await getImageFiles(CONFIG.inputDir);
    
    if (imageFiles.length === 0) {
        log(`No images found in ${CONFIG.inputDir}`, 'yellow');
        return;
    }

    log(`\nFound ${imageFiles.length} images to optimize...`, 'blue');

    let processed = 0;
    let totalOriginalSize = 0;
    let totalOptimizedSize = 0;
    let errors = 0;

    // Process each image
    for (const file of imageFiles) {
        const inputPath = path.join(CONFIG.inputDir, file);
        const basename = path.parse(file).name;
        const outputPath = path.join(CONFIG.outputDir, `${basename}.jpg`);
        const backupPath = path.join(CONFIG.backupDir, file);

        // Skip if already optimized
        try {
            await fs.access(outputPath);
            log(`⏭️  Skipping ${file} (already optimized)`, 'yellow');
            continue;
        } catch {
            // File doesn't exist, proceed with optimization
        }

        process.stdout.write(`Processing ${file}... `);

        const result = await optimizeImage(inputPath, outputPath, backupPath);

        if (result.success) {
            totalOriginalSize += result.originalSize;
            totalOptimizedSize += result.optimizedSize;
            processed++;
            
            log(`✓ ${result.originalSize}KB → ${result.optimizedSize}KB (-${result.savings}%)`, 'green');
        } else {
            errors++;
            log(`✗ Error: ${result.error}`, 'red');
        }
    }

    // Summary
    const totalSavings = totalOriginalSize > 0 ? 
        Math.round(((totalOriginalSize - totalOptimizedSize) / totalOriginalSize) * 100) : 0;

    log('\n📊 Optimization Summary:', 'blue');
    log(`   Processed: ${processed} images`);
    log(`   Errors: ${errors}`);
    log(`   Original size: ${totalOriginalSize}KB`);
    log(`   Optimized size: ${totalOptimizedSize}KB`);
    log(`   Total savings: ${totalSavings}% (${totalOriginalSize - totalOptimizedSize}KB)`, 'green');
    
    if (processed > 0) {
        log(`\n✅ Optimized images saved to: ${CONFIG.outputDir}`, 'green');
        log(`📁 Originals backed up to: ${CONFIG.backupDir}`, 'blue');
        log('\n💡 Next step: Update your CSV file to use the optimized images!', 'yellow');
    }
}

// Run the script
if (require.main === module) {
    processImages().catch(error => {
        log(`Fatal error: ${error.message}`, 'red');
        process.exit(1);
    });
}

module.exports = { processImages, CONFIG };