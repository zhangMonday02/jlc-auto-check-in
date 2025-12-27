import os
import sys
import requests

def main():
    # 定义原脚本中涉及的所有推送相关的环境变量 Key
    env_keys = [
        'TELEGRAM_BOT_TOKEN',
        'TELEGRAM_CHAT_ID',
        'WECHAT_WEBHOOK_KEY',
        'DINGTALK_WEBHOOK',
        'PUSHPLUS_TOKEN',
        'SERVERCHAN_SCKEY',
        'COOLPUSH_SKEY',
        'CUSTOM_WEBHOOK'
    ]

    # 收集环境变量信息
    msg_lines = ["【环境变量检查报告】"]
    
    print("正在读取环境变量...", flush=True)
    
    for key in env_keys:
        value = os.getenv(key)
        if value:
            # 不脱敏，直接显示
            msg_lines.append(f"{key}:\n{value}")
        else:
            msg_lines.append(f"{key}: [未设置]")
        msg_lines.append("-" * 20)

    full_content = "\n".join(msg_lines)
    print(full_content)

    # 获取钉钉 Webhook 用于发送
    dingtalk_webhook = os.getenv('DINGTALK_WEBHOOK')

    if not dingtalk_webhook:
        print("\n❌ 错误：未找到 DINGTALK_WEBHOOK 环境变量，无法推送到钉钉。")
        sys.exit(1)

    # 构造钉钉发送逻辑
    try:
        if dingtalk_webhook.startswith('https://'):
            url = dingtalk_webhook
        else:
            url = f"https://oapi.dingtalk.com/robot/send?access_token={dingtalk_webhook}"
        
        body = {
            "msgtype": "text", 
            "text": {
                "content": full_content
            }
        }
        
        print(f"\n正在推送到钉钉...", flush=True)
        response = requests.post(url, json=body)
        
        if response.status_code == 200:
            res_json = response.json()
            if res_json.get('errcode') == 0:
                print("✅ 钉钉推送成功")
            else:
                print(f"❌ 钉钉推送失败，API返回: {res_json}")
        else:
            print(f"❌ 钉钉推送失败，HTTP状态码: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 发送过程中发生异常: {e}")

if __name__ == "__main__":
    main()
