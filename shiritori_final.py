import sys, bs4, requests, random

hiragana_list = "ぁあぃいぅうぇえぉおかがきぎくぐけげこごさざしじすずせぜそぞただちぢっつづてでとどなにぬねのはばぱひびぴふぶぷへべぺほぼぽまみむめもゃやゅゆょよらりるれろゎわゐゑをんー"
hiragana_small = "ぁぃぅぇぉっゃゅょゎ"
hiragana_big = "あいうえおつやゆよわ"

WordList = [] #グローバル変数の単語リスト

def getWord(tanngo): #単語取得。
	while True:
		if tanngo == 'first':
			print('文字列を入力してください')
			mojiretsu=input()
			if not all([ch in hiragana_list for ch in mojiretsu]):
				print('入力文字列がひらがなではありません')
				continue
			if mojiretsu[0] in hiragana_small:
				print('入力文字列が小文字で始まっています')
				continue
			if mojiretsu[0] == "ん":
				print('入力文字列が"ん"で始まっています')
				continue
			if mojiretsu[0] == "ー":
				print('入力文字列が"ー"で始まっています')
				continue
			break
		else:
			print(tanngo[-1]+'で始まる文字列を入力してください')
			mojiretsu=input()
			if not all([ch in hiragana_list for ch in mojiretsu]):
				print('入力文字列がひらがなではありません')
				continue
			if mojiretsu[0] != tanngo[-1]:
				print('頭文字が一致しません')
				continue
			break
	return mojiretsu

def replace(word): #辞書登録用。ひらがなや伸ばし棒を変える役割も兼ねている
	boin_dic = {'あ':'あ','い':'い','う':'う','え':'え','お':'お',
				'か':'あ','き':'い','く':'う','け':'え','こ':'お',
				'さ':'あ','し':'い','す':'う','せ':'え','そ':'お',
				'た':'あ','ち':'い','つ':'う','て':'え','と':'お',
				'な':'あ','に':'い','ぬ':'う','ね':'え','の':'お',
				'は':'あ','ひ':'い','ふ':'う','へ':'え','ほ':'お',
				'ま':'あ','み':'い','む':'う','め':'え','も':'お',
				'や':'あ','ゆ':'う','よ':'お',
				'ら':'あ','り':'い','る':'う','れ':'え','ろ':'お',
				'わ':'あ','ゐ':'い','ゑ':'え','を':'お',
				'が':'あ','ぎ':'い','ぐ':'う','げ':'え','ご':'お',
				'ざ':'あ','じ':'い','ず':'う','ぜ':'え','ぞ':'お',
				'だ':'あ','ぢ':'い','づ':'う','で':'え','ど':'お',
				'ば':'あ','び':'い','ぶ':'う','べ':'え','ぼ':'お',
				'ぱ':'あ','ぴ':'い','ぷ':'う','ぺ':'え','ぽ':'お'}
	for i in range(len(hiragana_small)):
		if word[-1] == hiragana_small[i]:
			word=word.replace(word[-1], hiragana_big[i])
	if word[-1] == "ー":
		word=word.replace(word[-1], boin_dic[word[-2]])

	WordList.append(word)

	return word

def choiceWord(dic, words):
	try:
		word = random.choice(words) #単語をランダムに選択。
	except:
		return ('こうさん') #1つもなければ降参する

	while word[-1] not in dic.keys(): #最後の文字が50音になければ
		word =  choiceWord(dic, words) #単語を取り直す。

	return word

def wordInDic(word):
	URL = 'https://ejje.weblio.jp/content/' + word #辞書で単語を検索
	res = requests.get(URL) #URLから情報を取得
	try:
		res.raise_for_status() #エラー処理
	except:
		print('Error')
		quit()
	response = bs4.BeautifulSoup(res.content, "html.parser") #htmlを取得
	#requestsは<meta>タグのエンコーディングは見ません。
	#Content-Typeを指定しないとISO-8859-1でデコードされます。
	#よって日本語URLのr.textが文字化けします
	#res.contentにすることでBeautifulSoup側で<meta>タグからデコードしています。
	table_infos = response.select('#h1Query') #検索結果が1件でもあれば出現する部分。
	try:
		result = table_infos[0].getText() #エラーが出るか否かで検索結果があるか判定。
	except:
		return False

	return True


def returnWord(head):
	dic = {'あ':'00','い':'01','う':'02','え':'03','お':'04',
	'か':'05','き':'06','く':'07','け':'08','こ':'09',
	'さ':'10','し':'11','す':'12','せ':'13','そ':'14',
	'た':'15','ち':'16','つ':'17','て':'18','と':'19',
	'な':'20','に':'21','ぬ':'22','ね':'23','の':'24',
	'は':'25','ひ':'26','ふ':'27','へ':'28','ほ':'29',
	'ま':'30','み':'31','む':'32','め':'33','も':'34',
	'や':'35','ゆ':'37','よ':'39',
	'ら':'40','り':'41','る':'42','れ':'43','ろ':'44',
	'わ':'45','ゐ':'01','ゑ':'03','を':'04','ん':'-1',
	'が':'05','ぎ':'06','ぐ':'07','げ':'08','ご':'09',
	'ざ':'10','じ':'11','ず':'12','ぜ':'13','ぞ':'14',
	'だ':'15','ぢ':'16','づ':'17','で':'18','ど':'19',
	'ば':'25','び':'26','ぶ':'27','べ':'28','ぼ':'29',
	'ぱ':'25','ぴ':'26','ぷ':'27','ぺ':'28','ぽ':'29'}
	URL = 'https://www.jfd.or.jp/books/cat/wata-index/alph' + dic[head] #頭文字を選んだURL
	res = requests.get(URL) #URLから情報を取得
	try:
		res.raise_for_status() #エラー処理
	except:
		print('Error')
		quit()
	response = bs4.BeautifulSoup(res.content, "html.parser") #htmlを取得
	table_infos = response.select('td') #tdタグの単語を取得。
	words = [num for num in range(1,len(table_infos),4)] #tdタグからフリガナのみを抽出
	newwords = []
	for num in words:
		if table_infos[num].getText()[0] == head: #濁点対策。頭文字が一致していたら
			if table_infos[num].getText() not in WordList: #その単語が未使用なら
				newwords.append(table_infos[num].getText()) #未使用の単語リストを作成。
	word = choiceWord(dic, newwords) #ランダムに単語を選択。
	for i in range(2):
		if word[-1] == 'ん':
			word = choiceWord(dic, newwords) #ランダムに単語を選択しなおす。ん の確率を下げる。
	return(word)


mojiretsu = getWord('first') #1回目
if mojiretsu[-1] == "ん":
	print('入力文字列が"ん"で終わっています')
	print('あなたの負け')
	sys.exit()
if wordInDic(mojiretsu) == False:
	print('辞書にありません')
	print('あなたの負け')
	sys.exit()#check

while True: #2回目以降
	mojiretsu = replace(mojiretsu) #辞書に登録
	tanngo=returnWord(mojiretsu[-1]) #返す単語を取得
	print(tanngo) #単語を返す
	if tanngo[-1] == "ん":
		print('相手の文字列が"ん"で終わっています')
		print('あなたの勝ち！')
		sys.exit()
	tanngo = replace(tanngo) #辞書に登録
	mojiretsu = getWord(tanngo)
	if mojiretsu in WordList:
		print('その文字列は使用済みです')
		print('あなたの負け')
		sys.exit()
	if mojiretsu[-1] == "ん":
		print('入力文字列が"ん"で終わっています')
		print('あなたの負け')
		sys.exit()
	if wordInDic(mojiretsu) == False:
		print('辞書にありません')
		print('あなたの負け')
		sys.exit()#check
