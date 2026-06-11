import * as lark from '@larksuiteoapi/node-sdk';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import qrcode from 'qrcode-terminal';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ENV_PATH = path.resolve(__dirname, '..', '.env');

async function main() {
    console.log('='.repeat(50));
    console.log('🔑 飞书一键创建应用');
    console.log('   扫码后自动获取 App ID / App Secret');
    console.log('='.repeat(50));
    console.log();

    try {
        const result = await lark.registerApp({
            onQRCodeReady(info) {
                console.log(`⏳ 二维码已生成 (有效期 ${info.expireIn} 秒)`);
                console.log('📱 请用飞书扫描下方二维码（或在浏览器打开链接）:\n');
                
                // 终端二维码
                qrcode.generate(info.url, { small: true });
                
                console.log(`\n🔗 链接: ${info.url}`);
                console.log();
            },
            onStatusChange(info) {
                const statusMap = {
                    'polling': '等待扫码...',
                    'slow_down': '轮询降速中...',
                    'domain_switched': '域名已切换'
                };
                process.stdout.write(`  📡 ${statusMap[info.status] || info.status}\r`);
            },
            appPreset: {
                name: '灵感收集 {user}',
                desc: '将飞书聊天中的灵感一键转化为结构化知识文档',
            }
        });

        console.log('\n\n✅ 应用创建成功！');
        console.log(`  App ID:     ${result.client_id}`);
        console.log(`  App Secret: ${result.client_secret}`);
        if (result.user_info) {
            console.log(`  扫码用户:   ${result.user_info.open_id}`);
        }

        // 写入 .env 文件
        const envContent = `# 飞书 Bot 配置 (由 registerApp 自动创建)
FEISHU_APP_ID=${result.client_id}
FEISHU_APP_SECRET=${result.client_secret}
FEISHU_VERIFY_TOKEN=feishu_inspiration_${Date.now().toString(36)}

# 服务端口
PORT=5676
`;
        fs.writeFileSync(ENV_PATH, envContent, 'utf-8');
        console.log(`\n💾 配置已写入: ${ENV_PATH}`);

        console.log('\n📋 接下来步骤:');
        console.log('  1. 重启飞书 Bot 使配置生效:');
        console.log('     python _scripts/feishu_bot.py');
        console.log('  2. 去飞书开放平台配置事件订阅:');
        console.log('     应用 → 事件订阅 → 添加事件 → im.message.receive_v1');
        console.log('     回调地址: http://你的公网IP:5676/feishu/webhook');
        console.log('  3. 权限管理 → 添加 → im:message');
        console.log('  4. 发布 → 创建版本 → 上线');
        console.log('  5. 在飞书搜索"灵感收集"即可开始使用');
        console.log();

    } catch (e) {
        console.error('\n❌ 创建失败');
        console.error(`   错误: ${e.code || 'unknown'}`);
        console.error(`   详情: ${e.description || e.message}`);
        process.exit(1);
    }
}

main();
