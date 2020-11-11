#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time         # time.sleepを使いたいので
import cv2          # OpenCVを使うため
import numpy as np

# メイン関数
def main():
    pic = 10
    finish=0
    try:
        while True:
            #finishがTrueのときループ終了
            if finish:
                cv2.destroyAllWindows()
                print('実験終了します！')
                break
            
            #使うときは日付と見たい写真を変更する
            date = "20201030"
            pic_num = str(pic) + '.jpg'
            path = './TestResult/' + date + '/' + pic_num
            print(path)
            image = cv2.imread(path)
            # (B)ここから画像処理
            # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)      # OpenCV用のカラー並びに変換する
            # bgr_image = cv2.resize(image, dsize=(480,360) ) # 画像サイズを半分に変更

            # トラックバーを作るため，まず最初にウィンドウを生成
            cv2.namedWindow("HSV adjustor")

            # トラックバーのコールバック関数は何もしない空の関数
            def nothing(x):
                pass
            # トラックバーの生成
            cv2.createTrackbar("H_min", "HSV adjustor", 230, 255, nothing)       # Hueの最大値は179
            cv2.createTrackbar("H_max", "HSV adjustor", 7, 255, nothing)
            cv2.createTrackbar("S_min", "HSV adjustor", 65, 255, nothing)
            cv2.createTrackbar("S_max", "HSV adjustor", 255, 255, nothing)
            cv2.createTrackbar("V_min", "HSV adjustor", 0, 255, nothing)
            cv2.createTrackbar("V_max", "HSV adjustor", 255, 255, nothing)
            hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV_FULL)  # BGR画像 -> HSV画像
            
            while True:

                # トラックバーの値を取る
                h_min = cv2.getTrackbarPos("H_min", "HSV adjustor")
                h_max = cv2.getTrackbarPos("H_max", "HSV adjustor")
                s_min = cv2.getTrackbarPos("S_min", "HSV adjustor")
                s_max = cv2.getTrackbarPos("S_max", "HSV adjustor")
                v_min = cv2.getTrackbarPos("V_min", "HSV adjustor")
                v_max = cv2.getTrackbarPos("V_max", "HSV adjustor")
                # inRange関数で範囲指定２値化 -> マスク画像として使う
                # mask_image = cv2.inRange(hsv_image, (h_min, s_min, v_min), (h_max, s_max, v_max)) # HSV画像なのでタプルもHSV並
                
                h = hsv_image[:, :, 0] # 色相(Hue)                          
                s = hsv_image[:, :, 1] #彩度(Saturation)
                mask_image = np.zeros(h.shape, dtype=np.uint8) # 赤いところを示すマスクデータ作成
                mask_image[((h < h_max) | (h > h_min)) & (s > s_min)] = 255
                contours, _ = cv2.findContours(mask_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # 輪郭を作成
                rects = []
                for contour in contours: # 内包する凸形状を作り、矩形を計算
                    approx = cv2.convexHull(contour)
                    rect = cv2.boundingRect(approx)
                    rects.append(np.array(rect))
                if len(rects) > 0:
                    rect = max(rects, key=(lambda x: x[2] * x[3]))  # 最大の矩形を探索
                
                # bitwise_andで元画像にマスクをかける -> マスクされた部分の色だけ残る
                result_image = cv2.bitwise_and(hsv_image, hsv_image, mask=mask_image)
                cv2.rectangle(result_image, tuple(rect[0:2]), tuple(rect[0:2] + rect[2:4]), (0, 0, 255), thickness=2) 
                
                # (X)ウィンドウに表示
                cv2.imshow('HSV adjustor', result_image)   # ウィンドウに表示するイメージを変えれば色々表示できる
                key = cv2.waitKey(0)
                if key==ord('k'):
                    pic -= 10                   # keyが k だったらwhileループを脱出，前の写真へ
                    break
                elif key==ord('j'):
                    pic += 10                   # keyが j  だったらwhileループを脱出，次の写真へ
                    break

                elif key==ord('a'):             # keyが a だったらトラックバーから閾値を読み取ってもう一度画像処理
                    pass

                elif key==ord('f'):　　　　　　　# keyが f だったら全体のループを終了
                    finish=1
                    break
                
                
    except KeyboardInterrupt:    # Ctrl+cが押されたら離脱
        print( "終了！" )

# "python main.py"として実行された時だけ動く様にするおまじない処理
if __name__ == "__main__":      # importされると"__main__"は入らないので，実行かimportかを判断できる．
    main()    # メイン関数を実行