# coding:utf-8
import jieba  #分词
import  matplotlib.pyplot as plt #数据可视化
import wordcloud
from  wordcloud import WordCloud,ImageColorGenerator,STOPWORDS #词云
import numpy  as np  #科学计算
from PIL import Image  #处理图片

def outputCiyun():
    #打开文本
    textfile=open("info.txt").read().decode(encoding='utf-8') #读取文本内容
    textfile=textfile.replace("font","").replace("family","").replace("size","").replace("Arial","")
    textfile=textfile.replace("eb","").replace("BR","").replace("height","").replace("white","")
    textfile=textfile.replace("space","").replace("fareast","").replace("style","").replace("line","")
    textfile=textfile.replace("size","").replace("nbsp","").replace("rgb","").replace("color","")
    textfile=textfile.replace("13px","").replace("sans serif","").replace('bidi',"").replace(u"类别","").replace(u"描述","")
    textfile=textfile.replace(u"职位","").replace(u"职能","").replace(u'上学',"").replace(u"学历","").replace(u"要求","")
    textfile=textfile.replace(u"关键","").replace(u"至少","").replace(u'一种',"").replace(u"关键字","").replace(u"任职","")
    wordlist=jieba.cut_for_search(textfile)
    space_list=" ".join(wordlist)#链接词语
    backgroud=np.array(Image.open("2.jpg")) #背景图片
    mywordcloud=WordCloud(width=1400, height=700,background_color="black", #背景颜色
                          mask=backgroud,#写字用的背景图，从背景图取颜色
                          max_words=200,  #最大词语数量
                          stopwords=STOPWORDS, #停止的默认词语
                          font_path="simkai.ttf", #字体
                          max_font_size=200, #最大字体尺寸
                          random_state=50,#随机角度
                          scale=2).generate(space_list) #生成词云

    image_color=ImageColorGenerator(backgroud) #生成词云的颜色
    plt.axis("off")
    plt.imshow(mywordcloud) #显示词云
    plt.savefig(u"ciyun.jpg") #保存

    # plt.show()