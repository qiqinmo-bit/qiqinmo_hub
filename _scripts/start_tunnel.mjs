import localtunnel from 'localtunnel';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function startTunnel() {
    try {
        const tunnel = await localtunnel({ port: 5676 });
        const url = tunnel.url;
        console.log(`✅ Tunnel: ${url}`);
        console.log(`✅ Callback: ${url}/feishu/webhook`);
        fs.writeFileSync(path.join(__dirname, '..', 'tunnel_url.txt'), url);

        tunnel.on('close', () => {
            console.log('⚠️ Tunnel closed');
        });
    } catch (e) {
        console.error('❌ Tunnel error:', e.message);
        process.exit(1);
    }
}

startTunnel();
