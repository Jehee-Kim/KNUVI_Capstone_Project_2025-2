70, 50 모두 오히려 denoising 이후에 수치가 더 떨어짐
jpeg 저압축 구간에서는 nafnet이 오히려 과하게 smoothing하면서 세부정보를 손실했기 때문으로 판단됨

# JPEG70 result

=== 00000.png ===
PSNR  Input : 28.5480
PSNR  Output: 25.8418
SSIM  Input : 0.9163
SSIM  Output: 0.8281
LPIPS Input : 0.0401
LPIPS Output: 0.1856

=== 00001.png ===
PSNR  Input : 28.8253
PSNR  Output: 25.9934
SSIM  Input : 0.9162
SSIM  Output: 0.8322
LPIPS Input : 0.0378
LPIPS Output: 0.2045

=== 00002.png ===
PSNR  Input : 28.6410
PSNR  Output: 25.6540
SSIM  Input : 0.9065
SSIM  Output: 0.8056
LPIPS Input : 0.0432
LPIPS Output: 0.2393

=== 00003.png ===
PSNR  Input : 28.7847
PSNR  Output: 26.1615
SSIM  Input : 0.9025
SSIM  Output: 0.8063
LPIPS Input : 0.0460
LPIPS Output: 0.2260

=== 00004.png ===
PSNR  Input : 28.5652
PSNR  Output: 25.9818
SSIM  Input : 0.9137
SSIM  Output: 0.8333
LPIPS Input : 0.0371
LPIPS Output: 0.1845

=== 00005.png ===
PSNR  Input : 29.2107
PSNR  Output: 26.5584
SSIM  Input : 0.9224
SSIM  Output: 0.8434
LPIPS Input : 0.0416
LPIPS Output: 0.1628

=== 00006.png ===
PSNR  Input : 28.1341
PSNR  Output: 25.7477
SSIM  Input : 0.9168
SSIM  Output: 0.8418
LPIPS Input : 0.0388
LPIPS Output: 0.1789

=== 00007.png ===
PSNR  Input : 28.2454
PSNR  Output: 25.9183
SSIM  Input : 0.9181
SSIM  Output: 0.8438
LPIPS Input : 0.0399
LPIPS Output: 0.1791

=== 00008.png ===
PSNR  Input : 28.0414
PSNR  Output: 25.8066
SSIM  Input : 0.9318
SSIM  Output: 0.8714
LPIPS Input : 0.0453
LPIPS Output: 0.1725

=== 00009.png ===
PSNR  Input : 27.8653
PSNR  Output: 25.5431
SSIM  Input : 0.9274
SSIM  Output: 0.8615
LPIPS Input : 0.0381
LPIPS Output: 0.1673

=== 00010.png ===
PSNR  Input : 28.1358
PSNR  Output: 25.8560
SSIM  Input : 0.9557
SSIM  Output: 0.9050
LPIPS Input : 0.0372
LPIPS Output: 0.1527

=== 00011.png ===
PSNR  Input : 27.0724
PSNR  Output: 24.9924
SSIM  Input : 0.9339
SSIM  Output: 0.8813
LPIPS Input : 0.0387
LPIPS Output: 0.1903

=== 00012.png ===
PSNR  Input : 30.3294
PSNR  Output: 26.2429
SSIM  Input : 0.9388
SSIM  Output: 0.8578
LPIPS Input : 0.0378
LPIPS Output: 0.2268

=== 00013.png ===
PSNR  Input : 28.6934
PSNR  Output: 25.8158
SSIM  Input : 0.9298
SSIM  Output: 0.8573
LPIPS Input : 0.0366
LPIPS Output: 0.1783

=== 00014.png ===
PSNR  Input : 29.4634
PSNR  Output: 26.6949
SSIM  Input : 0.9345
SSIM  Output: 0.8681
LPIPS Input : 0.0390
LPIPS Output: 0.1773

=== 00015.png ===
PSNR  Input : 28.1867
PSNR  Output: 25.6129
SSIM  Input : 0.9397
SSIM  Output: 0.8852
LPIPS Input : 0.0325
LPIPS Output: 0.1559

=== 00016.png ===
PSNR  Input : 28.5983
PSNR  Output: 25.6482
SSIM  Input : 0.9321
SSIM  Output: 0.8600
LPIPS Input : 0.0397
LPIPS Output: 0.1698

=== 00017.png ===
PSNR  Input : 30.2642
PSNR  Output: 25.9403
SSIM  Input : 0.9422
SSIM  Output: 0.8678
LPIPS Input : 0.0334
LPIPS Output: 0.2092

=== 00018.png ===
PSNR  Input : 29.3481
PSNR  Output: 26.1078
SSIM  Input : 0.9439
SSIM  Output: 0.8751
LPIPS Input : 0.0290
LPIPS Output: 0.1570

=== 00019.png ===
PSNR  Input : 28.7177
PSNR  Output: 25.2685
SSIM  Input : 0.9349
SSIM  Output: 0.8505
LPIPS Input : 0.0339
LPIPS Output: 0.2004

=== 00020.png ===
PSNR  Input : 29.4732
PSNR  Output: 25.7875
SSIM  Input : 0.9392
SSIM  Output: 0.8777
LPIPS Input : 0.0246
LPIPS Output: 0.1448

=== 00021.png ===
PSNR  Input : 29.0628
PSNR  Output: 24.7870
SSIM  Input : 0.9367
SSIM  Output: 0.8432
LPIPS Input : 0.0317
LPIPS Output: 0.1984

==============================
📊 전체 평균 결과
==============================
평균 PSNR (Input):  28.7367 dB
평균 PSNR (Output): 25.8164 dB
평균 SSIM (Input):  0.9288
평균 SSIM (Output): 0.8544
평균 LPIPS (Input):  0.0374
평균 LPIPS (Output): 0.1846


# jpeg50 result

=== 00000.png ===
PSNR  Input : 26.8321
PSNR  Output: 25.0764
SSIM  Input : 0.8715
SSIM  Output: 0.7899
LPIPS Input : 0.0781
LPIPS Output: 0.2321

=== 00001.png ===
PSNR  Input : 27.0272
PSNR  Output: 25.2185
SSIM  Input : 0.8708
SSIM  Output: 0.7938
LPIPS Input : 0.0774
LPIPS Output: 0.2485

=== 00002.png ===
PSNR  Input : 26.9194
PSNR  Output: 25.0081
SSIM  Input : 0.8585
SSIM  Output: 0.7691
LPIPS Input : 0.0811
LPIPS Output: 0.2856

=== 00003.png ===
PSNR  Input : 27.1053
PSNR  Output: 25.4072
SSIM  Input : 0.8531
SSIM  Output: 0.7658
LPIPS Input : 0.0912
LPIPS Output: 0.2784

=== 00004.png ===
PSNR  Input : 26.8627
PSNR  Output: 25.1669
SSIM  Input : 0.8694
SSIM  Output: 0.7940
LPIPS Input : 0.0767
LPIPS Output: 0.2392

=== 00005.png ===
PSNR  Input : 27.5948
PSNR  Output: 25.8155
SSIM  Input : 0.8855
SSIM  Output: 0.8110
LPIPS Input : 0.0755
LPIPS Output: 0.2053

=== 00006.png ===
PSNR  Input : 26.4065
PSNR  Output: 24.9475
SSIM  Input : 0.8730
SSIM  Output: 0.8035
LPIPS Input : 0.0780
LPIPS Output: 0.2182

=== 00007.png ===
PSNR  Input : 26.5683
PSNR  Output: 25.0896
SSIM  Input : 0.8759
SSIM  Output: 0.8054
LPIPS Input : 0.0760
LPIPS Output: 0.2262

=== 00008.png ===
PSNR  Input : 26.3169
PSNR  Output: 24.8199
SSIM  Input : 0.8968
SSIM  Output: 0.8363
LPIPS Input : 0.0856
LPIPS Output: 0.2305

=== 00009.png ===
PSNR  Input : 26.1463
PSNR  Output: 24.7395
SSIM  Input : 0.8881
SSIM  Output: 0.8281
LPIPS Input : 0.0678
LPIPS Output: 0.2005

=== 00010.png ===
PSNR  Input : 26.6473
PSNR  Output: 25.2502
SSIM  Input : 0.9317
SSIM  Output: 0.8887
LPIPS Input : 0.0672
LPIPS Output: 0.1763

=== 00011.png ===
PSNR  Input : 25.4080
PSNR  Output: 24.3844
SSIM  Input : 0.8995
SSIM  Output: 0.8596
LPIPS Input : 0.0710
LPIPS Output: 0.2062

=== 00012.png ===
PSNR  Input : 28.5308
PSNR  Output: 26.0324
SSIM  Input : 0.9090
SSIM  Output: 0.8452
LPIPS Input : 0.0686
LPIPS Output: 0.2372

=== 00013.png ===
PSNR  Input : 26.8591
PSNR  Output: 25.1606
SSIM  Input : 0.8920
SSIM  Output: 0.8291
LPIPS Input : 0.0685
LPIPS Output: 0.2026

=== 00014.png ===
PSNR  Input : 27.7133
PSNR  Output: 26.0532
SSIM  Input : 0.9005
SSIM  Output: 0.8424
LPIPS Input : 0.0701
LPIPS Output: 0.2074

=== 00015.png ===
PSNR  Input : 26.3635
PSNR  Output: 24.7607
SSIM  Input : 0.9063
SSIM  Output: 0.8560
LPIPS Input : 0.0620
LPIPS Output: 0.1894

=== 00016.png ===
PSNR  Input : 26.8020
PSNR  Output: 24.8156
SSIM  Input : 0.8967
SSIM  Output: 0.8265
LPIPS Input : 0.0801
LPIPS Output: 0.2176

=== 00017.png ===
PSNR  Input : 28.4281
PSNR  Output: 25.6690
SSIM  Input : 0.9139
SSIM  Output: 0.8542
LPIPS Input : 0.0609
LPIPS Output: 0.2187

=== 00018.png ===
PSNR  Input : 27.3909
PSNR  Output: 25.4366
SSIM  Input : 0.9113
SSIM  Output: 0.8513
LPIPS Input : 0.0514
LPIPS Output: 0.1789

=== 00019.png ===
PSNR  Input : 26.8101
PSNR  Output: 24.5364
SSIM  Input : 0.8990
SSIM  Output: 0.8204
LPIPS Input : 0.0633
LPIPS Output: 0.2321

=== 00020.png ===
PSNR  Input : 27.6152
PSNR  Output: 25.0807
SSIM  Input : 0.9088
SSIM  Output: 0.8534
LPIPS Input : 0.0473
LPIPS Output: 0.1731

=== 00021.png ===
PSNR  Input : 27.1518
PSNR  Output: 24.1768
SSIM  Input : 0.9041
SSIM  Output: 0.8176
LPIPS Input : 0.0569
LPIPS Output: 0.2310

==============================
📊 전체 평균 결과
==============================
평균 PSNR (Input):  26.9773 dB
평균 PSNR (Output): 25.1203 dB
평균 SSIM (Input):  0.8916
평균 SSIM (Output): 0.8246
평균 LPIPS (Input):  0.0707
평균 LPIPS (Output): 0.2198
