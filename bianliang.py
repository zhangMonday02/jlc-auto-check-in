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
    msg_lines = ["【环境变量检查报告】\n"]
    
    print("正在读取环境变量...", flush=True)
    
    for key in env_keys:
        value = os.getenv(key)
        if value:
            # 不脱敏，直接显示
            msg_lines.append(f"**{key}**:\n{value}")
        else:
            msg_lines.append(f"**{key}**: [未设置]")
        msg_lines.append("\n" + "-" * 20 + "\n")

    full_content = "\n".join(msg_lines)
    print(full_content)

    # 获取 Server酱 SCKEY 用于发送
    serverchan_sckey = os.getenv('SERVERCHAN_SCKEY')

    if not serverchan_sckey:
        print("\n❌ 错误：未找到 SERVERCHAN_SCKEY 环境变量，无法推送到Server酱。")
        sys.exit(1)

    # 构造 Server酱发送逻辑
    try:
        url = f"https://sctapi.ftqq.com/{serverchan_sckey}.send"
        
        # Server酱接收 title 和 desp 参数
        data = {
            "title": "环境变量导出",
            "desp": full_content
        }
        
        print(f"\n正在推送到Server酱...", flush=True)
        response = requests.post(url, data=data)
        
        if response.status_code == 200:
            try:
                res_json = response.json()
                # Server酱通常返回 code:0 表示成功
                if res_json.get('code') == 0:
                    print("✅ Server酱推送成功")
                else:
                    print(f"❌ Server酱推送可能失败，API返回: {res_json}")
            except:
                # 某些旧版接口可能不返回标准JSON，只要200就算发送了
                print("✅ Server酱推送请求已发送")
        else:
            print(f"❌ Server酱推送失败，HTTP状态码: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 发送过程中发生异常: {e}")

if __name__ == "__main__":
    main()
