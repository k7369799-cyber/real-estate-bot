#!/usr/bin/env python3
"""
GitHub Actions용 부동산 알림 봇
"""

import os
import requests
from datetime import datetime
import random
import time

class GitHubRealEstateBot:
    def __init__(self):
        # 환경변수에서 토큰과 챗ID 가져오기
        self.bot_token = os.environ.get('BOT_TOKEN')
        self.chat_id = os.environ.get('CHAT_ID')
        self.telegram_api = f"https://api.telegram.org/bot{self.bot_token}"
        
        # 모니터링할 지역들
        self.regions = [
            {"name": "안양시", "emoji": "🏘️"},
            {"name": "과천시", "emoji": "🌳"}, 
            {"name": "의왕시", "emoji": "🚄"},
            {"name": "군포시", "emoji": "🏞️"},
            {"name": "수원시", "emoji": "🏛️"},
            {"name": "성남시", "emoji": "🌆"},
            {"name": "용인시", "emoji": "🎡"}
        ]

    def send_message(self, text):
        """텔레그램 메시지 전송"""
        url = f"{self.telegram_api}/sendMessage"
        data = {
            'chat_id': self.chat_id,
            'text': text,
            'parse_mode': 'HTML'
        }
        
        try:
            response = requests.post(url, data=data)
            if response.json().get('ok'):
                print("✅ 메시지 전송 성공!")
                return True
            else:
                print("❌ 메시지 전송 실패!")
                return False
        except Exception as e:
            print(f"오류: {e}")
            return False

    def get_sample_properties(self, region_name):
        """샘플 매물 데이터 생성"""
        property_count = random.randint(0, 6)
        properties = []
        
        locations = ["중앙동", "신도시", "구시가지", "역세권", "아파트촌", "단독주택가"]
        sources = ["네이버부동산", "직방", "다방", "부동산114", "원룸원"]
        
        # 정확한 가격 리스트
        price_options = [
            "1억원", 
            "1억 1000만원", "1억 2000만원", "1억 3000만원", "1억 4000만원", "1억 5000만원",
            "1억 6000만원", "1억 7000만원", "1억 8000만원", "1억 9000만원",
            "1억 1500만원", "1억 2500만원", "1억 3500만원", "1억 4500만원", "1억 5500만원",
            "1억 6500만원", "1억 7500만원", "1억 8500만원", "1억 9500만원",
            "1억 1200만원", "1억 1800만원", "1억 2300만원", "1억 2800만원", "1억 3200만원",
            "1억 3800만원", "1억 4200만원", "1억 4800만원", "1억 5200만원", "1억 5800만원"
        ]
        
        # 전용면적 옵션
        area_options = [18, 19, 20, 21, 22, 23, 24]
        
        for i in range(property_count):
            selected_area = random.choice(area_options)
            
            properties.append({
                "price": random.choice(price_options),
                "area": f"{selected_area}평(전용)",
                "rooms": "방3개/화장실2개", 
                "location": f"{region_name} {random.choice(locations)}",
                "type": random.choice(["빌라", "다세대", "연립"]),
                "floor": f"{random.randint(1, 4)}층/{random.randint(2, 5)}층",
                "source": random.choice(sources)
            })
        
        return properties

    def send_daily_update(self):
        """일일 업데이트 전송"""
        try:
            print(f"=== GitHub Actions 일일 리포트 시작 ===")
            
            # 헤더 메시지
            today = datetime.now()
            header_msg = f"""
🏠 <b>경기도 전세 매물 알림</b>
📅 {today.strftime("%Y년 %m월 %d일")} ({today.strftime("%A")})
⏰ {today.strftime("%H:%M")} 업데이트
☁️ <i>GitHub Actions 자동 실행</i>
"""
            self.send_message(header_msg)
            time.sleep(2)
            
            total_count = 0
            
            # 지역별 개별 메시지
            for region in self.regions:
                properties = self.get_sample_properties(region["name"])
                count = len(properties)
                total_count += count
                
                emoji = region["emoji"]
                name = region["name"]
                
                if count > 0:
                    region_msg = f"{emoji} <b>{name}</b> <code>({count}건)</code>\n"
                    
                    for i, prop in enumerate(properties, 1):
                        region_msg += f"\n   {i}. <b>{prop['price']}</b> | {prop['area']}\n"
                        region_msg += f"      🏠 {prop['type']} | {prop['rooms']}\n" 
                        region_msg += f"      📍 {prop['location']} | {prop['floor']}\n"
                        region_msg += f"      📱 출처: {prop['source']}\n"
                        
                        if i < len(properties):
                            region_msg += f"      ─────────────────────\n"
                    
                    self.send_message(region_msg)
                    time.sleep(2)
                else:
                    no_property_msg = f"{emoji} {name}: <i>신규 매물 없음</i>"
                    self.send_message(no_property_msg)
                    time.sleep(1)
            
            # 요약 메시지
            summary_msg = f"""
━━━━━━━━━━━━━━━━━━━━
📊 <b>총 {total_count}건의 신규 매물</b>

📱 <b>정보 출처:</b> 네이버부동산, 직방, 다방, 부동산114, 원룸원
💡 <i>정확한 정보는 해당 사이트에서 직접 확인하세요!</i>
🔄 <i>다음 업데이트: 내일 오전 9시</i>
☁️ <i>Powered by GitHub Actions</i>
"""
            self.send_message(summary_msg)
            
            print("✅ GitHub Actions 일일 리포트 전송 완료!")
                
        except Exception as e:
            error_msg = f"❌ <b>GitHub Actions 오류</b>\n\n{str(e)}\n\n⏰ {datetime.now().strftime('%H:%M:%S')}"
            self.send_message(error_msg)
            print(f"오류: {e}")

def main():
    """메인 실행"""
    bot = GitHubRealEstateBot()
    
    if not bot.bot_token or not bot.chat_id:
        print("❌ 환경변수 BOT_TOKEN과 CHAT_ID를 설정해주세요.")
        return
    
    try:
        bot.send_daily_update()
    except Exception as e:
        print(f"❌ 봇 실행 중 오류: {e}")

if __name__ == "__main__":
    main()
