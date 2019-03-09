from firebase import firebase
import json
with open('menu.json') as f:
    menuFile = json.load(f)
foodI = menuFile["Items"]
database = firebase.FirebaseApplication('https://cedarrestaurants-ad912.firebaseio.com/Qn4DcOURt9NUPCqctVvnpADZJe83', None)
while True:
    orders = (database.get("/Qn4DcOURt9NUPCqctVvnpADZJe83", "/cart"))
    score = 0
    score2 = 0
    scores2 = []
    total = 0
    extraBool = 0
    names = [0]
    scores = []
    itemName = []
    indexs = [0,0]
    ExtraPriceTtl = 0
    extras = []
    size = "NULL"
    ExtraName = ""
    extrasStr = []
    names[0] = (orders.keys())
    for i in range(len(orders)):
        orderNames = (names[0][i])
        if(orders[orderNames]["translated"] == 0):
            cart = (orders[orderNames]["itemCart"])
            for i in range(len(cart)):
                item = str(cart[i])
                for j in range(len(item)):
                    itemName.append(item[j].capitalize())
                    if(item[j] == ","):
                        if((item[j+1]) != " "):
                            size = (item[j+1])
                            dif = ((j+1) - len(item))
                            if(size != "s" or size != "m" or size != "l" and dif != -1):
                                itemName.pop(len(itemName) - 1)
                                extras.append(item[(j+1):])
                                break
                        elif((item[j+1]) == " "):
                            size = (item[j + 2])
                            dif = ((j + 2) - len(item))
                            if (size != "s" or size != "m" or size != "l" and dif != -1):
                                itemName.pop(len(itemName) - 1)
                                extras.append(item[(j+1):])
                                break
                for x in range(len(foodI)):
                    for y in range(len(foodI[x]["Name"])):
                        score = 0
                        food = str(foodI[x]["Name"][y])
                        indexs[0] = x
                        indexs[1] = y
                        foodName = ""
                        for xn in range(len(itemName)):
                            foodName = str(foodName +itemName[xn])
                        a = list(set(foodName) & set(food))
                        for i in a:
                            score+=1
                        scores.append([score,x])
                itemName = []
                itemS = 0
                itemIndex = 0
                for zz in range(len(scores)-1):
                    if(scores[zz][0] > itemS):
                        itemS = scores[zz][0]
                        itemIndex = scores[zz][1]
                scores = []
                putValN = str(foodI[itemIndex]["Name"][0])
                if(len(extras) > 0):
                    if(len(extras[0])>2):
                        es = ""
                        for m in range(len(extras[0])):
                            es += extras[0][m].capitalize()
                            if (extras[0][m] == ","):
                                es = es[0:-1]
                                extrasStr.append(es)
                                es = ""
                        extrasStr.append(es)
                if(len(extras) > 0):
                    if(len(extras[0])>2):
                        for xx in range(len(extrasStr)):
                            for yy in range(len(foodI[indexs[0]]["custom"])):
                                score2 = 0
                                foodx = str(foodI[indexs[0]]["custom"][yy][0])
                                valx = len(extrasStr)
                                foodName = str(extrasStr[xx])
                                zzn = list(set(foodName) & set(foodx))
                                for vvv in zzn:
                                    score2+=1
                                scores2.append([foodx,score2,yy])
                            extraS = 0
                            extraIndex = 0
                            ExtraName = ""
                            for zze in range(len(scores2)):
                                if (scores2[zze][1] > extraS):
                                    #print(scores2[zze])
                                    ExtraName += scores2[zze][0]
                                    ExtraName += ","
                                    extraS = scores2[zze][1]
                                    extrasIndex = scores2[zze][2]
                            #print(extraS,extrasIndex)
                            extraPrice = float(foodI[indexs[0]]["custom"][extrasIndex][1])
                            #print(extraPrice)
                            ExtraPriceTtl += extraPrice
                            scores2 = []
                if(str(foodI[itemIndex]["sizes"][0] != "o")):
                    if(size == "s"):
                        putValP = (foodI[itemIndex]["prices"][0])
                        putValN = putValN + " SMALL"
                    elif(size == "m"):
                        putValP = (foodI[itemIndex]["prices"][1])
                        putValN = putValN + " MEDIUM"
                    elif (size == "l"):
                        putValP = (foodI[itemIndex]["prices"][2])
                        putValN = putValN + " LARGE"
                    elif(size == "xl"):
                        putValP = (foodI[itemIndex]["prices"][3])
                        putValN = (putValN + " XLARGE")
                    else:
                        putValP = (foodI[itemIndex]["prices"][0])
                if(ExtraName != ""):
                    putValN += ","
                    putValN += ExtraName
                    putValN = putValN[:-1]
                putValP += ExtraPriceTtl
                size = "NULL"
                extras = []
                database.put("/Qn4DcOURt9NUPCqctVvnpADZJe83/cart/"+str(orderNames)+"/sortedCart/",putValN,putValP)
                total += float(putValP)
                ExtraPriceTtl = 0
                ExtraName = ""
            total = round(total,2)
            tax = round(total * 0.1 ,2)
            taxTotal = round(total*1.1, 2)
            database.put("/Qn4DcOURt9NUPCqctVvnpADZJe83/cart/" + str(orderNames) , "CEDARsubtotal", total)
            database.put("/Qn4DcOURt9NUPCqctVvnpADZJe83/cart/" + str(orderNames) , "CEDARtax", tax)
            database.put("/Qn4DcOURt9NUPCqctVvnpADZJe83/cart/" + str(orderNames) , "CEDARTotal", taxTotal)
            database.put("/Qn4DcOURt9NUPCqctVvnpADZJe83/cart/"+str(orderNames),"/translated/",1)