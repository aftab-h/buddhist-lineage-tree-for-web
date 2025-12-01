#!/usr/bin/env node

const fs = require('fs').promises;
const path = require('path');

// Image to entity mappings
const IMAGE_MAPPINGS = [
    // Jamyang Khyentse Wangpo page folder
    { file: 'Jamyang Khyentse Wangpo page/2nd Dzigar Kongtrul.jpg', entity: '2nd Dzigar Kongtrul' },
    { file: 'Jamyang Khyentse Wangpo page/3rd Katok Situ.jpg', entity: '3rd Katok Situ Kunchen Orgyen Chökyi Dorjé' },
    { file: 'Jamyang Khyentse Wangpo page/4th Dodrupchen Jikmé Trinlé Palbar.jpeg', entity: '4th Dodrupchen Jikmé Trinlé Palbar' },
    { file: 'Jamyang Khyentse Wangpo page/5th Dzogchen Rinpoche Thupten Chökyi Dorje.jpg', entity: '5th Dzogchen Rinpoche Thupten Chökyi Dorjé' },
    { file: 'Jamyang Khyentse Wangpo page/Adzom Drukpa Rinpoche Drodul Pawo Dorjé.jpg', entity: 'Adzom Drukpa Rinpoche Drodul Pawo Dorjé' },
    { file: 'Jamyang Khyentse Wangpo page/Adzom Gyalse Gyurmé Dorjé.jpg', entity: 'Adzom Gyalse Gyurmé Dorjé' },
    { file: 'Jamyang Khyentse Wangpo page/Dilgo Khyentsé Rinpoche Rabsel Dawa.jpg', entity: 'Dilgo Khyentsé Rinpoche Rabsel Dawa' },
    { file: 'Jamyang Khyentse Wangpo page/Dilgo Khyentsé Yangsi.jpg', entity: 'Dilgo Khyentsé Yangsi' },
    { file: 'Jamyang Khyentse Wangpo page/Druktrul Rinpoche.jpg', entity: 'Adzom Druktrul Tubten Pema Trinlé' },
    { file: 'Jamyang Khyentse Wangpo page/Dudjob Yangsi.webp', entity: 'Dudjom Yangsi a.k.a. Dudjom Sangye Pema Shepa' },
    { file: 'Jamyang Khyentse Wangpo page/Dudjom Rinpoche Jigdral Yeshe Dorje.jpg', entity: 'Dudjom Rinpoche Jigdral Yeshe Dorjé' },
    { file: 'Jamyang Khyentse Wangpo page/Gyakob Tulku Kunzang_Treasury of lives no permission.jpeg', entity: 'Gyakob Tulku Kunzang' },
    { file: 'Jamyang Khyentse Wangpo page/Jamgön Kongtrul_HAR no permissions.jpg', entity: 'Jamgön Kongtrul Yönten Gyatso Lodrö Tayé' },
    { file: 'Jamyang Khyentse Wangpo page/Jamyang Khyentse Chökyi Lodrö.jpg', entity: 'Jamyang Khyentse Chökyi Lodrö' },
    { file: 'Jamyang Khyentse Wangpo page/Jamyang Khyentsé Wangpo.jpg', entity: 'Jamyang Khyentsé Wangpo' },
    { file: 'Jamyang Khyentse Wangpo page/Jedrung Trinlé Jampa Jungné.jpg', entity: 'Jedrung Trinlé Jampa Jungné' },
    { file: 'Jamyang Khyentse Wangpo page/Kangyur Rinpoche Longchen Yeshe Dorje .jpg', entity: 'Kangyur Rinpoche Longchen Yeshé Dorjé' },
    { file: 'Jamyang Khyentse Wangpo page/Khenchen Jampal Dewé Nyima.jpg', entity: 'Khenchen Jampal Dewai Nyima' },
    { file: 'Jamyang Khyentse Wangpo page/Lopön Rinpoche Lama Sönam Zangpo.jpg', entity: 'Lopön Rinpoche Lama Sönam Zangpo' },
    { file: 'Jamyang Khyentse Wangpo page/Minling Trichen Kunzang Wangyal.jpeg', entity: 'Minling Trichen Kunzang Wangyal' },
    { file: 'Jamyang Khyentse Wangpo page/Mipam Jamyang Namgyal Gyatso.jpg', entity: 'Mipam Jamyang Namgyal Gyatso' },
    { file: 'Jamyang Khyentse Wangpo page/Neten_Chokling.jpeg', entity: 'Neten Chokling' },
    { file: 'Jamyang Khyentse Wangpo page/Orgyen Tobgyal Rinpoche.jpg', entity: 'Orgyen Tobgyal Rinpoche' },
    { file: 'Jamyang Khyentse Wangpo page/Ritrul Rigdzin Chögyal a.k.a. Drubwang Adzin Rinpoche.jpg', entity: 'Ritrul Rigdzin Chögyal a.k.a. Drubwang Adzin Rinpoche' },
    { file: 'Jamyang Khyentse Wangpo page/Sakya Khen Rinpoche Appey.jpg', entity: 'Sakya Khen Rinpoche Appey' },
    { file: 'Jamyang Khyentse Wangpo page/Serta Rinpoche.jpg', entity: 'Serta Rinpoche' },
    { file: 'Jamyang Khyentse Wangpo page/Shechen_Gyaltsap.jpg', entity: '4th Zhechen Gyaltsap Gyurmé Pema Namgyal' },
    { file: 'Jamyang Khyentse Wangpo page/Terchen Orgyen Chokgyur Lingpa.jpg', entity: 'Terchen Orgyen Chokgyur Lingpa' },
    { file: 'Jamyang Khyentse Wangpo page/Tokden Śākya Śrī_Treasury of Lives.jpeg', entity: 'Tokden Śākya Śrī' },
    { file: 'Jamyang Khyentse Wangpo page/Tsö Paltrul Rinpoche.jpg', entity: 'Tsö Patrul Rinpoche' },
    { file: 'Jamyang Khyentse Wangpo page/Yukhok Jadralwa Chöying Rangdrol.jpeg', entity: 'Yukhok Jadralwa Chöying Rangdrol' },

    // to be sorted folder
    { file: 'to be sorted/1st Dodrupchen, Jigmé Trinlé Özer.jpg', entity: '1st Dodrupchen' },
    { file: 'to be sorted/2nd Palyul Drupwang Pema Norbu, Rigdzin Kunzang Shedrupa.jpg', entity: '2nd Palyul Drupwang Pema Norbu (Rigdzin Kunzang Shedrupa)' },
    { file: 'to be sorted/Apang Terchen Orgyen Trinlé Lingpa.jpg', entity: 'Apang Terchen Orgyen Trinlé Lingpa' },
    { file: 'to be sorted/Bairo Rinpoché.jpg', entity: 'Bairo Rinpoché' },
    { file: 'to be sorted/Chagdud Tulku Padma Gargyi Wangchuk.jpeg', entity: 'Chagdud Tulku Padma Gargyi Wangchuk' },
    { file: 'to be sorted/Changma Khenchen Tupten Chöpel.jpg', entity: 'Changma Khenchen Tupten Chöpel' },
    { file: 'to be sorted/Chatral Rinpoché Sanjé Dorjé.jpeg', entity: 'Chatral Rinpoché Sanjé Dorjé' },
    { file: 'to be sorted/Dakki Chönyi Zangmo.jpeg', entity: 'Dakki Chönyi Zangmo' },
    { file: 'to be sorted/Dartang Choktrul Chökyi Dawa Rinpoché.jpeg', entity: 'Dartang Choktrul Chökyi Dawa Rinpoché' },
    { file: 'to be sorted/Gemang Gyalse Rigpai Dorjé (Gyalse Zhenpen Tayé Özer).jpg', entity: 'Gemang Gyalse Rigpai Dorjé (Gyalse Zhenpen Tayé Özer)' },
    { file: 'to be sorted/Golok Khenchen Munsel.jpg', entity: 'Golok Khenchen Munsel' },
    { file: 'to be sorted/Jamgön Kongtrul Yönten Gyatso Lodrö Tayé.jpg', entity: 'Jamgön Kongtrul Yönten Gyatso Lodrö Tayé' },
    { file: 'to be sorted/Jetsunma Trinle Chodron.jpg', entity: 'Jetsunma Trinle Chodron' },
    { file: 'to be sorted/Jigmé Gyalwai Nyugu.jpeg', entity: 'Jigmé Gyalwai Nyugu' },
    { file: 'to be sorted/Jigme Khyentse Rinpoche .jpg', entity: 'Jigme Khyentse Rinpoche' },
    { file: 'to be sorted/Katokpa Gyalse Rinpoche Sonam Detsen.jpeg', entity: 'Katokpa Gyalse Rinpoche Sonam Detsen' },
    { file: 'to be sorted/Khen Chökhyap.jpg', entity: 'Khen Chökhyap' },
    { file: 'to be sorted/Khen Ngawang Palzang Yangsi Rinpoché (Tekchok Tenpai Gyaltsen).jpg', entity: 'Khen Ngawang Palzang Yangsi Rinpoché (Tekchok Tenpai Gyaltsen)' },
    { file: 'to be sorted/Khen Rinpoché Lekshé Jorden.jpg', entity: 'Khen Rinpoché Lekshé Jorden' },
    { file: 'to be sorted/Khen Rinpoché Pema Tsewang Lhundrup (Khenpo Petsé).jpeg', entity: 'Khen Rinpoché Pema Tsewang Lhundrup (Khenpo Petsé)' },
    { file: 'to be sorted/Khenchen Gönpo.jpg', entity: 'Khenchen Gönpo' },
    { file: 'to be sorted/Khenchen Kunzang Palden Chodrak.jpg', entity: 'Khenchen Kunzang Palden Chodrak' },
    { file: 'to be sorted/Khenchen Ngawang Palzangpo (Khenpo Ngaga).jpeg', entity: 'Khenchen Ngawang Palzangpo (Khenpo Ngaga)' },
    { file: 'to be sorted/Khenpo Tsöndrü.jpeg', entity: 'Khenpo Tsöndrü' },
    { file: 'to be sorted/Khunu Rinpoché Tendzin Gyaltsen.jpeg', entity: 'Khunu Rinpoché Tendzin Gyaltsen' },
    { file: 'to be sorted/Kunzang Mingyur Paldron_HAR.jpg', entity: 'Kunzang Mingyur Paldron' },
    { file: 'to be sorted/Lhatsün Namkha Jigmé.jpg', entity: 'Lhatsün Namkha Jigmé' },
    { file: 'to be sorted/Lotsawa Chöpal Gyatso (Lochen Dharma Shri).png', entity: 'Lotsawa Chöpal Gyatso (Lochen Dharma Shri)' },
    { file: 'to be sorted/Mewa Khenchen Tupten.jpeg', entity: 'Mewa Khenchen Tupten' },
    { file: 'to be sorted/Nyoshul Khenpo Jamyang Dorjé.jpeg', entity: 'Nyoshul Khenpo Jamyang Dorjé' },
    { file: 'to be sorted/Palpung Tai Situ Rinpoché Pema Wangchok Gyalpo.jpg', entity: 'Palpung Tai Situ Rinpoché Pema Wangchok Gyalpo' },
    { file: 'to be sorted/Paltrul Orgyen Jigme Chokyi Wangpo_from Lotsawa House.jpg', entity: 'Paltrul Orgyen Jigmé Chokyi Wangpo' },
    { file: 'to be sorted/Polu Khen Rinpoché Dorjé.jpeg', entity: 'Polu Khen Rinpoché Dorjé' },
    { file: 'to be sorted/Rahor Khenchen Tupten.jpeg', entity: 'Rahor Khenchen Tupten' },
    { file: 'to be sorted/Rigdzin Jigmé Lingpa.jpeg', entity: 'Rigdzin Jigmé Lingpa' },
    { file: 'to be sorted/Sungtrul Kunzang Nyima.jpg', entity: 'Sungtrul Kunzang Nyima' },
    { file: 'to be sorted/Taklung Tsetrul Rinpoché.jpg', entity: 'Taklung Tsetrul Rinpoché' },
    { file: 'to be sorted/Terchen Gyurme Dorje.jpeg', entity: 'Terchen Gyurmé Dorjé' },
    { file: 'to be sorted/Terchen Lerab Lingpa (Tertön Sogyal).jpeg', entity: 'Terchen Lerab Lingpa (Tertön Sogyal)' },
    { file: 'to be sorted/Tromgé Choktrul Arik Rinpoché.jpg', entity: 'Tromgé Choktrul Arik Rinpoché' },
    { file: 'to be sorted/Washul Mewai Khenchen Tsewang Rigdzin.jpg', entity: 'Washul Mewai Khenchen Tsewang Rigdzin' },
    { file: 'to be sorted/Zhabkar Tsokdruk Rangdrol.jpeg', entity: 'Zhabkar Tsokdruk Rangdrol' },
    { file: 'to be sorted/Zhenga Dorjé Chang Zhenpen Chökyi Nangwa.jpg', entity: 'Zhenga Dorjé Chang Zhenpen Chökyi Nangwa' }
];

// Normalize text (same as in index.html)
function normalizeText(text) {
    return text
        .toLowerCase()
        // Remove diacritics
        .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
        // Handle special characters
        .replace(/[āàáâãäå]/g, 'a')
        .replace(/[èéêë]/g, 'e')
        .replace(/[ìíîï]/g, 'i')
        .replace(/[òóôõö]/g, 'o')
        .replace(/[ùúûü]/g, 'u')
        .replace(/[ñ]/g, 'n')
        .replace(/[ç]/g, 'c')
        // Tibetan special chars
        .replace(/[ḍ]/g, 'd')
        .replace(/[ṭ]/g, 't')
        .replace(/[ṅ]/g, 'n')
        .replace(/[ṣ]/g, 's')
        .replace(/[ṃ]/g, 'm')
        .replace(/[ś]/g, 's')
        .replace(/[ñ]/g, 'n')
        .replace(/[ī]/g, 'i')
        .replace(/[ū]/g, 'u')
        .replace(/[ö]/g, 'o')
        .replace(/[ä]/g, 'a')
        // Remove slashes, quotes, dots, and special chars
        .replace(/[\/\"\'\.\(\),]/g, '')
        // Replace spaces and hyphens with single hyphen
        .replace(/[\s\-]+/g, '-')
        // Remove any remaining non-alphanumeric (except hyphens)
        .replace(/[^a-z0-9\-]/g, '')
        // Remove leading/trailing hyphens
        .replace(/^-+|-+$/g, '');
}

// Get next available number for an entity
async function getNextImageNumber(entitySlug, optimizedDir) {
    try {
        const files = await fs.readdir(optimizedDir);
        const pattern = new RegExp(`^${entitySlug.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}-(\\d+)\\.jpg$`);

        let maxNumber = 0;
        for (const file of files) {
            const match = file.match(pattern);
            if (match) {
                const num = parseInt(match[1]);
                if (num > maxNumber) {
                    maxNumber = num;
                }
            }
        }

        return maxNumber + 1;
    } catch (error) {
        return 1;
    }
}

// Process all images
async function processImages() {
    const sourceDir = './images/from google drive Dzogchen lineage tree images';
    const originalsDir = './images/originals';
    const optimizedDir = './images/optimized';
    const tempDir = './images/temp-processing';

    console.log('🖼️  Processing 74 new Buddhist lineage images...\n');

    // Create temp directory
    await fs.mkdir(tempDir, { recursive: true });

    let processed = 0;
    let errors = [];

    for (const mapping of IMAGE_MAPPINGS) {
        try {
            const sourcePath = path.join(sourceDir, mapping.file);
            const entitySlug = normalizeText(mapping.entity);
            const nextNumber = await getNextImageNumber(entitySlug, optimizedDir);
            const filename = `${entitySlug}-${nextNumber}.jpg`;

            // Preserve original extension for originals folder
            const sourceExt = path.extname(mapping.file);
            const originalsFilename = `${entitySlug}-${nextNumber}${sourceExt}`;

            const originalsPath = path.join(originalsDir, originalsFilename);
            const tempPath = path.join(tempDir, originalsFilename);

            // Copy to originals (high quality backup)
            await fs.copyFile(sourcePath, originalsPath);

            // Copy to temp for processing
            await fs.copyFile(sourcePath, tempPath);

            processed++;
            console.log(`✓ ${processed}/74: ${mapping.entity} → ${filename}`);

        } catch (error) {
            errors.push({ mapping, error: error.message });
            console.log(`✗ Error processing ${mapping.file}: ${error.message}`);
        }
    }

    console.log(`\n📊 Summary:`);
    console.log(`   Copied to originals: ${processed}`);
    console.log(`   Errors: ${errors.length}`);
    console.log(`\n💡 Next steps:`);
    console.log(`   1. Run: cd images/temp-processing && node ../../optimize-images.js`);
    console.log(`   2. Move optimized files to images/optimized/`);
    console.log(`   3. Clean up temp directory`);
    console.log(`   4. Run: npm run generate-manifest`);

    if (errors.length > 0) {
        console.log(`\n❌ Errors encountered:`);
        errors.forEach(e => console.log(`   - ${e.mapping.file}: ${e.error}`));
    }
}

// Run
processImages().catch(error => {
    console.error('Fatal error:', error);
    process.exit(1);
});
