from flask import Flask, jsonify, render_template,request
import requests 


app = Flask(__name__)

choosemap = {
    "不設定": ["不設定"],
    "消逝的旅途": ["風化的開心之地","風化的開心與憤怒之地","風化的憤怒之地","風化的憤怒與悲傷之地","風化的悲傷之地","風化的悲傷與歡樂之地","風化的歡樂之地","隱藏的湖水邊","岩石領土","岩石和火焰領土","火焰領土","火焰和靈魂領土","靈魂領土","隱藏的火焰地帶","三岔路1","洞穴西側路1","洞穴西側路2","洞穴東側路1","洞穴東側路2","三岔路2","洞穴下側","洞穴上側","洞穴深處","亞勒瑪隱身處","隱藏的洞穴"
],
    "反轉城市": ["地下線路1","地下線路2","地下線路3","地下線路4","地下線路5","地下線路6","T-boy的研究列車1","T-boy的研究列車2","T-boy的研究列車3","隱藏研究列車","地下列車1","地下列車2","地下列車3","隱藏地下列車","地上列車1","地上列車2","地上列車3","隱藏M高塔","M高塔2","M高塔3","M高塔4"
],
    "啾啾艾爾蘭": ["瀑布下側","激流地帶3","激流地帶2","激流地帶1","啾啾村入口","鯨魚山入口","鯨魚山山腰1","鯨魚山山腰2","鯨魚山山頂","巨大的尾巴","園林入口","繽紛森林地帶1","繽紛森林地帶2","繽紛森林地帶3","五色園林深處","橢圓森林1","橢圓森林2","正圓森林1","正圓森林2","揪樂森林深處"
],
    "嚼嚼艾爾蘭": ["香菇森林3","香菇森林2","香菇森林1","香菇森林4","香菇森林5","香菇森林6","隱藏香菇森林","伊利亞特平原6","伊利亞特平原5","伊利亞特平原4","伊利亞特平原1","伊利亞特平原2","伊利亞特平原3","隱藏伊利亞特平原","蘑菇鳥森林6","蘑菇鳥森林5","蘑菇鳥森林4","蘑菇鳥森林3","蘑菇鳥森林2","蘑菇鳥森林1","隱藏蘑菇鳥森林"
],
    "拉契爾恩": ["優勝碟的街道2","優勝碟的街道1","雞群遊樂場3","雞群遊樂場2","雞群遊樂場1","顯露本色之處1","顯露本色之處2","顯露本色之處3","跳舞鞋佔領地1","跳舞鞋佔領地2","不法者街道1","不法者街道2","不法者街道3","惡夢時間塔1樓","惡夢時間塔2樓","惡夢時間塔3樓","惡夢時間塔4樓","惡夢時間塔5樓"
],
    "阿爾卡娜": ["水之森","日光之森","土之森","水和日光之森","日光和土之森","霜雲之森","雷雲之森","猛毒之森","爆破之森","霜與雷之森1","霜與雷之森2","猛毒與爆破之森1","猛毒與爆破之森2","洞穴的上路","洞穴的上路深處1","洞穴的上路深處2","洞穴的上路深淵處","洞穴的下路","洞穴的下路深處1","洞穴的下路深處2","洞穴的下路深淵處","五道洞穴","五道洞穴的上路","五道洞穴的間隔路","五道洞穴的下路","精靈之樹下面的洞穴"
],
    "魔菈斯": ["前往珊瑚之林的路2","前往珊瑚之林的路3","前往珊瑚之林的路4","賊貓出沒地","賊貓出沒地2","大哥的地盤","大哥的地盤2","大哥的地盤3","影子跳舞處2","影子跳舞處3","影子跳舞處4","封閉地區","封閉地區2","封閉地區3","那天的特雷亞非2","那天的特雷亞非3","那天的特雷亞非4"
],
    "艾斯佩拉": ["生命起始之地2","生命起始之地3","生命起始之地4","生命起始之地5","生命起始之地6","生命起始之地7","鏡光大海2","鏡光大海3","鏡光大海4","鏡光大海5","鏡光大海6","鏡光大海7","鏡光神殿2","鏡光神殿3","鏡光神殿4"
],
    "賽拉斯": ["光芒最後所及之處1","光芒最後所及之處2","光芒最後所及之處3","光芒最後所及之處4","光芒最後所及之處5","光芒最後所及之處6","光芒最後所及之處7","光芒最後所及之處8","光芒最後所及之處9","無限沉淪的深海1","無限沉淪的深海2","無限沉淪的深海3","無限沉淪的深海4","無限沉淪的深海5","無限沉淪的深海6","星星被吞噬的深海1","星星被吞噬的深海2","星星被吞噬的深海3","星星被吞噬的深海4","星星被吞噬的深海5","星星被吞噬的深海6"
],
    "月之橋": ["思想的邊境1","思想的邊境2","思想的邊境3","思想的邊境4","思想的邊境5","思想的邊境6","未知迷霧1","未知迷霧2","未知迷霧3","未知迷霧4","未知迷霧5","未知迷霧6","虛空海浪1","虛空海浪2","虛空海浪3","虛空海浪4","虛空海浪5","虛空海浪6"
],
    "苦痛迷宮": ["苦痛迷宮內部1","苦痛迷宮內部2","苦痛迷宮內部3","苦痛迷宮內部4","苦痛迷宮內部5","苦痛迷宮內部6","苦痛迷宮中心地帶1","苦痛迷宮中心地帶2","苦痛迷宮中心地帶3","苦痛迷宮中心地帶4","苦痛迷宮中心地帶5","苦痛迷宮中心地帶6","苦痛迷宮中心地帶7","苦痛迷宮最深處1","苦痛迷宮最深處2","苦痛迷宮最深處3","苦痛迷宮最深處4","苦痛迷宮最深處5","苦痛迷宮最深處6"
],
    "利曼": ["世界的眼淚下方1", "世界的眼淚下方2", "世界的眼淚下方3", "世界的眼淚中段1", "世界的眼淚中段2", "世界的眼淚中段3", "世界的眼淚中間點4", "世界終結之處 1-4", "世界終結之處 1-5", "世界終結之處 1-6", "世界終結之處 1-7", "世界終結之處 1-8", "世界終結之處 1-9", "世界終結之處 2-3", "世界終結之處 2-4", "世界終結之處 2-5", "世界終結之處 2-6", "世界終結之處 2-7", "世界終結之處 2-8"
],
#     "賽爾尼溫": ["海邊岩石地帶1", "海邊岩石地帶2", "海邊岩石地帶3", "海邊岩石地帶4", "賽爾尼溫西方城牆1", "賽爾尼溫西方城牆2", "賽爾尼溫西方城牆3", "賽爾尼溫東邊城牆1", "賽爾尼溫東邊城牆2", "賽爾尼溫東邊城牆3", "王立圖書館第1區域", "王立圖書館第2區域", "王立圖書館第3區域", "王立圖書館第4區域", "王立圖書館第5區域", "王立圖書館第6區域"
# ],
#     "燃燒的賽爾尼溫": ["決戰的西方城牆4", "決戰的西方城牆3", "決戰的西方城牆2", "決戰的西方城牆1", "決戰的東邊城牆1", "決戰的東邊城牆2", "決戰的東邊城牆3", "決戰的東邊城牆4", "決戰的東邊城牆5", "決戰的東邊城牆6", "燃燒的王立圖書館第1區域", "燃燒的王立圖書館第2區域", "燃燒的王立圖書館第3區域", "燃燒的王立圖書館第4區域", "燃燒的王立圖書館第5區域", "燃燒的王立圖書館第6區域"
# ],
#     "飯店阿爾克斯": ["沒有目的地的橫貫列車6", "沒有目的地的橫貫列車5", "沒有目的地的橫貫列車4", "沒有目的地的橫貫列車3", "沒有目的地的橫貫列車2", "沒有目的地的橫貫列車1", "不法之徒所支配的荒野1", "不法之徒所支配的荒野2", "不法之徒所支配的荒野3", "不法之徒所支配的荒野4", "浪漫日落的汽車戲院1", "浪漫日落的汽車戲院2", "浪漫日落的汽車戲院3", "浪漫日落的汽車戲院4", "浪漫日落的汽車戲院5", "浪漫日落的汽車戲院6"
# ],
    "200等以下": ["奇幻村-寧靜的沼澤","納希沙漠-沉睡沙漠","神木村-天空之巢II","玩具城-扭曲的迴廊","地球防衛本部-走廊H01","黃昏的勇士之村-被遺棄的挖掘地區2","黃昏的勇士之村-暴風峽谷","黃昏的勇士之村-蕭瑟的北側岩石路","黃昏的勇士之村-挖掘中斷地區","黃昏的勇士之村-封閉地區","星光之塔-2樓咖啡廳<4>","星光之塔-2樓咖啡廳<5>","星光之塔-3樓文具店<4>","星光之塔-3樓文具店<5>","星光之塔-4樓唱片店<4>","星光之塔-4層音樂賣場<5>","星光之塔-5樓化妝品店<4>","星光之塔-5層化妝品賣場<5>","星光之塔-6樓髮廊<4>","星光之塔-6層美容室<5>"
]
}
channeldata = ["1S", "2S", "3S", "4S", "5S", "6S", "7S", "8S", "9S", "10S", "11S", "12S", "13S", "14S", "15S", "16S", "17S", "18S", "19S", "20S", "21S", "22S", "23S", "24S", "25S", "26S", "27S", "28S", "29S", "30S"]
timelongdata = ["0.5H", "1H", "1.5H", "2H", "3H", "4H", "活動輪(15分鐘)"]




@app.route('/home/<userid>')
def home(userid):
    data = [
    "不設定",
    "消逝的旅途",
    "反轉城市",
    "啾啾艾爾蘭",
    "嚼嚼艾爾蘭",
    "拉契爾恩",
    "阿爾卡娜",
    "魔菈斯",
    "艾斯佩拉",
    "賽拉斯",
    "月之橋",
    "苦痛迷宮",
    "利曼",
    # "賽爾尼溫",
    # "燃燒的賽爾尼溫",
    # "飯店阿爾克斯",
    "200等以下"
    ]
    
    return render_template('index.html',mapdata=data,channeldata= channeldata,timelongdata=timelongdata,userid=userid)

@app.route('/')
def main():
  return 'Bot is aLive!'

@app.route('/changeselectfield/', methods=['GET', 'POST'])
def changeselectfield():
    if request.method == "POST":
        data = request.get_json()
        name = data['name']
        mapdata = choosemap[name]
        return jsonify(mapdata)
    else:
        return {}

@app.route('/getform',methods=['POST'])
def getform():
  if request.method == "POST":
    data = request.get_json()
    strr = '有表單'
    dcWebhook(strr)
    result = requests.post("https://active-lab-dominant.ngrok-free.app/dcrunefun", json=data)
    result = result.text
    return result


def dcWebhook(payload)->None:
    dcUrl = "https://discord.com/api/webhooks/1187035552877379615/ZM3wmvwKed_d7nNJytPlwd94RCwgIVsVToOMbASQfSOiS4fOm3sMc4pU5h7jZy8nQab7"
    data = {"content": str(payload)}
    requests.post(dcUrl, json=data)


if __name__ == '__main__':
    app.run()