import cv2
import numpy as np

def FlannMatch(parentImg, childImg):
    MIN_MATCH_COUNT=10 #设置最低匹配数量为10
    sift=cv2.xfeatures2d.SIFT_create() #创建sift检测器
    kp1,des1=sift.detectAndCompute(childImg,None) 
    kp2,des2=sift.detectAndCompute(parentImg,None)
    #创建设置FLAAN匹配
    FLANN_INDEX_KDTREE=0
    index_params=dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params=dict(checks=50)
    flann=cv2.FlannBasedMatcher(index_params,search_params)
    mathces=flann.knnMatch(des1,des2,k=2)
    good=[]
    #过滤不合格的匹配结果，大于0.7的都舍弃
    for m,n in mathces:
        if m.distance<0.7*n.distance:
            good.append(m)
    #如果匹配结果大于10，则获取关键点的坐标，用于计算变换矩阵
    if len(good)>MIN_MATCH_COUNT:
        src_pts=np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1,1,2)
        dst_pts =np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
    
        #计算变换矩阵和掩膜
        M,mask=cv2.findHomography(src_pts,dst_pts,cv2.RANSAC,10.0)
        matchesMask=mask.ravel().tolist()
        #根据变换矩阵进行计算，找到小图像在大图像中的位置
        h,w=childImg.shape
        pts=np.float32([[0,0],[0,h-1],[w-1,h-1],[w-1,0]]).reshape(-1,1,2)
        dst=cv2.perspectiveTransform(pts,M)
        return dst
    else:
        matchesMask=None
        return None
    pass

def GetMatchResultCentralPoint(matchResult):
    x = int(np.average(matchResult, axis =0, weights=None)[0][0])
    y = int(np.average(matchResult, axis =0, weights=None)[0][1])
    return (x,y)

def SetMatchFlag(screen, matchResult):
    # 标记目标图位置
    cv2.polylines(screen,[np.int32(matchResult)],True,0,5,cv2.LINE_AA)
    pass

